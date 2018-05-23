from CONFIG import *


def sum_dicts(dict1, dict2):
    """
    :param dict1: dictionary with integers as values
    :param dict2: dictionary with integers as values
    :return: dictionary, with the sum of the keys.
    """
    new_keys = np.unique(np.append(dict1.keys(), dict2.keys()))
    new_dict = {}
    for k in new_keys:
        new_dict[k] = dict1.get(k, 0) + dict2.get(k, 1)
    return new_dict


def constract_finished_items_dict():
    ks = ITEMS_NAMES
    return dict(zip(ks, np.zeros(len(ks))))


def get_round(n, r=0.2):
    if n == 0:
        return n
    n_mod = np.round(n % int(n), 2)
    gaps_arr = np.arange(0 - r, 1 + r, r)
    for i in gaps_arr:
        if n_mod <= i:
            return int(n) + np.round(i, 2)
    return
