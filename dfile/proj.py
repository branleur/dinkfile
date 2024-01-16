"""Saves and loads 'project' files which are just pickled data files consisting of both the map and index"""
import pickle
import logging
from os.path import join

def loadproj(file):
    """Loads a project file and returns a map and index"""
    with open(file, 'rb') as f:
        mapping = pickle.load(f)
        index = mapping.pop()
    logging.info("Loading the project file")
    return index, mapping

def saveproj(index, mapping, path):
    """Saves the data into a pickled file at path"""
    data = mapping[:]
    data.append(index)
    with open(join(path, "map.dink"), 'wb') as f:
        pickle.dump(data, f)
        logging.info("Saving the project file")
