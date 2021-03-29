from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *
from .image_dataset import *


class ClassMapFilterMixin:
    """
    Filter images in a dataset based on any combination of labels
    from `self.class_map`
    """

    _works_with = "ImageClassificationDataset"
    _requires = "ImageGridMixin"

    # TODO: rename this lol
    @staticmethod
    def this_in_that(this: Union[str, list], that: list):
        if isinstance(this, str):
            this = [set]
        return set(this) - set(that) == set()

    def setup_class_map_filtering(self):
        self.class_map_buttons = ClassMapButtons(options=self.classes)
        self.class_map_buttons.layout = CSS_LAYOUTS.class_map_buttons

    def generate_class_map_filtering_button(self, global_callbacks=[]):
        button = Button(description="Filter Dataset")

        def show_subset(*args):
            df = self.filter_dataset(
                self.df[self.label_col].apply(
                    lambda label: self.this_in_that(
                        this=self.class_map_buttons.value, that=label
                    )
                )
            )
            self.update_grid(df=df)
            for cb in global_callbacks:
                cb()

        button.on_click(show_subset)
        return button


class BatchClassificationLabelsMixin:
    _works_with = "ImageDatasetWithLabels"

    def setup_batch_labelling(self):
        # Create add and remove buttons
        self.batch_add_button = vue_autocomplete_box(
            items=self.classes,
            css_classes=[CSS_NAMES.BATCH_ADD_BUTTON],
        )

        self.batch_remove_button = vue_autocomplete_box(
            items=self.classes,
            css_classes=[CSS_NAMES.BATCH_REMOVE_BUTTON],
        )

        # Attach observers / callbacks to batch labelling buttons
        self.batch_add_button.observe(self.add_batch_label)
        self.batch_remove_button.observe(self.remove_batch_label)
        self.update_batch_labelling_descriptions()

        # Attach batch labelling description obersers to all datapoints
        for item in self.datapoints.values():

            def update_on_click(event):
                if event["type"] == "click":
                    self.update_batch_labelling_descriptions()

            ev = Event(source=item["view"], watched_events=["click"])
            ev.on_dom_event(update_on_click)

    @property
    def batch_add_value(self):
        return self.batch_add_button.v_model

    @property
    def batch_remove_value(self):
        return self.batch_remove_button.v_model

    def update_batch_labelling_descriptions(self):
        self.batch_add_button.label = f"Batch Add ({len(self.selected_items)})"
        self.batch_remove_button.label = f"Batch Remove ({len(self.selected_items)})"

    def add_batch_label(self, change):
        if self.batch_add_value in self.classes:
            for i in self.selected_items:
                if not i.max_labels_selected:
                    i.add_label(self.batch_add_value)
            self.batch_add_button.v_model = ""

    def remove_batch_label(self, change):
        if self.batch_remove_value in self.classes:
            for i in self.selected_items:
                i.remove_label(self.batch_remove_value)
            self.batch_remove_button.v_model = ""


class WidthSliderMixin:
    def setup_width_slider(self):
        self.width_slider = widgets.IntSlider(
            value=self.width,
            min=1,
            max=100,
            description="Item Width:",
            layout=widgets.Layout(align_items="center"),
        )
        self.width_slider.continuous_update = False

        def observe_item_width(change):
            for item in self.datapoints.values():
                # item.width = self.width_slider.value
                # item.img.width = f"{self.width_slider.value}%"
                item["item"].img.width = f"100%"
                item["item"].view.layout = Layout(width=f"{self.width_slider.value}%")
                self.width = self.width_slider.value

        self.width_slider.observe(observe_item_width, "value")
        observe_item_width(None)  # Attach callbacks to items on init


class DeleteSelectionMixin:
    def generate_delete_button(self, callbacks=[]):
        ""

        def delete_selected(*args):
            filt = ~self.df.filename.isin(self.selected_names)
            self.filter_and_mutate_dataset(filt)
            self.refresh()

            self.log_message(f"Deleted {~filt.sum()} images")
            self.log_message(f"Reset self")

            for cb in callbacks:
                cb()

        delete_button = widgets.Button(description="Delete Selected")
        delete_button.on_click(delete_selected)
        return delete_button

    def generate_unselect_all_button(self):
        "Generates a button that unselects all selected items"

        def unselect_all(*args):
            for item in self.datapoints.values():
                item["item"].unselect()
                if hasattr(self, "update_info"):
                    self.update_info()

        unselect_all_button = Button(description="Unselect All")
        unselect_all_button.on_click(unselect_all)
        return unselect_all_button

    def generate_select_all_button(self):
        "Generates a button that selects all selected items"

        def unselect_all(*args):
            for item in self.datapoints.values():
                item["item"].select()
                if hasattr(self, "update_info"):
                    self.update_info()

        select_all_button = Button(description="Select All")
        select_all_button.on_click(unselect_all)
        return select_all_button


