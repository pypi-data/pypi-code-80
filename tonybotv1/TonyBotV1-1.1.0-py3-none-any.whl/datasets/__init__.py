from .utils import load_dataset as _load_dataset

GU_1H_ASK = _load_dataset('GBPUSD60', 'Time', '2020-02-03', '2020-05-03', 36)
GU_15M_ASK = _load_dataset('GBPUSD15', 'Time', '2020-02-03', '2020-05-03', 36)