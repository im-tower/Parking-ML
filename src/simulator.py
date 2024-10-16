import arcade
from car import Car
from cell import Cell, ParkingLot
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Simulator"
SIMULATION_SPEED = 0.01


class Window(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        


    def setup(self):
        self.next_update_time = 0
        self.cells = []
        self.load_map()
        self.car = Car(arcade, self.cells[0])
        # Show all possible paths to all cells
        paths = []
        for cell in self.cells:
            paths.append(Cell.path_between(self.car.cell, cell))
        paths.sort(key=len, reverse=True)
        paths = paths[:3]
        select = random.randint(0, 2)
        self.car.set_path(paths[select])
    def on_draw(self):
        self.clear()
        # Code to draw the screen goes here
        for cell in self.cells:
            cell.draw()
        self.car.draw()

    def on_update(self, delta_time):
        # Code to update the screen goes here
        if self.next_update_time > 0:
            self.next_update_time -= delta_time
            return
        self.next_update_time = SIMULATION_SPEED
        self.car.move()


    def load_map(self):
        grid = []
        for i in range(SCREEN_WIDTH // 20):
            grid.append([])
            for j in range(SCREEN_HEIGHT // 20):
                grid[i].append(Cell(arcade, i * 20 + 10, j * 20 + 10, temporal=True))
        with open("map.sim", "r") as f:
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
                self.cells.append(grid[int(i)][int(j)])
                grid[int(i)][int(j)].save()


def main():
    """Main function"""
    window = Window()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()