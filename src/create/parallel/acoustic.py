from src import np, ErrorHandling

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
