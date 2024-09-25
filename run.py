#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# ---------------------------------------------------------------------------

__author__ = "Davi Melonio"

from functions.parallel_plane_model import AcousticModel, ElasticModel
from functions.img2model_project import *
from scipy.ndimage import gaussian_filter
import time
import numpy as np

class Parameters:
    def __init__(self, parameters: list):
        self.model_id = parameters[0]
        self.export_model_to_binary_file = parameters[1]
        self.plot_model_bool = parameters[2]
        self.model_smoothing_bool = parameters[3]
        self.smooth_level = parameters[4]
        self.binary_model_path = parameters[5]
        self.vs_velocity_approximation = parameters[6]
        self.rho_value_approximation = parameters[7]
        self.image_to_model_id = parameters[8]
        self.model_extra_routine = parameters[9]
        self.image_file_path = parameters[10]
        self.vp_velocity = parameters[11]
        self.vs_velocity = [round(i / 1.7, 2) for i in parameters[11]] if parameters[6] else parameters[12]
        self.rho_value = [round((0.31 * i ** 0.25) * 1e3, 2) for i in parameters[11]] if parameters[7] else parameters[13]
        self.complex_model_bool = parameters[14]
        self.inverse_velocity = parameters[15]
        self.vpmin = parameters[16]
        self.vpmax = parameters[17]
        self.vsmin = parameters[18] if not parameters[6] else round(parameters[16] / 1.7, 2)
        self.vsmax = parameters[19] if not parameters[6] else round(parameters[17] / 1.7, 2)
        self.rhomin = parameters[20] if not parameters[7] else round((0.31 * parameters[16] ** 0.25) * 1e3, 2)
        self.rhomax = parameters[21] if not parameters[7] else round((0.31 * parameters[17] ** 0.25) * 1e3, 2)
        self.parallel_plane_model_id = parameters[22]
        self.nx = parameters[23]
        self.nz = parameters[24]
        self.interfaces = parameters[25]
        self.vp_interfaces = parameters[26]
        self.vs_interfaces = parameters[27]
        self.rho_interfaces = parameters[28]

def print_parameters(data: Parameters) -> None:
    print("=============== Configuration ===============\n")
    
    print("### General Parameters ###\n")
    print("-> Model Parameters")
    print(f"        Model_ID = {data.model_id}")
    print(f"        Export_Model_to_Binary_File = {data.export_model_to_binary_file}")
    print(f"        Plot_Model = {data.plot_model_bool}")
    print(f"        Model_Smoothing = {data.model_smoothing_bool}")
    print(f"        Smooth_Level = {data.smooth_level}\n")
    
    print("-> Export Model Path")
    print(f"        Binary_Model_Path = {data.binary_model_path}\n")
    
    print("-> VS Velocity Approximation")
    print(f"        VS_Velocity = {data.vs_velocity_approximation}\n")
    
    print("-> Density Value Approximation")
    print(f"        Density_Value = {data.rho_value_approximation}\n")

    print("### Image to Model Area ###\n")
    print("-> Model Bools")
    print(f"        Image_To_Model_ID = {data.image_to_model_id}")
    print(f"        Model_Extra_Routine = {data.model_extra_routine}\n")
    
    print("-> Load Image Model")
    print(f"        Image_File_Path = {data.image_file_path}\n")
    
    print("-> Model Parameters")
    print(f"        VP_Velocity = {data.vp_velocity}")
    print(f"        VS_Velocity = {data.vs_velocity}")
    print(f"        Rho_Value = {data.rho_value}\n")
    
    print("### Complex Image Model ###\n")
    print("-> Model Bools")
    print(f"        Complex_Model_ID = {data.complex_model_bool}")
    print(f"        Inverse_Velocity = {data.inverse_velocity}\n")

    print("-> Model Parameters")
    print(f"        Minimum_VP_Velocity = {data.vpmin}")
    print(f"        Maximum_VP_Velocity = {data.vpmax}")
    print(f"        Minimum_VS_Velocity = {data.vsmin}")
    print(f"        Maximum_VS_Velocity = {data.vsmax}")
    print(f"        Minimum_Density = {data.rhomin}")
    print(f"        Maximum_Density = {data.rhomax}\n")
    
    print("### Parallel Plane Model Area ###\n")
    print("-> Model Bools")
    print(f"        Parallel_Plane_Model_ID = {data.parallel_plane_model_id}\n")
    
    print("-> Model Parameters")
    print(f"        Nx = {data.nx}")
    print(f"        Nz = {data.nz}")
    print(f"        Interfaces = {data.interfaces}")
    print(f"        VP_Velocity = {data.vp_interfaces}")
    print(f"        VS_Velocity = {data.vs_interfaces}")
    print(f"        Rho_Value = {data.rho_interfaces}\n")
    
    print("============================================\n")

def model_type_img(id: int, image: np.array, frequent_brightness: list, vp_interfaces: list, vs_interfaces: list, rho_interfaces: list, model_routine_bool: bool) -> np.array:
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

