from gym.envs.registration import register

register(
    id='chefshat',
    entry_point='ChefsHatGym.env.ChefsHatEnv:ChefsHatEnv',
)