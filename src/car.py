from cell import Cell, ParkingLot
class Car:
    size = 20
    def __init__(self, arcade, cell) -> None:
        self.arcade = arcade
        self.cell = cell
        self.color = self.arcade.color.BLUE

    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.cell.x, self.cell.y, self.size, self.size, self.color)

    def set_path(self, path):
        self.path = path

    def move(self):
        for cell in self.cell.adjacent_cells:
            if cell.id == self.path[0] and cell.available:
                self.cell.available = True
                self.cell = cell
                self.path.pop(0)
                self.cell.available = False
                if type(self.cell) == ParkingLot:
                    self.color = self.arcade.color.GRAY
                break
                