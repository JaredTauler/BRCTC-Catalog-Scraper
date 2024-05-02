import pickle
import os
path = "D:/PycharmProjects/PlacementWebapp/pickles" # FIXME


def pickle_load(filename):
    with open(f'{path}/{filename}.pkl', 'rb') as file:
        return pickle.load(file)

def pickle_dump(filename, out):
    with open(f'{path}/{filename}.pkl', 'wb') as file:
        pickle.dump(out, file)