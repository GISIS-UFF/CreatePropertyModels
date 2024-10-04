from src import np, ErrorHandling

class Parallel:
    def __init__(self, Nx: int, Nz: int, interfaces: list, value_interfaces: list):
        self.Nx = Nx
        self.Nz = Nz
        self.value_interfaces = value_interfaces
        self.interfaces = interfaces
        self.model = np.zeros((Nz, Nx))

    def acoustic(self):
        self.__create_model_loop(self.value_interfaces[0])

    def elastic(self):
        aux_model = []
        for i in range(len(self.value_interfaces)):
            self.__create_model_loop(self.value_interfaces[i])
            aux_model.append(self.model)
        self.model = aux_model

    def __create_model_loop(self, value_interfaces) -> None:
        self.model[:self.interfaces[0], :] = value_interfaces[0]
        for layer, velocity in enumerate(value_interfaces[1:]):
            self.model[self.interfaces[layer]:, :] = velocity
