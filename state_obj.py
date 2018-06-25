from CONFIG import *
from processing import *


class State(object):
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self,  items_prod_line, all_items_in_queue={}):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.items_prod_line = items_prod_line
        self.rewards_states = {}
        self.items_in_queue = all_items_in_queue
        self.cycle_time = self.get_cycle_time()
        #self.available_items = np.unique([i[0] for i in all_items_in_queue.items() if i[1] > 0])

        #self.calc_rewards_for_actions()

    def get_cycle_time(self):
        last_item = self.items_prod_line[N_WORKERS-1]
        last_item_name = last_item[ITEM_NAME]
        x0 = last_item[ITEM_LOC] / N_PARTS
        v = WORKERS_POWER_DICT[N_WORKERS - 1]
        #remain_work = get_work_last_worker(last_item[ITEM_LOC] / N_PARTS, last_item_name)
        a, b = get_func_patameters(last_item_name)
        return (1 - x0)/v * (a /2. * (1 + x0) + b)


def get_arr_state(s1): # TODO why? and two going over on the same data!
    locs = []
    names = []
    #d = {}
    for k in s1.values():
        #d[k[ITEM_LOC]] = k[ITEM_NAME]
        names.append(k[ITEM_NAME])
        locs.append(k[ITEM_LOC])
    return names, locs


def divide_queues_types(visited_states, n=2):
    """
    visited_states - list - describe state:
     - items in system, with locations.
     - items in queue
     - immidiate reward
    n - number of minimum items per type
    """
    type1_states = []
    type2_states = []
    for s in visited_states:
        if len([i for i in s[1] if i[1] > n]) == 3:
            type1_states.append(s)
        else:
            type2_states.append(s)
    print len(type1_states), len(type2_states)
    return type1_states, type2_states



# def get_arr_state(s):
#     locs = []
#     names = []
#     d = {}
#     for k in np.sort(s[0].keys()):
#         locs.append(s[0][k][ITEM_LOC])
#         names.append(s[0][k][ITEM_NAME])
#         d[s[0][k][ITEM_LOC]] = s[0][k][ITEM_NAME]
#     return d