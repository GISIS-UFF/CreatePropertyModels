from sys import path
path.append("../")
# TODO: make it work
from src import Parameters, Image, Plot
import time

__author__ = "Davi Melonio"

def run():
    start = time.time()

    PATH = "config/parameters.txt"
    p = Parameters(PATH)
    img = Image(p)

    end = time.time()

    print(f"Runtime: {end - start} seconds")

    Plot(p, img)

if __name__ == '__main__':
    run()
