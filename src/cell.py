
class Cell:
    size = 20
    id = 0
    cells = []
    def __init__(self, arcade, x, y) -> None:
        self.arcade = arcade
        self.x = x
        self.y = y
        self.adjacent_cells = []
        self.id = Cell.id
        Cell.id += 1
        self.available = True
        self.color = self.arcade.color.WHITE
        Cell.cells.append(self)
    
    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)

    def connect(self, cell):
        return self.adjacent_cells.append(cell)
    
    def __repr__(self) -> str:
        return f'Cell({self.x}, {self.y}, {self.id})'

    @classmethod
    def dijkstra(cls, source):
        """ Implement a Dijkstra algorithm to find the shortest path between two cells """
        distances = {cell: float('inf') for cell in Cell.cells}
        predecessor = {cell: None for cell in Cell.cells}  # Track previous cell for path reconstruction
        distances[source] = 0
        unvisited = set(Cell.cells)
        
        while unvisited:
            current = min(unvisited, key=lambda cell: distances[cell])
            unvisited.remove(current)
            
            for neighbor in current.adjacent_cells:
                if neighbor in unvisited:
                    new_distance = distances[current] + 1  # Assuming equal weights for simplicity
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessor[neighbor] = current  # Track the cell that leads to this one
        
        return distances, predecessor
    
    @classmethod
    def path_between(cls, source, target):
        """ Find the shortest path between two cells using Dijkstra """
        distances, predecessor = cls.dijkstra(source)
        path = []
        current = target
        
        # Rebuild the path by walking backwards from target to source
        while current is not None:
            path.append(current)
            current = predecessor[current]
        
        # Return the path from source to target
        path.reverse()
        path.pop(0)
        return [cell.id for cell in path]

    
class ParkingLot(Cell):
    size = 20
    def __init__(self, arcade, x, y) -> None:
        super().__init__(arcade, x, y)
        self.color = self.arcade.color.GREEN

    def draw(self):
        self.arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)