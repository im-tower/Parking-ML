import random
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
        self.parking_timer = None  # Nuevo: Temporizador de estacionamiento
        self.parking_lot = None    # Referencia al ParkingLot donde está estacionado
        self.is_exiting = False     # indicar que está saliendo

    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.cell.x, self.cell.y, self.size, self.size, self.color)

    def set_path(self, path):
        self.path = path

    def move(self):
        if len(self.path) == 0:
            return
        
        self.search_time += 1 
        next_cell_id = self.path[0]
        next_cell = next((cell for cell in self.cell.adjacent_cells if cell.id == next_cell_id and cell.available), None)
        
        if next_cell:
            self.cell.available = True
            self.cell = next_cell
            self.path.pop(0)
            self.cell.available = False
            self.pollution += 1

            # Usar el tipo de celda en lugar de isinstance
            if self.cell.type == 'ParkingLot':
                self.color = self.arcade.color.GRAY
                self.parking_lot = self.cell
                self.parking_lot.reserved = True
                if self.parking_timer is None:
                    lambd = 1/100  # 10 segundos de promedio
                    self.parking_timer = int(random.expovariate(lambd))
            elif self.cell.type == 'ExitCell':
                self.is_exiting = True  # Indicar que el vehículo está saliendo
                self.color = self.arcade.color.GREEN
            else:
                if self.is_exiting:
                    self.color = self.arcade.color.RED  # Rojo si está saliendo
                else:
                    self.color = self.arcade.color.BLUE if not self.parking_timer else self.arcade.color.RED

    def update_parking_timer(self):
        if self.parking_timer is not None:
            self.parking_timer -= 1
            if self.parking_timer <= 0:
                return True  # Tiempo agotado, listo para salir
        return False