class CinemaNetSimilarityMixin:
    from scipy import spatial

    # TODO: Unused
    def setup_similarity(self):
        menu = widgets.Dropdown(
            options=["cinemanet_embedding", "cinemanet_probabilities"]
        )
        self.compare_key_options = menu

    def generate_similarity_button(self, callbacks=[]):
        ""

        def calc_similarity(*args):
            df = self.df
            filt = df.filename.apply(str).isin(self.selected_names)
            self.log_message(f"Selected {df[filt].filename}")

            similarity = df.apply(
                lambda row: self.compute_similarity(df[filt], row),
                axis=1,
            )
            self.log_message(f"Computed similarity")
            self.log_message(
                f"Similarity indices: {similarity.sort_values().index.values}"
            )

            self.filter_and_mutate_dataset(similarity.sort_values().index.values)
            self.refresh()
            # self.reset(df=df.loc[similarity.sort_values().index.values])
            self.log_message(f"Reset")

            for cb in callbacks:
                cb()

        button = widgets.Button(description="Sort By Similarity")
        button.on_click(calc_similarity)
        return button

    def compute_similarity(
        self,
        source: Union[pd.Series, pd.DataFrame],
        target: pd.Series,
        # compare_key: str = "cinemanet_embedding",
        metric_func: Callable = spatial.distance.cosine,
    ):
        source = convert_single_row_to_series(source)

        compare_key = self.compare_key_options.value
        self.log_message(f"Computing similarity by {compare_key}")

        if compare_key in ["cinemanet_embedding", "cinemanet_probabilities"]:
            return metric_func(source[compare_key], target[compare_key])
        else:
            raise RuntimeError(f"Invalid `compare_key`: {compare_key}")


class ImageGridMixin:
    """
    Sets up `self.grid` to contains `self.images`.
    Use `generate_grid_range_slider` followed by `set_grid_range_slider` in a global
      context like so:

    dset = ImageDataset(...)
    def REFRESH_GLOBAL_DISPLAY(...)
    indxs_slider = dset.generate_grid_range_slider(callbacks=[REFRESH_GLOBAL_DISPLAY])
    dset.set_grid_range_slider(indxs_slider)
    """

    def setup_img_grid(self):
        self.grid = widgets.Box(
            children=[],
            width="100%",
            layout=CSS_LAYOUTS.flex_layout,
        )
        self.update_grid()

    def update_grid(self, *args, df: pd.DataFrame = None):
        """Sets up self.grid to all `self.images` if no grid range slider is initialised
        else to the interval values of the slider
        """
        # TODO: Refactor
        if df is not None:
            children = []
            for fname in df.filename:
                children.append(self.datapoints[fname]["view"])

        else:
            if hasattr(self, "grid_range_slider"):
                children = []
                # items = {}
                val = self.grid_range_slider.value
                for i, (key, item) in enumerate(self.datapoints.items()):
                    if i >= val[0] and i <= val[1]:
                        children.append(item["view"])

                # children = self.images[slice(*self.grid_range_slider.value)]
            else:
                children = [item["view"] for item in self.datapoints.values()]

        self.grid.children = children

    def set_grid_range_slider(self, grid_range_slider: widgets.IntRangeSlider):
        self.grid_range_slider = grid_range_slider
        self.update_grid()

    def generate_grid_range_slider(self, callbacks=[]):
        grid_range_slider = widgets.IntRangeSlider(
            value=(0, 50),
            min=0,
            max=min(500, len(self)),
            description="Show Img #",
        )
        grid_range_slider.continuous_update = False

        def update_ranges(*args):
            """Checks to see if the slider's value is greater than num available items
            and reset the range value and the max possible value accordingly
            """
            # if hasattr(self, "grid_range_slider"):
            range_values = grid_range_slider.value
            if range_values[1] > len(self):
                range_values = (range_values[0], len(self))

            grid_range_slider.value = range_values
            grid_range_slider.max = min(500, len(self))

        grid_range_slider.observe(self.update_grid, "value")
        grid_range_slider.observe(update_ranges, "value")

        for cb in callbacks:
            grid_range_slider.observe(cb, "value")

        return grid_range_slider


class InfoMixin:
    def update_info(self):
        info = []
        info.append(f"Num Selected: {self.num_selected}")
        info.append(f"Total Num. Images: {len(self)}")
        info = "&emsp;".join(info)
        self.info.value = f"<h5>{info}<h5>"
        self.info.layout = get_flex_layout()

    def setup_info(self):
        self.info = widgets.HTML()

        # Update info whenever a datapoint is clicked
        for item in self.datapoints.values():

            def update_on_click(event):
                if event["type"] == "click":
                    self.update_info()

            ev = Event(source=item["view"], watched_events=["click"])
            ev.on_dom_event(update_on_click)

        self.update_info()
