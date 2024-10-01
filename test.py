from src import np, plt, Parameters, Image, FindPredominantBrightness, CreateModel
import time

__author__ = "Davi Melonio"

def run():
    PATH = "config/parameters.txt"
    p = Parameters(PATH)

    image_loader = Image(p.image_file_path)
    img = image_loader.img

    brightness_finder = FindPredominantBrightness(img)
    frequent_brightness = brightness_finder.get()

    model_creator = CreateModel(image_loader, frequent_brightness, p.vp_interfaces, p.model_extra_routine)
    model = model_creator.set_values()

    return model

if __name__ == '__main__':
    start = time.time()

    model = run()

    end = time.time()

    plt.imshow(model)
    plt.show()

    print(f"Runtime: {end - start} seconds")

