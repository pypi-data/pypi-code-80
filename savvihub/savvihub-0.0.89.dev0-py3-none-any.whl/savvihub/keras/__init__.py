import keras

from savvihub import log
from savvihub.constants import SAVVIHUB_PLOTS_FILETYPE_IMAGE, SAVVIHUB_PLOTS_FILETYPE_IMAGES


class SavviHubCallback(keras.callbacks.Callback):
    def __init__(self, data_type=None, validation_data=None):
        super().__init__()
        self._data_type = data_type

        self.validation_data = None
        if validation_data is not None:
            self.validation_data = validation_data

    def on_epoch_end(self, epoch, logs=None):
        log(step=epoch, row=logs)

        if self._data_type in (SAVVIHUB_PLOTS_FILETYPE_IMAGE, SAVVIHUB_PLOTS_FILETYPE_IMAGES):
            print(f'validation_data:{self.validation_data}')
            print(f'validation_data type: {type(self.validation_data)}')
            print(f'model: {self.model}')
