import arcade
from cell import Cell, ParkingLot, SpawnCell, ExitCell
from car import Car
from timer import Timer
import random
import math
import tkinter as tk
from tkinter import filedialog

from controller import NearestParkingAvailableController

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Simulator"
SIMULATION_SPEED = 0.1
LAMBDA_CARS = 1/3 # 1 car every 3 ticks.


class Window(arcade.Window):

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.average_search_time = 0
        self.average_pollution = 0
        self.grid = []  # Inicializamos self.grid como una lista vacía
        self.cells = []  # Inicializamos self.cells también aquí
        self.exit_cells = []  # Inicializamos self.exit_cells aquí

    def setup(self):
        self.next_update_time = 0
        self.cells = []
        self.load_map()
        self.cars = []
        self.spawn_cells = [cell for cell in self.cells if isinstance(cell, SpawnCell)]
        self.parking_lots = [cell for cell in self.cells if isinstance(cell, ParkingLot)]
        self.controller = NearestParkingAvailableController(self)
        self.total_Search_time = 0
        self.total_pollution = 0
        self.timer_spawn = Timer(random.expovariate(LAMBDA_CARS))
        self.arrival_times = []
        self.exit_cells = [cell for cell in self.cells if isinstance(cell, ExitCell)]  # Asigna exit_cells después de cargar el mapa

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

    def on_update(self, delta_time):
        if self.next_update_time > 0:
            self.next_update_time -= delta_time
            return

        # Temporizador para spawn de autos
        if self.timer_spawn.update(1):
            self.timer_spawn.reset(round(random.expovariate(LAMBDA_CARS)))
            self.arrival_times.append(self.timer_spawn.time)
            available_spawns = [cell for cell in self.spawn_cells if cell.available]
            if len(available_spawns) > 0:
                select = random.randint(0, len(available_spawns) - 1)
                spawn_cell = available_spawns[select]  # Usar available_spawns en lugar de self.spawn_cells
                self.cars.append(spawn_cell.spawn_car())

        # Actualiza el controlador y los movimientos
        self.controller.update()
        self.next_update_time = SIMULATION_SPEED
        for car in self.cars:
            car.move()

        # Eliminar autos que han llegado a una salida
        cars_to_remove = []
        for car in self.cars:
            if isinstance(car.cell, ExitCell) and len(car.path) == 0:  # Solo remover si ha terminado su path
                cars_to_remove.append(car)
                if car.parking_lot:
                    car.parking_lot.reserved = False
                    car.parking_lot.available = True

        for car in cars_to_remove:
            self.cars.remove(car)



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
                    elif direction == 'exit':
                        grid[int(i)][int(j)] = ExitCell(arcade, int(i) * 20 + 10, int(j) * 20 + 10)
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) + 1])
                        grid[int(i)][int(j)].connect(grid[int(i)][int(j) - 1])
                        grid[int(i)][int(j)].connect(grid[int(i) - 1][int(j)])
                        grid[int(i)][int(j)].connect(grid[int(i) + 1][int(j)])
                    self.cells.append(grid[int(i)][int(j)])
                    grid[int(i)][int(j)].save()
        except Exception as e:
            print(f"Error loading map: {e}")

def plot_histogram(arrival_times):
    import matplotlib.pyplot as plt
    plt.hist(arrival_times, bins=4)
    plt.xlabel("Ticks")
    plt.ylabel("Number of cars")
    plt.title("Arrival times")
    plt.show()

def main():
    """Función principal"""
    window = Window()
    window.setup()
    arcade.run()
    plot_histogram(window.arrival_times)


if __name__ == "__main__":
    main()
