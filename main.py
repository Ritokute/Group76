import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2433042_2312763_2211199_2211299_2213444.policy2433042_2312763_2211199_2211299_2213444 import Policy2433042_2312763_2211199_2211299_2213444

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 100

if __name__ == "__main__":
    # Reset the environment
    observation, info = env.reset(seed=42)

    # Test GreedyPolicy
    gd_policy = GreedyPolicy()
    ep = 0
    while ep < NUM_EPISODES:
        action = gd_policy.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            print(info)
            observation, info = env.reset(seed=ep)
            ep += 1

    # Reset the environment
    observation, info = env.reset(seed=42)

    # Test RandomPolicy
    rd_policy = RandomPolicy()
    ep = 0
    while ep < NUM_EPISODES:
        action = rd_policy.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            print(info)
            observation, info = env.reset(seed=ep)
            ep += 1

    # Uncomment the following code to test your policy
    # # Reset the environment
    observation, info = env.reset(seed=42)
    print(info)

    policy2433042_2312763_2211199_2211299_2213444 = Policy2433042_2312763_2211199_2211299_2213444(policy_id=1)
    for _ in range(200):
        action = policy2433042_2312763_2211199_2211299_2213444.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)
        print(info)

        if terminated or truncated:
            observation, info = env.reset()

env.close()
