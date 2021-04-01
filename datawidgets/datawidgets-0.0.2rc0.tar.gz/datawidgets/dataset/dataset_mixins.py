from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *
from .image_dataset import *


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

    @property
    def batch_add_value(self):
        return self.batch_add_button.v_model

    @property
    def batch_remove_value(self):
        return self.batch_remove_button.v_model

    def update_batch_labelling_descriptions(self, *args):
        self.batch_add_button.label = f"Batch Add ({len(self.selected_items)})"
        self.batch_remove_button.label = f"Batch Remove ({len(self.selected_items)})"

        # `hasattr` is used here IN CASE this function is called before
        # `setup_batch_labelling` is called. We could probably do away with
        # it but it's here for safety as setup functions don't have an order
        if hasattr(self, "class_map_negative_buttons"):
            self.batch_remove_button.items = flatten(
                [i.labels for i in self.selected_items]
            )

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
        self.width_slider.observe(
            lambda x: setattr(self, "width", self.width_slider.value)
        )


class DeleteSelectionMixin:
    def generate_delete_button(self, callbacks=[]):
        ""

        def delete_selected(*args):
            self.num_deleted = self.num_deleted + len(self.selected_names)

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

    def unselect_all(self, *args, callbacks=[]):
        for item in self.active_datapoints:
            item["item"].unselect()

    def select_all(self, *args, callbacks=[]):
        for item in self.active_datapoints:
            item["item"].select()

    def invert_selection(self, *args, callbacks=[]):
        for i in self.active_datapoints:
            item = i["item"]
            if item.is_selected:
                item.unselect()
            else:
                item.select()

    def generate_unselect_all_button(self, callbacks=[]):
        "Generates a button that unselects all selected items"

        unselect_all_button = Button(description="Unselect All")
        unselect_all_button.on_click(self.unselect_all)
        for cb in callbacks:
            unselect_all_button.on_click(cb)

        return unselect_all_button

    def generate_select_all_button(self, callbacks=[]):
        "Generates a button that selects all selected items"

        select_all_button = Button(description="Select All")
        select_all_button.on_click(self.select_all)
        for cb in callbacks:
            select_all_button.on_click(cb)

        return select_all_button

    def generate_invert_selection_button(self, callbacks=[]):
        "Generates a button to invert selected items"

        button = Button(description="Invert Selection")
        button.on_click(self.invert_selection)
        for cb in callbacks:
            button.on_click(cb)

        return button


