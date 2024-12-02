import gym
from gym import spaces
import numpy as np
import pygame
import random

class ParkingEnv(gym.Env):
    """
    Entorno personalizado de Gym que simula un estacionamiento de múltiples vehículos con múltiples salidas.
    Un solo agente controla todos los vehículos de forma secuencial.
    Observación: Distancias en pasos desde las casillas adyacentes al objetivo más cercano para el vehículo actual.
    """

    def __init__(self, num_vehicles=3, num_targets=3):
        super(ParkingEnv, self).__init__()

        # Definir la cuadrícula del estacionamiento
        self.grid_size = (10, 10)  # 30x30 cuadrícula
        self.max_steps = 100
        self.current_step = 0
        self.num_vehicles = num_vehicles  # Número de vehículos
        self.num_targets = num_targets  # Número de salidas (metas)
        self.current_vehicle = 0  # Índice del vehículo actual que está siendo controlado

        # Acciones: 0=Arriba, 1=Abajo, 2=Izquierda, 3=Derecha
        self.action_space = spaces.Discrete(4)

        # Observación: [distancia_arriba, distancia_abajo, distancia_izquierda, distancia_derecha]
        # Distancias en pasos al objetivo más cercano desde las casillas adyacentes del vehículo actual
        self.observation_space = spaces.Box(
            low=0,
            high=self.grid_size[0] + self.grid_size[1],
            shape=(4,),
            dtype=np.float32
        )

        # Inicialización de Pygame para la renderización
        pygame.init()
        self.screen = None
        self.cell_size = 50
        self.screen_width = self.grid_size[0] * self.cell_size
        self.screen_height = self.grid_size[1] * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simulación de Estacionamiento con Múltiples Vehículos y Salidas")

        self.reset()

    def reset(self):
        """
        Reinicia el entorno a un estado inicial.
        """
        # Reiniciar las posiciones de los vehículos
        self.vehicle_positions = []
        for _ in range(self.num_vehicles):
            while True:
                pos = [random.randint(0, self.grid_size[0] - 1), random.randint(0, self.grid_size[1] - 1)]
                if pos not in self.vehicle_positions:
                    self.vehicle_positions.append(pos)
                    break

        # Generar nuevas posiciones aleatorias para las salidas
        self.target_positions = []
        for _ in range(self.num_targets):
            while True:
                target = [random.randint(0, self.grid_size[0] - 1), random.randint(0, self.grid_size[1] - 1)]
                if target not in self.vehicle_positions and target not in self.target_positions:
                    self.target_positions.append(target)
                    break

        self.current_step = 0
        self.current_vehicle = 0  # Reiniciar al primer vehículo
        self.parked_vehicles = []  # Lista de vehículos estacionados
        return self._get_obs()

    def _manhattan_distance(self, pos1, pos2):
        """
        Calcula la distancia de Manhattan entre dos posiciones en la cuadrícula.
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _get_closest_target_distance(self, position):
        """
        Calcula la distancia de Manhattan al objetivo más cercano desde una posición dada.
        """
        if not self.target_positions:
            return self.grid_size[0] + self.grid_size[1]
        return min(self._manhattan_distance(position, target) for target in self.target_positions)

    def _count_nearby_vehicles(self, position, radius=1):
        """
        Cuenta cuántos vehículos están cerca de una posición dada dentro de un radio especificado.
        """
        count = 0
        for vehicle in self.vehicle_positions:
            if vehicle != position:  # No contar el vehículo actual
                distance = abs(vehicle[0] - position[0]) + abs(vehicle[1] - position[1])  # Distancia de Manhattan
                if distance <= radius:
                    count += 1
        return count

    def _get_obs(self):
        """
        Obtiene la observación actual del entorno para el vehículo actual.
        """
        # Si el vehículo actual está estacionado, devolver una observación nula
        if self.current_vehicle in self.parked_vehicles:
            return np.array([self.grid_size[0] + self.grid_size[1]] * 4, dtype=np.float32)

        vehicle_x, vehicle_y = self.vehicle_positions[self.current_vehicle]

        # Calcular las distancias en pasos desde las casillas adyacentes al objetivo más cercano
        distances = []

        # Arriba
        if vehicle_y < self.grid_size[1] - 1:
            distances.append(self._get_closest_target_distance([vehicle_x, vehicle_y + 1]))
        else:
            distances.append(self.grid_size[0] + self.grid_size[1])  # Valor máximo si está fuera de la cuadrícula

        # Abajo
        if vehicle_y > 0:
            distances.append(self._get_closest_target_distance([vehicle_x, vehicle_y - 1]))
        else:
            distances.append(self.grid_size[0] + self.grid_size[1])

        # Izquierda
        if vehicle_x > 0:
            distances.append(self._get_closest_target_distance([vehicle_x - 1, vehicle_y]))
        else:
            distances.append(self.grid_size[0] + self.grid_size[1])

        # Derecha
        if vehicle_x < self.grid_size[0] - 1:
            distances.append(self._get_closest_target_distance([vehicle_x + 1, vehicle_y]))
        else:
            distances.append(self.grid_size[0] + self.grid_size[1])

        return np.array(distances, dtype=np.float32)

    def step(self, action):
        """
        Aplica una acción al vehículo actual y actualiza el estado del entorno.
        """
        self.current_step += 1
        done = False
        reward = -1  # Penalización por paso

        # Si el vehículo actual ya está estacionado, pasar al siguiente vehículo
        if self.current_vehicle in self.parked_vehicles:
            self.current_vehicle = (self.current_vehicle + 1) % self.num_vehicles
            return self._get_obs(), reward, done, {}

        # Guardar la distancia anterior al objetivo más cercano
        previous_distance = self._get_closest_target_distance(self.vehicle_positions[self.current_vehicle])

        # Aplicar acción al vehículo actual
        if action == 0 and self.vehicle_positions[self.current_vehicle][1] < self.grid_size[1] - 1:  # Arriba
            self.vehicle_positions[self.current_vehicle][1] += 1
        elif action == 1 and self.vehicle_positions[self.current_vehicle][1] > 0:  # Abajo
            self.vehicle_positions[self.current_vehicle][1] -= 1
        elif action == 2 and self.vehicle_positions[self.current_vehicle][0] > 0:  # Izquierda
            self.vehicle_positions[self.current_vehicle][0] -= 1
        elif action == 3 and self.vehicle_positions[self.current_vehicle][0] < self.grid_size[0] - 1:  # Derecha
            self.vehicle_positions[self.current_vehicle][0] += 1
        else:
            # Acción inválida
            reward += -5  # Penalización adicional

        # Calcular la nueva distancia al objetivo más cercano
        current_distance = self._get_closest_target_distance(self.vehicle_positions[self.current_vehicle])

        # Recompensa por moverse a una casilla con menor distancia al objetivo más cercano
        if current_distance < previous_distance:
            reward += 10  # Recompensa por acercarse
        elif current_distance > previous_distance:
            reward -= 10  # Penalización por alejarse

        # Penalización por estar cerca de otros vehículos
        nearby_vehicles = self._count_nearby_vehicles(self.vehicle_positions[self.current_vehicle], radius=3)
        if nearby_vehicles > 0:
            reward -= 5 * nearby_vehicles  # Penalización proporcional al número de vehículos cercanos

        # Verificar si el vehículo alcanzó alguna de las salidas
        if self.vehicle_positions[self.current_vehicle] in self.target_positions:
            reward += 200  # Gran recompensa por alcanzar una salida
            self.target_positions.remove(self.vehicle_positions[self.current_vehicle])  # Eliminar la meta alcanzada
            self.parked_vehicles.append(self.current_vehicle)  # Marcar el vehículo como estacionado

        # Cambiar al siguiente vehículo
        self.current_vehicle = (self.current_vehicle + 1) % self.num_vehicles

        # Verificar si excedió el número máximo de pasos o si todas las metas fueron alcanzadas
        if self.current_step >= self.max_steps or len(self.target_positions) == 0:
            done = True

        return self._get_obs(), reward, done, {}

    def render(self, mode='human'):
        """
        Renderiza el entorno utilizando Pygame.
        """
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Simulación de Estacionamiento con Múltiples Vehículos y Salidas")

        # Manejar eventos de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Dibujar cuadrícula
        self.screen.fill((255, 255, 255))  # Fondo blanco
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(x * self.cell_size, (self.grid_size[1] - 1 - y) * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)  # Líneas de la cuadrícula

        # Dibujar salidas
        for target in self.target_positions:
            target_rect = pygame.Rect(target[0] * self.cell_size,
                                      (self.grid_size[1] - 1 - target[1]) * self.cell_size,
                                      self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 255, 0), target_rect)  # Salidas en verde

        # Dibujar vehículos
        for i, vehicle in enumerate(self.vehicle_positions):
            color = (0, 0, 255) if i not in self.parked_vehicles else (128, 128, 128)  # Azul si no está estacionado, gris si lo está
            vehicle_rect = pygame.Rect(vehicle[0] * self.cell_size,
                                       (self.grid_size[1] - 1 - vehicle[1]) * self.cell_size,
                                       self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, vehicle_rect)  # Vehículos

        pygame.display.flip()

    def close(self):
        """
        Cierra la ventana de renderizado.
        """
        if self.screen:
            pygame.quit()
            self.screen = None