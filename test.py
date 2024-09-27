from src import GetParameters, Parameters
from src import ImageLoader

# class ModelCreator:
#     @staticmethod
#     def create_model(image: np.array, frequent_brightness: list, interfaces: list, routine_bool: bool) -> np.array:
#         model_creator = CreateModel(image, frequent_brightness, interfaces, routine_bool)
#         return model_creator.set_model_values()

def run():
    
    PATH = "config/parameters.txt"
    p = GetParameters(PATH)

    data_raw = p.get()

    d = Parameters(data_raw)

    test = d.image_file_path

    i = ImageLoader("data/input/salt_model.png")

    img = i.load()

    height, width = i.get_dimension()

    print(d.model_id)
    print(height, width)

if __name__ == '__main__':
    run()
