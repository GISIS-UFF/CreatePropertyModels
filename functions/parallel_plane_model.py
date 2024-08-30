import numpy as np

class AcousticModel:
    """
    Creates VP model
    """
    def __init__(self, Nx: int, Nz: int, vp_interfaces: list, interfaces: list) -> None:
        ErrorHandling.negative_model_parameters(Nx, Nz)

        self.Nx = Nx
        self.Nz = Nz
        self.value_interface = vp_interfaces
        self.interfaces = interfaces

    def set_model(self) -> np.array:
        self.model_to_plot = np.zeros((self.Nz, self.Nx))

        ErrorHandling.interface_error(self.interfaces, self.value_interface)

        self.__create_model_loop()
        return self.model_to_plot
    
    def __create_model_loop(self) -> None:
        self.model_to_plot[:self.interfaces[0], :] = self.value_interface[0]
        for layer, velocity in enumerate(self.value_interface[1:]):
            self.model_to_plot[self.interfaces[layer]:, :] = velocity

class ElasticModel:
    """
    Creates VP, VS and Density model
    """
    def __init__(self, Nx: int, Nz: int, vp_interfaces: list, vs_interfaces: list, rho_interfaces: list, interfaces: list) -> None:
        ErrorHandling.negative_model_parameters(Nx, Nz)

        self.Nx = Nx
        self.Nz = Nz
        self.value_interfaces = [vp_interfaces, vs_interfaces, rho_interfaces]
        self.interfaces = interfaces

    def set_model(self) -> np.array:
        models = []
        for i in range(len(self.value_interfaces)):
            self.model_to_plot = np.zeros((self.Nz, self.Nx))
            current_model = self.__create_model_loop(self.value_interfaces[i])
            models.append(current_model)
        return models

    def __create_model_loop(self, current_model_interface: list) -> np.array:
        self.model_to_plot[:self.interfaces[0], :] = current_model_interface[0]
        for layer, property_value in enumerate(current_model_interface[1:]):
            self.model_to_plot[self.interfaces[layer]:, :] = property_value
        return self.model_to_plot        

class ErrorHandling:
    """
    Class for management of error messages
    """
    @staticmethod
    def interface_error(interfaces: list, value_interfaces: list) -> None:
        if len(interfaces) != len(value_interfaces) - 1:
            raise ValueError("Interfaces Must be a Length Smaller than velocity_interfaces!")

    @staticmethod
    def negative_model_parameters(Nx: int, Nz: int) -> None:
        if Nx < 0 or Nz < 0:
            raise ValueError("Model Parameters Cannot be Negative!")

