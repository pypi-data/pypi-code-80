import warnings

from forecastflow.satellite.tableau import prep

warnings.filterwarnings("once", category=DeprecationWarning, module=__name__)


def __getattr__(name):
    if name in ['PrepType', 'make_prediction_schema']:
        warnings.warn(
            f'{__name__} is deprecated, use {prep.__name__} instead.',
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(prep, name)
    else:
        raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
