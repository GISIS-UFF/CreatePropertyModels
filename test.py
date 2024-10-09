from src import Parameters, Image, Plot
import debug.print_parameters 
import time

# run só controla, não fica passando parametro
__author__ = "Davi Melonio"

def run():
    PATH = "config/parameters.txt"
    p = Parameters(PATH)
    img = Image(p)

    model = img.model

    if p.print_parameters:
        debug.print_parameters.print_parameters(p)    

    return p, img, model

if __name__ == '__main__':
    start = time.time()

    p, img, model = run()

    end = time.time()

    print(f"Runtime: {end - start} seconds")

    Plot(p, img)
