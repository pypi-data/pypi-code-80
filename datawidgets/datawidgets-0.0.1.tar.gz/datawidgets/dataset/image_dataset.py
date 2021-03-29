from datawidgets.imports import *
from .review_mixins import *
from .dataset_mixins import *
from datawidgets.data import *
from datawidgets.interface import *


class ImageDataset(
    AbstractInterface,
    ImageGridMixin,
    WidthSliderMixin,
    DeleteSelectionMixin,
    InfoMixin,
):
    def __init__(self, df, width: int = 100):
        self.df = df
        self.df.index = self.df.filename
        self.width = width
        self.view_components = []
        self.view_css_classes = []

        self.setup()
        self.setup_view()

    def setup_items(self):
        items = {}
        for idx, fname in tqdm(
            self.df.filename.iteritems(), total=len(self), desc="Setup Data Items"
        ):
            item = ImageDataPoint(fname)
            items[idx] = {
                "item": item,
                "view": item.view,
            }
        self.datapoints = items

    @staticmethod
    def _check_filter(filter_: Union[Sequence[str], np.ndarray, pd.Series]):
        if isinstance(filter_, pd.Series):
            # Keep only True values if boolean masking
            if isinstance(filter_.iloc[0], (bool, np.bool8, np.bool)):
                filter_ = filter_[filter_]
            filter_ = filter_.index.values
        return filter_

    def filter_dataset(self, filter_: Union[Sequence[str], np.ndarray, pd.Series]):
        "Returns a view of `self.df` without any modifications"
        filter_ = self._check_filter(filter_)
        return self.df.loc[filter_]

    def filter_and_mutate_dataset(
        self, filter_: Union[Sequence[str], np.ndarray, pd.Series]
    ):
        """
        Reorder and/or delete items from internal dataset by self.df's index, which
            is set to the filename on init
        If passing in a boolean `pd.Series` mask, only True values are kept
        """
        filter_ = self._check_filter(filter_)
        items = {}
        for i in filter_:
            # del self.datapoints[i]
            items[i] = self.datapoints[i]
        self.datapoints = items
        self.df = self.df.loc[filter_]

    def refresh(self):
        self.update_grid()
        self.update_info()

    # def __repr__(self):
    #     self._repr_html_()

    def setup(self):
        self.setup_items()
        self.setup_logging()
        self.setup_width_slider()
        self.setup_img_grid()
        self.setup_info()

    def __len__(self):
        return len(self.df)

    # TODO: Is it inefficient to have these properties for very large datasets?
    @property
    def selected_names(self):
        return [item.source for item in self.selected_items]

    @property
    def num_selected(self):
        return sum([item["item"].is_selected for item in self.datapoints.values()])

    @property
    def selected_items(self):
        return [
            item["item"]
            for item in self.datapoints.values()
            if item["item"].is_selected
        ]


