from datawidgets.imports import *


# TODO: Refactor
class CSS_LAYOUTS:
    empty = Layout(width="0px", height="0px")
    button_layout = Layout(
        margin="0",
        width="auto",
        height="30px",
        border="0.1px solid black",
        justify_content="flex-start",
    )
    flex_layout = Layout(
        display="flex",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="center",
        align_items="center",
    )
    flex_layout_col = Layout(
        display="flex",
        flex_flow="column wrap",
        width=f"100%",
        justify_content="center",
        align_items="center",
    )
    autowidth = Layout(width="auto")
    wide_button = Layout(width="200px")
    flex_padded = Layout(
        display="flex",
        padding="0.25em",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="center",
        align_items="center",
    )
    class_map_buttons = Layout(
        display="flex",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="flex-start",
    )


class CSS_NAMES:
    IMG_BOX = "image-box"

    LABEL_BUTTON = "label-button"
    MODIFIED_LABEL_BUTTON = "label-button-modified"
    LABEL_BUTTON_TOGGLED = "label-button-toggled"
    LABEL_BUTTON_GROUP = "label-button-group"
    LABEL_SEARCH_BOX = "label-searchbox"
    AUTOCOMPLETE_BOX = "autocomplete-box"
    BATCH_ADD_BUTTON = "batch-add-button"
    BATCH_REMOVE_BUTTON = "batch-remove-button"
    FILE_UPLOAD_BUTTON = "file-upload-button"

    def __init__(self):
        self.IMG_BOX_HOVER = f"{self.IMG_BOX}-on-hover"
        self.IMG_BOX_SELECTED = f"{self.IMG_BOX}-selected"
        self.IMG_BOX_CONTAINER = f"{self.IMG_BOX}-container"
        self.IMG_BOX_CONTAINER_SELECTED = f"{self.IMG_BOX_CONTAINER}-selected"
        self.FILE_UPLOAD_REFRESH_BUTTON = f"{self.FILE_UPLOAD_BUTTON}-refresh"
        self.FILE_UPLOAD_CONTAINER = f"{self.FILE_UPLOAD_BUTTON}-container"
        self.FILE_UPLOAD_GO_BUTTON = f"{self.FILE_UPLOAD_BUTTON}-go"


CSS_NAMES = CSS_NAMES()
