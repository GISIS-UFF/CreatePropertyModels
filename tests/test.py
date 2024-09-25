import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ModelCreator:
    @staticmethod
    def create_model(image: np.array, frequent_brightness: list, interfaces: list, routine_bool: bool) -> np.array:
        model_creator = CreateModel(image, frequent_brightness, interfaces, routine_bool)
        return model_creator.set_model_values()

