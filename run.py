#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# @author: Davi Melonio
# ---------------------------------------------------------------------------

from src import Parameters, ModelFactory, measure_runtime

PATH = "config/parameters.txt"

@measure_runtime
def run():
    p = Parameters(PATH)
    factory = ModelFactory(p) 
    factory.create_model()
    return factory

if __name__ == '__main__':
    factory = run()
    factory.plot_model()
