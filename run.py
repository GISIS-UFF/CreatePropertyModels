#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# @author: Davi Melonio
# ---------------------------------------------------------------------------

import time
from src import Parameters, Image, Plot

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
