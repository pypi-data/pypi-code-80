from datawidgets.imports import *
from ..interface import *
from .image_mixins import *

# from datawidgets.dataset.image_dataset import ImageClassificationDataset

from icevision.core.class_map import ClassMap


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


class ImageWithLabels(ImageDataPoint, ClassificationLabelsMixin):
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

        if isinstance(labels, str):
            labels = [labels]
        if not isinstance(labels, list):
            raise TypeError(f"Expected a list of labels, got {type(labels)}")

        # HACK ...fuck this...
        self._labels = labels

        super().__init__(source=source, width=width)

    def setup(self):
        # Call mixins' setup methods
        self.setup_img()
        self.setup_mouse_interaction()
        self.setup_labelling()

    def update_view(self):
        self.view.children = [
            self.img,
            self.searchbox,
            self.label_buttons.buttons,
        ]
