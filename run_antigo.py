#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# ---------------------------------------------------------------------------

__author__ = "Davi Melonio"

from functions.parallel_plane_model import AcousticModel, ElasticModel
from functions.img2model_project import *
from scipy.ndimage import gaussian_filter
import time
import numpy as np

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
