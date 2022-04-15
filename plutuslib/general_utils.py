import pickle
import random
from typing import List

def save_file(path: str, obj):
    """Saves the object to the specified path
    :param path:
    :type path: str
    :param obj: any object
    :type obj: any filetype, mostly pandas df
    :raise: Exception if there is an error in pickle saving object 
    """
    try:
        with open(path, 'wb') as f: # write bytes
            pickle.dump(obj, f)
    except Exception as err:
        print(err)

def load_file(path: str):
    """Loads the object from the specified path
    :param path:
    :type path: str
    :raise: Exception if there is an error in pickle loading object
    :returns: loaded file from specified path
    :rtype: depends on loaded file
    """
    try:
        with open(path, 'rb') as f: # read bytes
            return pickle.load(f)
    except Exception as err:
        print(err)

def generate_pairs(range: tuple, n: int) -> List[tuple]:
    """Generates a list of slow and fast MA pairs of length n
    :param range: a tuple containing the minimum and maximum bounds of possible MAs
    :type range: tuple
    :param n: number of pairs of slow and fast MAs
    :type n: int
    :returns: a list of tuples containing slow and fast MAs
    :rtype: List[tuple]
    """
    pairs = []
    while len(pairs) <= n:
        pair = random.sample(list(range(tuple[0],tuple[1])),2)
        if pair[0] == pair[1]: continue
        pairs.append((min(pair[0],pair[1]), max(pair[0],pair[1])))
    return pairs