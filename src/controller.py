from abc import ABC, abstractmethod
from cell import Cell
import arcade

class Controller:

    def __init__(self, simulation):
        self.simulation = simulation

    @abstractmethod
    def update(self):
        """ Update the simulation state. Route cars, control cars, etc. """
        pass


class NearestParkingAvailableController(Controller):
    def update(self):
        # Asigna parqueo si no tiene ruta y es azul
        not_assigned_cars = [car for car in self.simulation.cars 
                           if len(car.path) == 0 and car.color == arcade.color.BLUE]
        
        # Obtener lista de parqueos disponibles (no reservados)
        available_parkings = [parking for parking in self.simulation.parking_lots 
                            if not parking.reserved]

        for car in not_assigned_cars:
            if available_parkings:  # Solo buscar ruta si hay parqueos disponibles
                paths = []
                for parking in available_parkings:
                    path = Cell.path_between(car.cell, parking)
                    if path:  # Solo agregar si existe un camino válido
                        paths.append([path, parking])
                
                if paths:  # Si encontramos caminos válidos
                    paths.sort(key=lambda pair: len(pair[0]))  # Ordenar por longitud del camino
                    shortest_path, nearest_parking = paths[0]
                    car.set_path(shortest_path)
                    nearest_parking.reserved = True

        # Verifica temporizadores de autos estacionados y redirige a la salida
        parked_cars = [car for car in self.simulation.cars if car.color == arcade.color.GRAY]
        for car in parked_cars:
            if car.update_parking_timer():
                exit_paths = []
                for exit_cell in self.simulation.exit_cells:
                    exit_path = Cell.path_between(car.cell, exit_cell)
                    if exit_path:
                        exit_paths.append((exit_path, exit_cell))
                
                if exit_paths:
                    exit_paths.sort(key=lambda pair: len(pair[0]))
                    shortest_path, _ = exit_paths[0]
                    car.set_path(shortest_path)
                    car.color = arcade.color.RED
                    # Liberar el parqueo cuando el auto comienza a salir
                    if car.parking_lot:
                        car.parking_lot.reserved = False
                        car.parking_lot.available = True
                        car.parking_lot = None