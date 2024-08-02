import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class ModelProvider(ABC):
    @abstractmethod
    def set_model(self):
        pass


class AcousticModel(ModelProvider):
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
        self.__create_zero_model()

        ErrorHandling.interface_error(self.interfaces, self.value_interface)

        self.__create_model_loop()
        return self.model_to_plot
    
    def __create_model_loop(self) -> None:
        self.model_to_plot[:self.interfaces[0], :] = self.value_interface[0]
        for layer, velocity in enumerate(self.value_interface[1:]):
            self.model_to_plot[self.interfaces[layer]:, :] = velocity

    def __create_zero_model(self) -> None:
        self.model_to_plot = np.zeros((self.Nz, self.Nx))


class ElasticModel(ModelProvider):
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
            self.__create_zero_model()
            current_model = self.__create_model_loop(self.value_interfaces[i])
            models.append(current_model)
        return models

    def __create_model_loop(self, current_model_interface: list) -> np.array:
        self.model_to_plot[:self.interfaces[0], :] = current_model_interface[0]
        for layer, property_value in enumerate(current_model_interface[1:]):
            self.model_to_plot[self.interfaces[layer]:, :] = property_value
        return self.model_to_plot        

    def __create_zero_model(self) -> None:
        self.model_to_plot = np.zeros((self.Nz, self.Nx))


class AcousticModelPlot:

    @staticmethod
    def acoustic_plot(model: list, Nx: int, Nz: int):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18,10))

        xloc = np.linspace(0, Nx - 1, 11, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax.imshow(model, cmap="jet")
        ax.set_title("VP Model", fontsize=15)
        ax.set_xlabel("Distance [m]",fontsize=12)
        ax.set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, label='VP [m/s]')
        cax.set_ticks(np.linspace(model.min(), model.max(), num=5))

        ax.set_xticks(xloc)
        ax.set_xticklabels(xlab)

        ax.set_yticks(zloc)
        ax.set_yticklabels(zlab)

        plt.show()
        return fig


class ElasticModelPlot:
    
    @staticmethod
    def elastic_model_plot(models: list, Nx: int, Nz: int):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(18,10))

        xloc = np.linspace(0, Nx - 1, 11, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax[0].imshow(models[0], cmap="jet")
        ax[0].set_title("VP Model", fontsize=15)
        ax[0].set_xlabel("Distance [m]",fontsize=12)
        ax[0].set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, ax=ax[0], label='VP [m/s]')
        cax.set_ticks(np.linspace(models[0].min(), models[0].max(), num=5))

        im2 = ax[1].imshow(models[1], cmap="jet")
        ax[1].set_title("VS Model", fontsize=15)
        ax[1].set_xlabel("Distance [m]",fontsize=12)
        ax[1].set_ylabel("Depth [m]", fontsize=12)
        cax2 = fig.colorbar(im2, ax=ax[1], label='VS [m/s]')
        cax2.set_ticks(np.linspace(models[1].min(), models[1].max(), num=5))

        im3 = ax[2].imshow(models[2], cmap="jet")
        ax[2].set_title("Density Model", fontsize=15)
        ax[2].set_xlabel("Distance [m]",fontsize=12)
        ax[2].set_ylabel("Depth [m]", fontsize=12)
        cax3 = fig.colorbar(im3, ax=ax[2], label='Density [kg/m$^3$]')
        cax3.set_ticks(np.linspace(models[2].min(), models[2].max(), num=5))

        for i in range(len(ax)):
            ax[i].set_xticks(xloc)
            ax[i].set_xticklabels(xlab)

            ax[i].set_yticks(zloc)
            ax[i].set_yticklabels(zlab)

        plt.show()
        return fig


class ErrorHandling:
    """
    Class for management of error messages
    """
    @staticmethod
    def interface_error(interfaces: list, value_interfaces: list) -> None:
        for value_interface in value_interfaces:
            if len(interfaces) != len(value_interface) - 1:
                raise ValueError("Interfaces Must be a Length Smaller than velocity_interfaces!")

    @staticmethod
    def negative_model_parameters(Nx: int, Nz: int) -> None:
        if Nx < 0 or Nz < 0:
            raise ValueError("Model Parameters Cannot be Negative!")

