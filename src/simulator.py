import arcade
from cell import Cell, ParkingLot, SpawnCell
from car import Car
import random
import tkinter as tk
from tkinter import filedialog

from controller import NearestParkingAvailableController

import random
import matplotlib.pyplot as plt

import math
# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Simulator"
SIMULATION_SPEED = 0.7


class Window(arcade.Window):

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.average_search_time = 0
        self.average_pollution = 0
        self.car_count = 0  # Contador de coches

        # Atributos inicializados en setup
        self.arrival_timer = 0  # Tiempo acumulado
        self.next_arrival_time = 0  # Tiempo hasta la próxima llegada
        self.arrival_times = []  # Lista para almacenar los tiempos entre llegadas
        self.service_times = []  # Lista para almacenar los tiempos de servicio
        
    def setup(self):
        self.next_update_time = 0
        self.cells = []
        self.load_map()
        self.car = Car(arcade, self.cells[0])
        self.car_count += 1  # Incrementar el contador de coches
        self.cars = [self.car]
        self.spawn_cells = [cell for cell in self.cells if isinstance(cell, SpawnCell)]
        self.parking_lots = [cell for cell in self.cells if isinstance(cell, ParkingLot)]
        self.controller = NearestParkingAvailableController(self)
        self.total_Search_time = 0
        self.total_pollution = 0

        # Inicializar temporizador
        self.arrival_timer = 0
        self.next_arrival_time = self.get_next_arrival_time()

    def on_draw(self):
        self.clear()
        # Dibujar las celdas y el coche
        for cell in self.cells:
            cell.draw()
        for car in self.cars:
            car.draw()

        # Dibujar la información en la columna derecha
        self.draw_info()

    def draw_info(self):
        # Calcular promedios
        car_count = len(self.cars)
    
    # Calcular el tiempo de búsqueda promedio y la contaminación promedio
        if car_count > 0:
            total_search_time = sum(car.search_time for car in self.cars)
            total_pollution = sum(car.pollution for car in self.cars)
            
            self.average_search_time = total_search_time / car_count
            self.average_pollution = total_pollution / car_count
        else:
            self.average_search_time = 0
            self.average_pollution = 0

        # Definir posición y tamaño del recuadro
        box_x = SCREEN_WIDTH - 220
        box_y = SCREEN_HEIGHT - 100
        box_width = 220
        box_height = 90

        # Dibujar el borde negro (rectángulo más grande)
        #arcade.draw_lrbt_rectangle_filled(box_y, box_y + box_height, box_x, box_x + box_width, arcade.color.BLACK)
        # Dibujar el recuadro blanco (rectángulo más pequeño)
        arcade.draw_lrbt_rectangle_filled(
            left=box_x,
            right=box_x + box_width,
            top=box_y + box_height,
            bottom=box_y,
            color=arcade.color.WHITE
        )

        
        # Mostrar la información
        arcade.draw_text(f"Tiempo de búsqueda promedio: {self.average_search_time:.2f}", 
                         box_x +5, box_y + 50, arcade.color.BLACK, 11)
        arcade.draw_text(f"Contaminación promedio: {self.average_pollution:.2f}", 
                         box_x +5, box_y + 30, arcade.color.BLACK, 11)

    def get_next_arrival_time(self):
        """
        Genera el tiempo hasta la próxima llegada de coche con una distribución exponencial.
        """
        lambda_rate = 1 / 0.5  # Tasa de llegada: 1 coche cada 0.5 segundos
        return -math.log(1 - random.random()) / lambda_rate

    def on_update(self, delta_time):
        # Asegurarse de que los temporizadores estén inicializados
        if self.arrival_timer is None or self.next_arrival_time is None:
            self.setup()

        # Actualizar la pantalla y el contador de tiempo
        if self.next_update_time > 0:
            self.next_update_time -= delta_time
            return
        self.controller.update()

        # Incrementar el contador de tiempo de llegada
        self.arrival_timer += delta_time

        print(f"Tiempo acumulado: {self.arrival_timer:.2f} segundos")

        # Verificar si el tiempo acumulado ha superado el siguiente tiempo de llegada
        if self.arrival_timer >= self.next_arrival_time:
            available_spawns = [cell for cell in self.spawn_cells if cell.available]
            if available_spawns:
                # Generar un nuevo coche en una celda de spawn disponible
                selected_spawn = random.choice(available_spawns)
                new_car = selected_spawn.spawn_car()
                self.cars.append(new_car)
                self.car_count += 1
                print(f"Car {self.car_count} spawned")
            else:
                print("No hay espacio disponible para un nuevo vehículo.")

            # Reiniciar el temporizador y calcular el tiempo para la siguiente llegada
            self.arrival_timer = 0
            self.next_arrival_time = self.get_next_arrival_time()

            print(f"Nuevo tiempo de llegada: {self.next_arrival_time:.2f} segundos")

        # Actualizar el tiempo de la próxima actualización y mover los autos
        self.next_update_time = SIMULATION_SPEED
        for car in self.cars:
            car.move()
    
    # Función para graficar los histogramas
    @staticmethod
    def plot_histograms(arrival_times, service_times):
        plt.figure(figsize=(12, 5))

        # Histograma de tiempos entre llegadas
        plt.subplot(1, 2, 1)
        plt.hist(arrival_times, bins=20, color='blue', alpha=0.7)
        plt.title('Histograma de Tiempos entre Llegadas')
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Frecuencia')

        # Histograma de tiempos de servicio
        plt.subplot(1, 2, 2)
        plt.hist(service_times, bins=20, color='green', alpha=0.7)
        plt.title('Histograma de Tiempos de Servicio')
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Frecuencia')

        plt.tight_layout()
        plt.show()

    def load_map(self):
        # Crear una ventana de diálogo para seleccionar un archivo
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        file_path = filedialog.askopenfilename(filetypes=[("Simulation Files", "*.sim")])

        if not file_path:
            print("No file selected")
            return

        # Crear la cuadrícula de celdas
        grid = []
        for i in range(SCREEN_WIDTH // 20):
            grid.append([])
            for j in range(SCREEN_HEIGHT // 20):
                grid[i].append(Cell(arcade, i * 20 + 10, j * 20 + 10, temporal=True))

        # Cargar el mapa desde el archivo seleccionado
        try:
            with open(file_path, "r") as f:
                for line in f:
                    i, j, direction = line.strip().split()
                    if direction == 'up':
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) + 1])
                    elif direction == 'down':
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) - 1])
                    elif direction == 'left':
                        grid[int(i)][int(j)].connect(grid[int(i) - 1][int(j)])
                    elif direction == 'right':
                        grid[int(i)][int(j)].connect(grid[int(i) + 1][int(j)])
                    elif direction == 'intersection':
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) + 1])
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) - 1])
                        grid[int(i)][int(j)].connect(grid[int(i) - 1][int(j)])
                        grid[int(i)][int(j)].connect(grid[int(i) + 1][int(j)])
                    elif direction == 'parking':
                        grid[int(i)][int(j)] = ParkingLot(arcade, int(i) * 20 + 10, int(j) * 20 + 10)
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) + 1])
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) - 1])
                        grid[int(i)][int(j)].connect(grid[int(i) - 1][int(j)])
                        grid[int(i)][int(j)].connect(grid[int(i) + 1][int(j)])
                    elif direction == 'spawn':
                        grid[int(i)][int(j)] = SpawnCell(arcade, int(i) * 20 + 10, int(j) * 20 + 10)
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) + 1])
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) - 1])
                        grid[int(i)][int(j)].connect(grid[int(i) - 1][int(j)])
                        grid[int(i)][int(j)].connect(grid[int(i) + 1][int(j)])
                    self.cells.append(grid[int(i)][int(j)])
                    grid[int(i)][int(j)].save()
        except Exception as e:
            print(f"Error loading map: {e}")


def main():
    """Función principal"""
    window = Window()
    window.setup()
    arcade.run()
    # Al final de la simulación, o cuando quieras visualizar los histogramas
    Window.plot_histograms(window.arrival_timer, window.service_times)


if __name__ == "__main__":
    main()