class ImageClassificationDataset(
    ImageDataset,
    BatchClassificationLabelsMixin,
    ClassMapFilterMixin,
    ReviewMixin,
    DownloadModifiedMixin,
):
    def __init__(
        self,
        df,
        width: int = 25,
        class_map: Optional[ClassMap] = None,
        label_col: str = "label",
        is_multilabel: bool = False,
    ):
        self.df = df
        self.label_col = label_col
        self.is_multilabel = is_multilabel

        # Derive class map from `label_col` if not passed in
        if class_map is None:
            # TODO: Multi-label class map
            if not self.is_multilabel:
                self.class_map = ClassMap(
                    classes=list(self.df[self.label_col].unique()),
                    background=None,
                )
            else:

                def convert_labels_to_list(label: Union[str, List[str]]):
                    if isinstance(label, str):
                        return [label]
                    elif isinstance(label, list):
                        return label
                    elif isinstance(label, np.ndarray):
                        if isinstance(label[0], str):
                            return list(label)
                    raise TypeError(
                        f"Expected string or list of labels, got {type(label)}"
                    )

                self.df[self.label_col] = self.df[self.label_col].apply(
                    convert_labels_to_list
                )
                all_labels = self.df[self.label_col].values
                self.class_map = ClassMap(
                    classes=uniqueify(flatten(all_labels)),
                    background=None,
                )
        else:
            self.class_map = class_map

        self.classes = self.class_map._id2class

        # HACK: blah..
        super().__init__(df=self.df, width=100)
        self.width = width
        self.width_slider.value = self.width

    def get_modified_df(self):
        rows = []
        for fname, datapoint in self.datapoints.items():
            if datapoint["item"].is_modified:
                rows.append([fname, datapoint["item"].labels])

        modified_df = pd.DataFrame(rows, columns=["filename", self.label_col])
        modified_df = modified_df.merge(
            self.df.drop(columns=[self.label_col]).reset_index(drop=True),
            on="filename",
        )
        modified_df.index = modified_df.filename
        return modified_df

    def setup(self):
        super().setup()
        self.setup_batch_labelling()
        self.setup_class_map_filtering()
        self.setup_review_grid()
        self.setup_download_modified()

    def setup_items(self):
        items = {}
        for idx, row in tqdm(
            self.df.iterrows(), total=len(self.df), desc="Setting Up Data Items"
        ):
            item = ImageWithLabels(
                source=row.filename,
                class_map=self.class_map,
                labels=row[self.label_col],
                is_multilabel=self.is_multilabel,
                parent_dataset=self,
            )
            items[idx] = {
                "item": item,
                "view": item.view,
            }
        self.datapoints = items

    def setup_view(self):
        delete_button = self.generate_delete_button()
        view_range_slider = self.generate_grid_range_slider()
        unselect_button = self.generate_unselect_all_button()
        select_button = self.generate_select_all_button()
        class_map_filtering_button = self.generate_class_map_filtering_button()
        refresh_review_button = self.generate_review_refresh_button()
        refresh_view_selected_button = self.generate_selected_refresh_button()
        refresh_export_button = self.generate_export_refresh_button()

        try:

            def reset_grid_idxs(*args):
                self.grid_range_slider.value = (
                    0,
                    min(self.grid_range_slider.value[1], len(self)),
                )

            similarity_button = self.generate_similarity_button(callbacks=[])
            similarity_button.on_click(reset_grid_idxs)

        except:
            similarity_button = Button()
            similarity_button.layout = CSS_LAYOUTS.empty

        self.set_grid_range_slider(view_range_slider)

        selection_controls = HBox([delete_button, select_button, unselect_button])
        image_view_controls = HBox([self.width_slider, self.grid_range_slider])
        sorting_controls = HBox([similarity_button])
        batch_labelling_controls = HBox(
            [
                self.batch_add_button,
                self.batch_remove_button,
            ]
        )
        review_controls = HBox([refresh_review_button, refresh_view_selected_button])
        class_map_filtering_controls = VBox(
            [
                class_map_filtering_button,
                self.class_map_buttons,
            ]
        )

        selection_controls.layout = CSS_LAYOUTS.flex_layout
        image_view_controls.layout = CSS_LAYOUTS.flex_layout
        sorting_controls.layout = CSS_LAYOUTS.flex_layout
        batch_labelling_controls.layout = CSS_LAYOUTS.flex_padded
        class_map_filtering_controls.layout = CSS_LAYOUTS.flex_layout_col
        review_controls.layout = CSS_LAYOUTS.flex_layout

        REVIEW_TAB = widgets.VBox(
            [
                review_controls,
                image_view_controls,
                selection_controls,
                batch_labelling_controls,
                self.review_grid,
            ]
        )

        refresh_export_button.click()
        refresh_export_button_centered = HBox([refresh_export_button])
        refresh_export_button_centered.layout = CSS_LAYOUTS.flex_layout
        EXPORT_TAB = VBox(
            [
                refresh_export_button_centered,
                self.export_area,
            ]
        )

        MAIN_CONTROLS = widgets.VBox(
            [
                class_map_filtering_controls,
                image_view_controls,
                selection_controls,
                sorting_controls,
                batch_labelling_controls,
            ]
        )

        MAIN_OUTPUT = widgets.Tab(
            [
                widgets.VBox([MAIN_CONTROLS, self.info, self.grid]),
                REVIEW_TAB,
                EXPORT_TAB,
            ]
        )

        MAIN_OUTPUT.set_title(0, "Main Labelling Main Labelling")
        MAIN_OUTPUT.set_title(1, "Review")
        MAIN_OUTPUT.set_title(2, "Export")
        self.view = MAIN_OUTPUT


class CinemaNetDataset(ImageClassificationDataset, CinemaNetSimilarityMixin):
    def __init__(
        self,
        df,
        width: int = 100,
        label_col: str = "label",
        is_multilabel: bool = False,
    ):
        super().__init__(
            df=df,
            width=width,
            label_col=label_col,
            is_multilabel=is_multilabel,
        )

    def setup(self):
        super().setup()
        self.setup_similarity()