class MarkCompletedMixin:
    def setup_mark_completed(self):

        self.mark_completed_toggle.add_class()

    def mark_selected_as_completed(self, *args):
        for i in self.active_datapoints:
            if i["item"].is_selected:
                i["item"].mark_as_completed()

    def toggle_view_mark_completed(self, *args):
        self.hide_completed = not self.hide_completed

    def generate_mark_completed_buttons(self, callbacks=[]):
        self.hide_completed = False
        return [
            self._generate_mark_completed_button(callbacks=callbacks),
            self._generate_mark_view_toggle_button(callbacks=callbacks),
        ]

    def _generate_mark_view_toggle_button(self, callbacks=[]):
        toggle = widgets.Button(description="Hide Completed")
        toggle.add_class(CSS_NAMES.SHOW_COMPLETED_TOGGLE)

        def change_btn_description(*args):
            self.toggle_view_mark_completed()
            if self.hide_completed:
                toggle.description = "Show Completed"
            else:
                toggle.description = "Hide Completed"

        toggle.on_click(change_btn_description)
        for cb in callbacks:
            toggle.on_click(cb)

        return toggle

    def _generate_mark_completed_button(self, callbacks=[]):

        button = Button(description="Mark As Completed")
        button.add_class(CSS_NAMES.MARK_AS_COMPLETED_BUTTON)
        button.on_click(self.mark_selected_as_completed)

        for cb in callbacks:
            button.on_click(cb)

        return button


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

    _maybe_uses = ["ClassMapFilterMixin"]

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
        items = []
        if hasattr(self, "grid_range_slider"):
            val = self.grid_range_slider.value
        else:
            val = (0, 50)

        if hasattr(self, "positive_class_map_filter"):
            df = self.filter_dataset(self.class_map_subset_filter)
            for i, fname in enumerate(df.filename):
                if i >= val[0] and i < val[1]:
                    item = self.datapoints[fname]
                    if hasattr(self, "hide_completed"):
                        if item["item"].is_completed and self.hide_completed:
                            continue
                        else:
                            items.append(item)
                    else:
                        items.append(item)

        else:
            for i, (key, item) in enumerate(self.datapoints.items()):
                if i >= val[0] and i < val[1]:
                    items.append(item)

        children = [i["view"] for i in items]
        self.active_datapoints = items
        self.grid.children = children

    def reset_grid_range_value(self, *args):
        self.grid_range_slider.value = (0, 50)

    def set_grid_range_slider(self, grid_range_slider: widgets.IntRangeSlider):
        self.grid_range_slider = grid_range_slider
        self.update_grid()

    def update_grid_range_slider(self, *args):
        min_value, max_value = self.grid_range_slider.value
        max_limit = len(self)

        if max_value > len(self):
            max_value = len(self)

        num_filtered_items = len(self)
        if hasattr(self, "positive_class_map_filter"):
            num_filtered_items = (
                self.positive_class_map_filter & self.negative_class_map_filter
            ).sum()
            if max_value > num_filtered_items:
                max_value = num_filtered_items
        max_limit = min(len(self), num_filtered_items)

        self.grid_range_slider.value = (min_value, max_value)
        self.grid_range_slider.max = max_limit

    def generate_grid_range_slider(self, callbacks=[]):
        grid_range_slider = widgets.IntRangeSlider(
            value=(0, 50),
            min=0,
            max=len(self),
            description="Show Img #",
        )
        grid_range_slider.add_class(CSS_NAMES.GRID_RANGE_SLIDER)
        grid_range_slider.continuous_update = False

        def increment_range(*args):
            range_values = grid_range_slider.value
            grid_range_slider.value = (range_values[1], range_values[1] + 50)
            self.update_grid_range_slider()

        def decrement_range(*args):
            range_values = grid_range_slider.value
            grid_range_slider.value = (range_values[0] - 50, range_values[0])
            self.update_grid_range_slider()

        grid_range_slider.observe(self.update_grid, "value")
        if hasattr(self, "update_info"):
            grid_range_slider.observe(self.update_info, "value")
        grid_range_slider.observe(self.update_grid_range_slider, "value")

        for cb in callbacks:
            grid_range_slider.observe(cb, "value")

        increment_button = Button(description="»")
        decrement_button = Button(description="«")

        increment_button.add_class(CSS_NAMES.RANGE_NEXT_PREV_BUTTONS)
        decrement_button.add_class(CSS_NAMES.RANGE_NEXT_PREV_BUTTONS)
        increment_button.on_click(increment_range)
        decrement_button.on_click(decrement_range)

        return decrement_button, grid_range_slider, increment_button


class InfoMixin:
    def update_info(self, *args, additional_info: List[str] = []):
        if isinstance(additional_info, str):
            additional_info = [additional_info]

        info = [
            f"Selected: {self.num_selected}",
            f"Images In Grid: {len(self.grid.children)}"
            if hasattr(self, "grid")
            else "",
            f"Total Images: {len(self)}",
            f"Deleted: {self.num_deleted}",
            f"Modified: {self.num_modified}",
            f"Completed: {self.num_completed}/{len(self)}",
        ]

        info = "&emsp;&emsp;".join(info)
        self.info.value = f"<h5>{info}<h5>"

        self.info.add_class(CSS_NAMES.MAIN_INFO_PANEL)
        self.info.layout = CSS_LAYOUTS.flex_layout

    def setup_info(self):
        self.info = widgets.HTML()
