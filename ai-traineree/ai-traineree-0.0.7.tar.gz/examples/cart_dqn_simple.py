from ai_traineree.agents.dqn import DQNAgent
from ai_traineree.env_runner import EnvRunner
from ai_traineree.tasks import GymTask
from ai_traineree.loggers import TensorboardLogger

import numpy as np
import pylab as plt
import torch


def run(
    reward_goal: float=100.0,
    max_episodes: int=2000,
    eps_start: float=1.0,
    eps_end: float=0.01,
    eps_decay: float=0.995,
):
    epsilon = eps_start
    mean_scores = []
    epsilons = []
    episode = 0

    while (episode < max_episodes):
        episode += 1
        score = 0
        state = task.reset()
        iterations = 0
        max_iterations = max_iterations if max_iterations is not None else max_iterations
        done = False

        while(iterations < max_iterations and not done):
            iterations += 1
            action = agent.act(state, eps)

            next_state, reward, done, _ = task.step(action)
            _rewards.append((iteration, reward))
            score += float(reward)

            agent.step(state, action, reward, next_state, done)
            # n -> n+1  => S(n) <- S(n+1)
            state = next_state

        mean_scores.append(sum(scores_window) / len(scores_window))
        epsilons.append(epsilon)

        epsilon = max(eps_end, eps_decay * epsilon)

        if mean_scores[-1] >= reward_goal and len(scores_window) == window_len:
            break

    return None


seed = 32167
# torch.set_deterministic(True)
torch.manual_seed(seed)
data_logger = TensorboardLogger()

env_name = 'CartPole-v1'
task = GymTask(env_name, seed=seed)
agent = DQNAgent(task.state_size, task.action_size, n_steps=5, seed=seed, device="cuda")
env_runner = EnvRunner(task, agent, data_logger=data_logger, seed=seed)

scores = env_runner.run(reward_goal=100, max_episodes=300, force_new=True, eps_decay=0.99, gif_every_episodes=5)
env_runner.interact_episode(render=True)

# plot the scores
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.arange(len(scores)), scores)
plt.ylabel('Score')
plt.xlabel('Episode #')
plt.savefig(f'{env_name}.png', dpi=120)
plt.show()
