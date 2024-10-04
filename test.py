from src import np, plt, Parameters, Image, PredominantBrightness, CreateModel, Parallel
import debug.print_parameters 
import time

__author__ = "Davi Melonio"

def run():
    PATH = "config/parameters.txt"
    p = Parameters(PATH)

    image_loader = Image(p.image_file_path)
    img = image_loader.img

    brightness_finder = PredominantBrightness(img, len(p.vp_velocity))
    frequent_brightness = brightness_finder.get()

    model_creator = CreateModel(image_loader, frequent_brightness, p.vp_velocity, p.model_extra_routine)
    # deixar model no construtor
    model = model_creator.set_values()

    # model_create = Parallel(p.nx, p.nz, p.interfaces,  
                            # [p.vp_velocity_parallel, p.vs_velocity_parallel, p.density_value_parallel]) 

    # model_create.acoustic()

    # model = model_create.model

    debug.print_parameters.print_parameters(p)    

    return model

if __name__ == '__main__':
    start = time.time()

    model = run()

    end = time.time()

    plt.imshow(model)
    plt.show()

    print(f"Runtime: {end - start} seconds")

