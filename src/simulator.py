import arcade
from cell import Cell, ParkingLot, SpawnCell
from car import Car
import random
import tkinter as tk
from tkinter import filedialog

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

    def setup(self):
        self.next_update_time = 0
        self.cells = []
        self.load_map()
        self.car = Car(arcade, self.cells[0])
        self.car_count += 1  # Incrementar el contador de coches
        # Show all possible paths to all cells
        paths = []
        for cell in self.cells:
            paths.append(Cell.path_between(self.car.cell, cell))
        paths.sort(key=len, reverse=True)
        paths = paths[:3]
        select = random.randint(0, 2)
        self.car.set_path(paths[select])
        parking = None
        for cell in self.cells:
            if isinstance(cell, ParkingLot):
                parking = cell
                break
        self.car.set_path(Cell.path_between(self.car.cell, parking))
        self.cars = [self.car]
        self.spawn_cells = [cell for cell in self.cells if isinstance(cell, SpawnCell)]

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
        if self.car_count > 0:
            self.average_search_time = self.car.search_time / self.car_count
            self.average_pollution = self.car.pollution / self.car_count

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
        # Actualizar la pantalla
        if self.next_update_time > 0:
            self.next_update_time -= delta_time
            return
        if random.randint(1,2) == 1:
            available_spawns = [cell for cell in self.spawn_cells if cell.available]
            if len(available_spawns) > 0:
                select = random.randint(0, len(available_spawns) - 1)
                self.cars.append(self.spawn_cells[select].spawn_car())
                print(f"Car {self.car_count} spawned")
        self.next_update_time = SIMULATION_SPEED
        for car in self.cars:
            car.move()

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


if __name__ == "__main__":
    main()