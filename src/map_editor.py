import arcade
import random
import os
import tkinter as tk
from tkinter import filedialog
# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Map Editor"
SIMULATION_SPEED = 1

GRID_SIZE = 20


class Window(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


    def setup(self):
        # define empty grid
        self.brush = None
        self.grid = []
        self.prev_selected = None
        self.shape_list = arcade.shape_list.ShapeElementList()
        for i in range(SCREEN_WIDTH // GRID_SIZE):
            self.grid.append([])
            for j in range(SCREEN_HEIGHT // GRID_SIZE):
                shape = arcade.shape_list.create_rectangle_outline(i * GRID_SIZE + GRID_SIZE/2, j * GRID_SIZE+GRID_SIZE/2, GRID_SIZE, GRID_SIZE, arcade.color.WHITE)
                self.grid[i].append({
                    "shape" : shape,
                    "color" : arcade.color.WHITE,
                    "direction" : None
                })
                self.shape_list.append(shape)
        # Llamar a la función de importación al iniciar
        self.import_map()

        
    def on_draw(self):
        self.clear()
        # Code to draw the screen goes here
        # Draw grid with an outline
        self.shape_list.draw()


    def on_update(self, delta_time):
        # Code to update the screen goes here
        pass


    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        super().on_key_release(symbol, modifiers)
        if symbol == arcade.key.RIGHT:
            self.brush = arcade.color.RED
        elif symbol == arcade.key.LEFT:
            self.brush = arcade.color.BLUE
        elif symbol == arcade.key.UP:
            self.brush = arcade.color.GREEN
        elif symbol == arcade.key.DOWN:
            self.brush = arcade.color.YELLOW
        elif symbol == arcade.key.ENTER:
            self.brush = arcade.color.PURPLE
        elif symbol == arcade.key.P:
            self.brush = arcade.color.PINK
        elif symbol == arcade.key.DELETE:
            self.brush = arcade.color.WHITE
        elif symbol == arcade.key.SPACE:
            self.brush = None
        elif symbol == arcade.key.E:
            self.export()
        elif symbol == arcade.key.I:  # Presiona 'I' para importar un archivo
            self.import_map()
        elif symbol == arcade.key.S: # Casilla de Spawn
            self.brush = arcade.color.ORANGE

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if self.brush:
            i = x // GRID_SIZE
            j = y // GRID_SIZE
            if self.grid[i][j]["color"] == self.brush:
                return
            if self.grid[i][j]["shape"] not in self.shape_list:
                return
            self.grid[i][j]["color"] = self.brush
            self.shape_list.remove(self.grid[i][j]["shape"])
            new_shape = arcade.shape_list.create_rectangle_outline(i * GRID_SIZE + GRID_SIZE/2, j * GRID_SIZE + GRID_SIZE/2, GRID_SIZE, GRID_SIZE, self.brush)
            self.shape_list.append(new_shape)
            self.grid[i][j]["shape"] = new_shape
            if self.brush == arcade.color.RED:
                self.grid[i][j]["direction"] = "right"
            elif self.brush == arcade.color.BLUE:
                self.grid[i][j]["direction"] = "left"
            elif self.brush == arcade.color.GREEN:
                self.grid[i][j]["direction"] = "up"
            elif self.brush == arcade.color.YELLOW:
                self.grid[i][j]["direction"] = "down"
            elif self.brush == arcade.color.PURPLE:
                self.grid[i][j]["direction"] = "intersection"
            elif self.brush == arcade.color.PINK:
                self.grid[i][j]["direction"] = "parking"
            elif self.brush == arcade.color.ORANGE:
                self.grid[i][j]["direction"] = "spawn"
            else:
                self.grid[i][j]["direction"] = None

        return super().on_mouse_release(x, y, button, modifiers)
    
    def export(self):
        # Crear la carpeta "parking" si no existe
        directory = "parking"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Encuentra el siguiente número de archivo disponible dentro de la carpeta
        num = 1
        while os.path.exists(f"{directory}/map_{num}.sim"):
            num += 1

        filename = f"{directory}/map_{num}.sim"
        
        with open(filename, "wb") as f:
            for i in range(SCREEN_WIDTH // GRID_SIZE):
                for j in range(SCREEN_HEIGHT // GRID_SIZE):
                    if self.grid[i][j]["color"] != arcade.color.WHITE:
                        f.write(f"{i} {j} {self.grid[i][j]['direction']}\n".encode())
        
        print(f"Map exported as {filename}")
    
    def import_map(self):
        # Crear una ventana de diálogo para seleccionar un archivo
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        file_path = filedialog.askopenfilename(filetypes=[("Simulation Files", "*.sim")])

        if not file_path:
            print("No file selected")
            return

        try:
            # Limpiar la cuadrícula y la lista de formas antes de cargar un nuevo mapa
            self.shape_list = arcade.shape_list.ShapeElementList()
            for i in range(SCREEN_WIDTH // GRID_SIZE):
                for j in range(SCREEN_HEIGHT // GRID_SIZE):
                    self.grid[i][j]["color"] = arcade.color.WHITE
                    self.grid[i][j]["direction"] = None
                    shape = arcade.shape_list.create_rectangle_outline(
                        i * GRID_SIZE + GRID_SIZE / 2, j * GRID_SIZE + GRID_SIZE / 2, GRID_SIZE, GRID_SIZE, arcade.color.WHITE
                    )
                    self.grid[i][j]["shape"] = shape
                    self.shape_list.append(shape)

            # Leer y cargar el contenido del archivo seleccionado
            with open(file_path, "r") as f:
                for line in f:
                    i, j, direction = line.strip().split()
                    i, j = int(i), int(j)

                    # Actualizar la celda con la dirección importada
                    if direction == "right":
                        self.brush = arcade.color.RED
                    elif direction == "left":
                        self.brush = arcade.color.BLUE
                    elif direction == "up":
                        self.brush = arcade.color.GREEN
                    elif direction == "down":
                        self.brush = arcade.color.YELLOW
                    elif direction == "intersection":
                        self.brush = arcade.color.PURPLE
                    elif direction == "parking":
                        self.brush = arcade.color.PINK
                    else:
                        self.brush = arcade.color.WHITE

                    # Actualizar color y dirección en la celda
                    self.grid[i][j]["color"] = self.brush
                    self.grid[i][j]["direction"] = direction

                    # Crear un nuevo shape y actualizarlo directamente
                    new_shape = arcade.shape_list.create_rectangle_outline(
                        i * GRID_SIZE + GRID_SIZE / 2, j * GRID_SIZE + GRID_SIZE / 2, GRID_SIZE, GRID_SIZE, self.brush
                    )
                    self.grid[i][j]["shape"] = new_shape
                    self.shape_list.append(new_shape)

            print(f"Map imported from {file_path}")

        except Exception as e:
            print(f"Error importing map: {e}")





def main():
    """Main function"""
    window = Window()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()