
class Cell:
    size = 20
    id = 0
    def __init__(self, arcade, x, y) -> None:
        self.arcade = arcade
        self.x = x
        self.y = y
        self.adjacent_cells = []
        self.id = Cell.id
        Cell.id += 1
        self.available = True
        self.color = self.arcade.color.WHITE
    
    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)

    def connect(self, cell):
        return self.adjacent_cells.append(cell)
    
class ParkingLot(Cell):
    size = 20
    def __init__(self, arcade, x, y) -> None:
        super().__init__(arcade, x, y)
        self.color = self.arcade.color.GREEN

    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)