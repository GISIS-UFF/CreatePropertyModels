__author__ = "Davi Melonio"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from utils.error_handling import ErrorHandling

from .image.load import ImageLoader

from .parameters.get import GetParameters
from .parameters.define import Parameters

from utils.extra_routine import ModelRoutine
from utils.predominant_brightness import FindPredominantBrightness
# from .create.img2model.model import CreateModel
# from .create.img2model.complex import CreateComplexModel
# from .plot.acoustic import AcousticModelPlot
# from .plot.elastic import ElasticModelPlot
# from .create.parallel.acoustic import AcousticModel
# from .create.parallel.elastic import ElasticModel
#
# __all__ = [
#     "ErrorHandling", "Parameters", "ModelRoutine",
#     "FindPredominantBrightness", "AcousticModelPlot",
#     "CreateComplexModel", "ElasticModelPlot", "ImageLoader",
#     "CreateModel", "CreateComplexModel", "AcousticModel", 
#     "ElasticModel", "np", "plt", "mpimg"
# ]

__all__ = [
    "ErrorHandling", "ImageLoader",
    "GetParameters", "Parameters"
]

PATH = "config/parameters.txt"
p = GetParameters(PATH)

data_raw = p.get()

data = Parameters(data_raw)


