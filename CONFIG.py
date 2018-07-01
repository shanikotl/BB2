from collections import Counter
from scipy.stats import poisson
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import pandas as pd
import random
import math
import time
import operator


ITEMS_NAMES = [I1, I2, I3] = ["I1", "I2", "I3"]
WORKERS_NAMES = [W0, W1, W2, W3, W4] = ["w0", "w1", "w2", "w3", "w4"]


#TASKS_NAMES = [Q1, Q2, Q3, Q4, Q5] = ["q1", "q2", "q3", "q4", "q5"]
WORK_TYPES = "work_types"
WORK_UNITS = "work_units"
ITEM_NAME = "item_name"
LAST_WORKER = WORKERS_NAMES[-1]
REWARD = "reward"
NEXT_STEP = "next_state"
ITEM_LOC = "item_location"


TIME_DELTA = 0.01
N_PARTS = 40.# size will be 1/40.
STEP_SIZE = 1./N_PARTS
N_WORKERS = 5
N_CYCLES = 13517
ITEM_1_S, ITEM_1_b = 3., 2.
ITEM_2_S, ITEM_2_b = 2, 0.
ITEM_3_S, ITEM_3_b = 10., 0.


def get_func_patameters(last_item_name):
    if last_item_name == I1:
        a, b = ITEM_1_S, ITEM_1_b
    elif last_item_name == I2:
        a, b = ITEM_2_S, ITEM_2_b
    else:
        a, b = ITEM_3_S, ITEM_3_b
    return a, b

# Poisson arrival of items:
LAMB1 = 0.2
LAMB2 = 0.2
LAMB3 = 0.3
EPSILON_GREEDY = 0.9
#work for 1 unit of time, for each worker.

items_prod_line = {
        0: {ITEM_NAME: I1, ITEM_LOC: 1},
        1: {ITEM_NAME: I3, ITEM_LOC: 2},
        2: {ITEM_NAME: I3, ITEM_LOC: 5},
        3: {ITEM_NAME: I2, ITEM_LOC: 11},
        4: {ITEM_NAME: I1, ITEM_LOC: 30}
    }


WORKERS_POWER_DICT = {
    0: 0.6,
    1: 0.1,
    2: 10,
    3: 0.5,
    4: 0.7
}

WORKERS_ORDER = dict(zip(WORKERS_NAMES, range(len(WORKERS_NAMES))))

# 3 types of items: "I1", "I2", "I3"
# 5 workers: "w0", "w1", "w2", "w3", "w4"



total_lamb = float(LAMB1 + LAMB2 + LAMB3)
p_lamb1 = LAMB1 / total_lamb
p_lamb2 = LAMB2 / total_lamb
p_lamb3 = LAMB3 / total_lamb
# global lamb1
# global lamb2
# global lamb3
