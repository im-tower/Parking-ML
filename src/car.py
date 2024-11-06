class Car:
    size = 20
    def __init__(self, arcade, cell) -> None:
        self.arcade = arcade
        self.cell = cell
        self.cell.available = False
        self.color = self.arcade.color.BLUE
        self.pollution = 0
        self.search_time = 0
        self.path = []

    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.cell.x, self.cell.y, self.size, self.size, self.color)

    def set_path(self, path):
        self.path = path

    def move(self):
        if len(self.path) == 0:
            return
        
        # Incrementa el tiempo de búsqueda por cada intento de movimiento
        self.search_time += 1 
        
        for cell in self.cell.adjacent_cells:
            if cell.id == self.path[0] and cell.available:
                self.cell.available = True
                self.cell = cell
                self.path.pop(0)
                self.cell.available = False
                if type(self.cell.type) == 'ParkingLot':
                    self.color = self.arcade.color.GRAY
                break
        self.pollution += 1

    
