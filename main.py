#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# ---------------------------------------------------------------------------

__author__ = "Davi Melonio"

from functions.parallel_plane_model import AcousticModel, ElasticModel
from functions.img2model_project import *
import time
import os

def print_parameters(parameters: str) -> None:
    print("=============== Configuration ===============\n")
    print("### Image to Model Area ###\n")
    print("->Model Bools")
    print(f"        Model_ID = {parameters[0]}") 
    print(f"        Model_Extra_Routine = {parameters[1]}") 
    print(f"        Export_Model_to_Binary_File = {parameters[2]}")
    print(f"        Plot_Model = {parameters[3]}\n")

    print("->Load Image Model")
    print(f"        Image_File_Path = {parameters[4]}\n")

    print("->Model Parameters")
    print(f"        VP_Velocity = {parameters[5]}")
    print(f"        VS_Velocity = {parameters[6]}")
    print(f"        Rho_Value = {parameters[7]}\n")

    print("->VS Velocity Approximation")
    print(f"        VS_Velocity = {parameters[8]}\n")

    print("->Output Binary File")
    print(f"        Output_Binary_Path = {parameters[9]}\n")

    print("### Parallel Plane Model Area ###\n")
    print("->Model Bools")
    print(f"        Parallel_Plane_Model_ID = {parameters[10]}")
    print(f"        Model_ID = {parameters[11]}")
    print(f"        Plot_Model = {parameters[12]}\n")

    print("->Model Parameters")
    print(f"        Nx = {parameters[13]}")
    print(f"        Nz = {parameters[14]}")
    print(f"        Interfaces = {parameters[15]}")
    print(f"        VP_Velocity = {parameters[16]}")
    print(f"        VS_Velocity = {parameters[17]}")
    print(f"        Rho_Value = {parameters[18]}\n")
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

def model_plot(model_id: int, model_plot_bool: bool, model: np.array, Nx: int, Nz: int) -> None:
    if model_plot_bool:
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

start = time.time()
path = os.getcwd()

instanced_parameters = GetParameters(path + "/parameters/parameters.txt")
parameters = instanced_parameters.get_parameter()

print_parameters(parameters)

parallel_plane_model = parameters[10]
if parallel_plane_model:
    model_id = parameters[11]
    model_plot_bool = parameters[12]
    Nx = parameters[13]
    Nz = parameters[14]
    interfaces = parameters[15]
    vp_interfaces = parameters[16]
    vs_interfaces = parameters[17]
    rho_interfaces = parameters[18]

    end = time.time()
    print(f"Runtime: {round(end - start, 4)} seconds")

    model = model_type_parallel(model_id, Nx, Nz, vp_interfaces, vs_interfaces, rho_interfaces, interfaces)
    model_plot(model_id, model_plot_bool, model, Nx, Nz)
else:
    model_id = parameters[0]
    model_routine_bool = parameters[1]
    model_binary_bool = parameters[2]
    model_plot_bool = parameters[3]

    instanced_image_loader = ImageLoader(parameters[4])
    image = instanced_image_loader.load_image()

    instanced_image_color_finder = FindPredominantBrightness(image)
    frequent_brightness = instanced_image_color_finder.get_image_predominant_brightness()

    vp_interfaces = parameters[5]
    vs_interfaces = [i / 1.7 for i in vp_interfaces] if parameters[8] else parameters[6]
    rho_interfaces = parameters[7]

    model = model_type_img(model_id, image, frequent_brightness, vp_interfaces, vs_interfaces, rho_interfaces, model_routine_bool)
    path_seiswave = parameters[9]
    export2binary(model_binary_bool, model_id, model, path_seiswave)

    end = time.time()
    print(f"Runtime: {round(end - start, 4)} seconds")
    
    Nz, Nx = image.shape
    model_plot(model_id, model_plot_bool, model, Nx, Nz)