def model_type_complex(id: int, image: np.array, vp_limits: list, vs_limits: list, rho_limits: list, inverse_velocity: bool) -> np.array:
    if id == 1:
        instanced_complex_model_generator = CreateComplexModel(image, data.vpmin, data.vpmax, data.inverse_velocity)
        model = instanced_complex_model_generator.set_model_values()
        return model
    elif id == 2:
        instanced_complex_model_generator = CreateComplexModel(image, vp_limits[0], vp_limits[1], inverse_velocity)
        model_vp = instanced_complex_model_generator.set_model_values()
        instanced_complex_model_generator = CreateComplexModel(image, vs_limits[0], vs_limits[1], inverse_velocity)
        model_vs = instanced_complex_model_generator.set_model_values()
        instanced_complex_model_generator = CreateComplexModel(image, rho_limits[0], rho_limits[1], inverse_velocity)
        model_rho = instanced_complex_model_generator.set_model_values()
        return [model_vp, model_vs, model_rho]
    else:
        raise KeyError("Please select a valid key. [1, 2]")

def apply_model_smooth(model_id: bool, model: np.array) -> np.array:
    if model_id == 1:
     model = gaussian_filter(model, sigma=data.smooth_level)
    elif model_id == 2:
        model[0] = gaussian_filter(model[0], sigma=data.smooth_level)
        model[1] = gaussian_filter(model[1], sigma=data.smooth_level)
        model[2] = gaussian_filter(model[2], sigma=data.smooth_level)
    return model

def model_plot(model_id: int, plot_model_bool: bool, model: np.array, Nx: int, Nz: int) -> None:
    if plot_model_bool:
        if model_id == 1:
            AcousticModelPlot.acoustic_plot(model, Nx, Nz)
        elif model_id == 2:
            ElasticModelPlot.elastic_model_plot(model[0], model[1], model[2], Nx, Nz)

def export2binary(bin_id: bool, model_id: int, model: np.array, binary_model_path: str) -> None:
    if bin_id:
        if model_id == 1:
            Export2Binary(model, binary_model_path + "model_vp_2d.bin").export_model_to_binary()
        elif model_id == 2:
            Export2Binary(model[0], binary_model_path + "model_vp_2d.bin").export_model_to_binary()
            Export2Binary(model[1], binary_model_path + "model_vs_2d.bin").export_model_to_binary()
            Export2Binary(model[2], binary_model_path + "model_rho_2d.bin").export_model_to_binary() 

def print_runtime():
    end = time.time()
    print(f"Runtime: {round(end - start, 4)} seconds")

start = time.time()

instanced_parameters = GetParameters("parameters/parameters.txt")
parameters_list = instanced_parameters.get_parameter()
data = Parameters(parameters_list)

print_parameters(data)

if data.parallel_plane_model_id + data.complex_model_bool + data.image_to_model_id > 1:
    print("You can only have one Model Generation activated.")
    exit()

if data.parallel_plane_model_id:
    model = model_type_parallel(data.model_id, data.nx, data.nz, data.vp_interfaces, data.vs_interfaces, data.rho_interfaces, data.interfaces)

    if data.model_smoothing_bool:
        model = apply_model_smooth(data.model_id, model)

    print_runtime()

    model_plot(data.model_id, data.plot_model_bool, model, data.nx, data.nz)

    if data.export_model_to_binary_file:
        export2binary(data.export_model_to_binary_file, data.model_id, model, data.binary_model_path)
    
elif data.complex_model_bool:
    instanced_image_loader = ImageLoader(data.image_file_path)
    image = instanced_image_loader.load_image()

    vp_limits = [data.vpmin, data.vpmax]
    vs_limits = [data.vsmin, data.vsmax]
    rho_limits = [data.rhomin, data.rhomax]

    model = model_type_complex(data.model_id, image, vp_limits, vs_limits, rho_limits, data.inverse_velocity)

    if data.model_smoothing_bool:
        model = apply_model_smooth(data.model_id, model)
    print_runtime()

    Nz, Nx = image.shape
    model_plot(data.model_id, data.plot_model_bool, model, Nx, Nz)

    if data.export_model_to_binary_file:
        export2binary(data.export_model_to_binary_file, data.model_id, model, data.binary_model_path)

elif data.image_to_model_id:
    instanced_image_loader = ImageLoader(data.image_file_path)
    image = instanced_image_loader.load_image()
    
    instanced_image_color_finder = FindPredominantBrightness(image)
    frequent_brightness = instanced_image_color_finder.get_image_predominant_brightness()
    model = model_type_img(data.model_id, image, frequent_brightness, data.vp_velocity, data.vs_velocity, data.rho_value, data.model_extra_routine)

    if data.model_smoothing_bool:
        model = apply_model_smooth(data.model_id, model)

    print_runtime()

    Nz, Nx = image.shape
    model_plot(data.model_id, data.plot_model_bool, model, Nx, Nz)

    if data.export_model_to_binary_file:
        export2binary(data.export_model_to_binary_file, data.model_id, model, data.binary_model_path)
else:
    print("Select a valid model generator. Verify if you activated the right parameters in Model Bools.")
    exit()