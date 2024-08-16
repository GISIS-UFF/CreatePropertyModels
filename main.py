#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# ---------------------------------------------------------------------------

__author__ = "Davi Melonio"

from functions.parallel_plane_model import AcousticModel, ElasticModel
from functions.img2model_project import *
import time
import numpy as np

class Parameters:
    def __init__(self, parameters: list):
        self.model_id = parameters[0]
        self.model_extra_routine = parameters[1]
        self.export_model_to_binary_file = parameters[2]
        self.plot_model = parameters[3]
        self.image_file_path = parameters[4]
        self.vp_velocity = parameters[5]
        self.vs_velocity = [round(i / 1.7, 2) for i in parameters[6]] if parameters[8] else parameters[6]
        self.rho_value = parameters[7]
        self.vs_velocity_approximation = parameters[8]
        self.complex_model_bool = parameters[9]
        self.inverse_velocity = parameters[10]
        self.vmin = parameters[11]
        self.vmax = parameters[12]
        self.parallel_plane_model_id = parameters[13]
        self.model_parallel_plane_id = parameters[14]
        self.plot_model_bool = parameters[15]
        self.nx = parameters[16]
        self.nz = parameters[17]
        self.interfaces = parameters[18]
        self.vp_interfaces = parameters[19]
        self.vs_interfaces = parameters[20]
        self.rho_interfaces = parameters[21]

def print_parameters(data: Parameters) -> None:
    print("=============== Configuration ===============\n")
    print("### Image to Model Area ###\n")
    print("->Model Bools")
    print(f"        Model_ID = {data.model_id}") 
    print(f"        Model_Extra_Routine = {data.model_extra_routine}") 
    print(f"        Export_Model_to_Binary_File = {data.export_model_to_binary_file}")
    print(f"        Plot_Model = {data.plot_model}\n")

    print("->Load Image Model")
    print(f"        Image_File_Path = {data.image_file_path}\n")

    print("->Model Parameters")
    print(f"        VP_Velocity = {data.vp_velocity}")
    print(f"        VS_Velocity = {data.vs_velocity}")
    print(f"        Rho_Value = {data.rho_value}\n")

    print("->VS Velocity Approximation")
    print(f"        VS_Velocity = {data.vs_velocity_approximation}\n")

    print("->Complex Model\n")
    print(f"        Complex_Model_ID = {data.complex_model_bool}")
    print(f"        Inverse_Velocity = {data.inverse_velocity}\n")

    print(f"        Minimum_Velocity = {data.vmin}")
    print(f"        Maximum_Velocity = {data.vmax}\n")

    print("### Parallel Plane Model Area ###\n")
    print("->Model Bools")
    print(f"        Parallel_Plane_Model_ID = {data.parallel_plane_model_id}")
    print(f"        Model_ID = {data.inverse_velocity}")
    print(f"        Plot_Model = {data.plot_model_bool}\n")

    print("->Model Parameters")
    print(f"        Nx = {data.nx}")
    print(f"        Nz = {data.nz}")
    print(f"        Interfaces = {data.interfaces}")
    print(f"        VP_Velocity = {data.vp_interfaces}")
    print(f"        VS_Velocity = {data.vs_interfaces}")
    print(f"        Rho_Value = {data.rho_interfaces}\n")
    print("============================================\n")

def model_type_img(id: int, image: np.array, frequent_brightness: list, vp_interfaces: list, vs_interfaces: list, rho_interfaces: list, model_routine_bool: bool) -> list:
    if id == 1:
        return ModelCreator.create_model(image, frequent_brightness, vp_interfaces, model_routine_bool)
    elif id == 2:
        model_vp = ModelCreator.create_model(image, frequent_brightness, vp_interfaces, model_routine_bool)
        model_vs = ModelCreator.create_model(image, frequent_brightness, vs_interfaces, model_routine_bool)
        model_rho = ModelCreator.create_model(image, frequent_brightness, rho_interfaces, model_routine_bool)
        return [model_vp, model_vs, model_rho]
    else:
        raise KeyError("Please select a valid key. [1, 2]")

def model_type_parallel(id: int, Nx: int, Nz: int, vp_interfaces: list, vs_interfaces: list, rho_interfaces: list, interfaces: list):
    if id == 1:
        instanced_model = AcousticModel(Nx, Nz, vp_interfaces, interfaces)
        return instanced_model.set_model()
    elif id == 2:
        instanced_model = ElasticModel(Nx, Nz, vp_interfaces, vs_interfaces, rho_interfaces, interfaces)
        return instanced_model.set_model()
    else:
        raise KeyError("Please select a valid key. [1, 2]")

def model_plot(model_id: int, plot_model_bool: bool, model: np.array, Nx: int, Nz: int) -> None:
    if plot_model_bool:
        if model_id == 1:
            AcousticModelPlot.acoustic_plot(model, Nx, Nz)
        elif model_id == 2:
            ElasticModelPlot.elastic_model_plot(model[0], model[1], model[2], Nx, Nz)

def export2binary(bin_id: bool, model_id: int, model: np.array, path_seiswave: str) -> None:
    if bin_id:
        if model_id == 1:
            Export2Binary(model, path_seiswave + "model_vp_2d.bin").export_model_to_binary()
        elif model_id == 2:
            Export2Binary(model[0], path_seiswave + "model_vp_2d.bin").export_model_to_binary()
            Export2Binary(model[1], path_seiswave + "model_vs_2d.bin").export_model_to_binary()
            Export2Binary(model[2], path_seiswave + "model_rho_2d.bin").export_model_to_binary() 

def print_runtime():
    end = time.time()
    print(f"Runtime: {round(end - start, 4)} seconds")

start = time.time()

instanced_parameters = GetParameters("parameters/parameters.txt")
parameters_list = instanced_parameters.get_parameter()
data = Parameters(parameters_list)

print_parameters(data)

if data.parallel_plane_model_id:
    model = model_type_parallel(data.model_parallel_plane_id, data.nx, data.nz, data.vp_interfaces, data.vs_interfaces, data.rho_interfaces, data.interfaces)
    
    print_runtime()

    model_plot(data.parallel_plane_model_id, data.plot_model_bool, model, data.nx, data.nz)
elif data.complex_model_bool:
    instanced_image_loader = ImageLoader(data.image_file_path)
    image = instanced_image_loader.load_image()
    
    instanced_complex_model_generator = CreateComplexModel(image, data.vmin, data.vmax, data.inverse_velocity)
    model = instanced_complex_model_generator.set_model_values()
    
    print_runtime()

    Nz, Nx = image.shape
    model_plot(data.model_id, data.plot_model_bool, model, Nx, Nz)
    
    if data.export_model_to_binary_file:
        export2binary(data.export_model_to_binary_file, data.model_id, model, data.output_binary_path)

else:
    instanced_image_loader = ImageLoader(data.image_file_path)
    image = instanced_image_loader.load_image()
    
    instanced_image_color_finder = FindPredominantBrightness(image)
    frequent_brightness = instanced_image_color_finder.get_image_predominant_brightness()
    model = model_type_img(data.model_id, image, frequent_brightness, data.vp_velocity, data.vs_velocity, data.rho_value, data.model_extra_routine)
    
    print_runtime()

    Nz, Nx = image.shape
    model_plot(data.model_id, data.plot_model_bool, model, Nx, Nz)
    
    if data.export_model_to_binary_file:
        export2binary(data.export_model_to_binary_file, data.model_id, model, "binary_models/")

