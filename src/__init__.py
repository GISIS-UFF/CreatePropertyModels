__author__ = "Davi Melonio"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from utils.error_handling import ErrorHandling

from .parameters import Parameters
from .image.load import ImageLoader, ImageDimensions
from .create.img2model.model import CreateModel
from .create.img2model.complex import CreateComplexModel
from .routines.extra import ModelRoutine
from .routines.predominant_brightness import FindPredominantBrightness
from .plot.acoustic import AcousticModelPlot
from .plot.elastic import ElasticModelPlot
from .create.parallel.acoustic import AcousticModel
from .create.parallel.elastic import ElasticModel

__all__ = [
    "ErrorHandling", "Parameters", "ModelRoutine",
    "FindPredominantBrightness", "AcousticModelPlot",
    "CreateComplexModel", "ElasticModelPlot", "ImageLoader",
   "ImageDimensions" , "CreateModel", "CreateComplexModel", 
    "AcousticModel", "ElasticModel", "np", "plt", "mpimg"
]

PATH = "config/parameters.txt"

p = Parameters(PATH)

data = p.get()
