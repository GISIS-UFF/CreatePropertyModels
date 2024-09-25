class ErrorHandling:
    """
    Class for management of error messages
    """
    @staticmethod
    def verify_image_existence() -> None:
        print("Image not found. Please verify the file path.")
        exit()

    @staticmethod
    def wrong_image_format() -> None:
        print("Please use a valid image format. [png, jpg, jpeg]")
        exit()

    @staticmethod
    def could_not_open_file() -> None:
        print("Can't open/read file. Make sure your file path is right.")
        exit()
# error handling parallel
# class ErrorHandling:
#     """
#     Class for management of error messages
#     """
#     @staticmethod
#     def interface_error(interfaces: list, value_interfaces: list) -> None:
#         if len(interfaces) != len(value_interfaces) - 1:
#             raise ValueError("Interfaces Must be a Length Smaller than velocity_interfaces!")
#
#     @staticmethod
#     def negative_model_parameters(Nx: int, Nz: int) -> None:
#         if Nx < 0 or Nz < 0:
#             raise ValueError("Model Parameters Cannot be Negative!")
