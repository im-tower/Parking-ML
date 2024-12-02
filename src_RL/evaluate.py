import gym
import time
from parking_env import ParkingEnv
from stable_baselines3 import DQN

def main():
    env = ParkingEnv(num_vehicles=3, num_targets=3)

    # Cargar el modelo entrenado
    model = DQN.load("dqn_parking", env=env)

    # Número de episodios a evaluar
    num_episodes = 10
    total_rewards = []

    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0

        print(f"--- Episodio {episode + 1} ---")
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            env.render()
            time.sleep(0.2)  # Pausa para visualizar

        total_rewards.append(episode_reward)
        print(f"Recompensa total del episodio {episode + 1}: {episode_reward}")

    # Calcular estadísticas
    mean_reward = sum(total_rewards) / num_episodes
    print(f"\nRecompensa promedio en {num_episodes} episodios: {mean_reward}")
    print(f"Recompensas por episodio: {total_rewards}")

    env.close()

if __name__ == "__main__":
    main()