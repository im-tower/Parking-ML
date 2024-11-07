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
        not_assigned_cars = [car for car in self.simulation.cars if len(car.path) == 0 and car.color == arcade.color.BLUE]
        for car in not_assigned_cars:
            # Calculate all possible paths to parking lots
            paths = []
            for parking in self.simulation.parking_lots:
                paths.append([Cell.path_between(car.cell, parking), parking])
            paths.sort(key=lambda pair: len(pair[0]))
            if len(paths) > 0:
                for path in paths:
                    if not path[1].reserved:
                        car.set_path(path[0])
                        path[1].reserved = True
                        break
            else:
                print(f"No parking lots available for car {car.id}")
            
            