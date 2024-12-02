import gym
from parking_env import ParkingEnv
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy

def main():
    env = ParkingEnv(num_vehicles=3, num_targets=3)

    # Crear el agente DQN
    model = DQN('MlpPolicy', env, verbose=1, learning_rate=1e-3, buffer_size=10000,
                learning_starts=1000, batch_size=32, tau=1.0, gamma=0.99,
                train_freq=4, target_update_interval=1000, exploration_fraction=0.1,
                exploration_final_eps=0.02)

    # Entrenar el agente
    model.learn(total_timesteps=50000)

    # Guardar el modelo entrenado
    model.save("dqn_parking")

    env.close()

if __name__ == "__main__":
    main()