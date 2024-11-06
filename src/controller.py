from abc import ABC, abstractmethod

class Controller:

    def __init__(self, simulation):
        self.simulation = simulation

    @abstractmethod
    def update(self):
        """ Update the simulation state. Route cars, control cars, etc. """
        pass

