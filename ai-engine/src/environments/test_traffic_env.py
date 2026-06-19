from src.environments.traffic_env import TrafficEnv


def main():
    env = TrafficEnv(max_steps=120)

    obs, info = env.reset()

    print("Estado inicial:")
    print(obs)
    print(info)

    total_reward = 0

    for step in range(120):
        action = env.action_space.sample()

        obs, reward, terminated, truncated, info = env.step(action)

        total_reward += reward

        print("-" * 60)
        print(f"Step: {step + 1}")
        print(f"Action: {action}")
        print(f"Observation: {obs}")
        print(f"Reward: {reward}")
        print(f"Terminated: {terminated}")
        print(f"Truncated: {truncated}")
        print(f"Info: {info}")

        if terminated or truncated:
            break

    env.close()

    print("=" * 60)
    print(f"Total reward: {total_reward}")


if __name__ == "__main__":
    main()