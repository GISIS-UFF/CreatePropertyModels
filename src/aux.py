import time

class ErrorHandling:
    """
    Class for management of error messages
    """

    @staticmethod
    def verify_image_existence() -> None:
        raise FileNotFoundError("Image not found. Please verify the file path.")

    @staticmethod
    def wrong_image_format() -> None:
        raise ValueError("Please use a valid image format. [png, jpg, jpeg]")

    @staticmethod
    def could_not_open_file() -> None:
        raise IOError("Can't open/read file. Make sure your file path is right.")

    @staticmethod
    def interface_error(interfaces: list, value_interfaces: list) -> None:
        if len(interfaces) != len(value_interfaces) - 1:
            raise ValueError("Interfaces must be a length smaller than velocity_interfaces!")

    @staticmethod
    def negative_model_parameters(Nx: int, Nz: int) -> None:
        if Nx < 0 or Nz < 0:
            raise ValueError("Model parameters cannot be negative!")

def measure_runtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Runtime: {end - start} seconds")
        return result
    return wrapper
