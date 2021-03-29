from gym.envs.registration import register


register(
    id = 'basic-TicTacToe-v0',
    entry_point='tail_envs.tictactoe.BasicTicTacToe:BasicTicTacToeEnv',
    max_episode_steps= 10
)