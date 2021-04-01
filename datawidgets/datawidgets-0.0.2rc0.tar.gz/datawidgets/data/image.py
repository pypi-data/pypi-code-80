from datawidgets.imports import *
from ..interface import *
from .image_mixins import *

# from datawidgets.dataset.image_dataset import ImageClassificationDataset

# from icevision.core.class_map import ClassMap


class ImageDataPoint(
    AbstractInterface,
    ImageLoaderMixin,
    ImageMouseInteractionMixin,
):
    def setup(self):
        # Call mixins' setup methods
        self.setup_img()
        self.setup_mouse_interaction()

    def setup_view(self):
        self.view = VBox([self.img])
        self.view.layout = Layout(width=f"{self.width}%")
        self.view.add_class(f"{CSS_NAMES.IMG_BOX_CONTAINER}")

    def update_view(self):
        self.view.children = [self.img]


class ImageWithLabels(ImageDataPoint, ClassificationLabelsMixin, NoteMixin):
    def __init__(
        self,
        class_map: ClassMap,
        source: Union[str, Path, Any],
        labels: Union[str, List[str]] = [],
        is_multilabel: bool = False,
        width: int = 100,
        parent_dataset=None,
        # dset_df: pd.DataFrame = None,
        # dset_df_label_col: str = "label",
    ):
        self.class_map = class_map
        self.classes = self.class_map._id2class
        self.is_multilabel = is_multilabel
        self.dset = parent_dataset
        self.is_completed = False

        if isinstance(labels, str):
            labels = [labels]
        if not isinstance(labels, list):
            raise TypeError(f"Expected a list of labels, got {type(labels)}")

        # HACK ...fuck this...
        self._labels = labels

        super().__init__(source=source, width=width)

    def mark_as_completed(self):
        self.unselect()
        self.is_completed = True
        self.img.add_class(CSS_NAMES.IMG_COMPLETED)

    def setup(self):
        # Call mixins' setup methods
        self.setup_img()
        self.setup_note()
        self.setup_mouse_interaction()
        self.setup_labelling()

    def attach_click_event(self, on_click_func: Callable):
        "Helper func to call `on_click_func` when `self.view` is clicked"

        def update_on_click(event):
            if event["type"] == "click":
                on_click_func()

        ev = Event(source=self.view, watched_events=["click"])
        ev.on_dom_event(update_on_click)

        self.log_message(f"Attached {on_click_func.__func__.__name__} event")

    def attach_mouse_click_dset_event(self, func):
        "Wrapper func for using `self.attach_click_event` on functions from the parent dataset"
        if self.dset is not None:
            if hasattr(self.dset, func):
                self.attach_click_event(getattr(self.dset, func))

    def dset_width_slider_observer(self):
        if self.dset is not None:
            if hasattr(self.dset, "width_slider"):
                # self.view.layout = Layout(width=f"{self.dset.width_slider.value}%")
                self.dset.width_slider.observe(
                    lambda x: setattr(
                        self.view,
                        "layout",
                        Layout(width=f"{self.dset.width_slider.value}%"),
                    ),
                    "value",
                )

    def attach_event_handlers(self):
        # Put in event observers that need to be attached as a datapoint
        # is created in here
        self.attach_mouse_click_dset_event("update_info")
        self.attach_mouse_click_dset_event("update_batch_labelling_descriptions")
        self.dset_width_slider_observer()

    def update_view(self):
        self.attach_event_handlers()
        self.view.children = [
            self.img,
            self.note,
            HBox([self.toggle_note_button, self.searchbox]),
            self.label_buttons.buttons,
        ]
