from gym.envs.registration import register
from copy import deepcopy
from . import datasets

register(
    id='TonyBotV1-v0',
    entry_point='TonyBotV1.envs:TradingEnv',
    kwargs={
        'df1': deepcopy(datasets.GU_1H_ASK),
        'df15': deepcopy(datasets.GU_15M_ASK),
        'window_size': 36,
        'max_loss': 0.8,
        'max_profit': 4,
        'stoploss': 0.0025,
        'takeprofit': 0.0040,
        'slipping': 0.0003,
        'image_size': 36,
        'image_count': 16,
        'frame_bound': (36, len(datasets.GU_15M_ASK))
    }
)