import os
import pickle

def volver():
    while True:
        try:
            os.chdir('Facturacion')
            break
        except FileNotFoundError: os.chdir('..')

def cargar(clase: str):
    lista = []

    if f'{clase}.pkl' not in os.listdir():
        return lista

    f = open(f'{clase}.pkl', 'rb')
    while True:
        try:
            x = pickle.load(f)
            lista.append(x)

        except EOFError:
            f.close()
            break

    return lista