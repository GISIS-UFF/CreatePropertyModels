#----------------------------------------------------------------------------
# Create Date: 16/07/2024 3:30PM
# @author: Davi Melonio
# ---------------------------------------------------------------------------
# TODO: escrever minha a rotina de conversão() em C
import time
from src import Parameters, ModelFactory

def run():
    start = time.time()

    PATH = "config/parameters.txt"
    p = Parameters(PATH)
    model_factory = ModelFactory(p) 
    model = model_factory.create_model()
    # botar lógica do elástica aqui, chamar 3 vezes
    model.set_values()
    # loop do elastico para binary aqui também

    end = time.time()

    print(f"Runtime: {end - start} seconds")

    if p.model_id == 1:
        model.plot_acoustic()
    elif p.model == 2:
        pass

if __name__ == '__main__':
    run()
