from CONFIG import *
from stochasic_arrival import *
from utils import *
from processing import *
from state_obj import *
# update the order of items in the production line:
# this is done at the end of each cycle:
from visited_states import *
import random

def add_item_change_workers(items_prod_line, chosen_item=I3):
    """
    :param items_prod_line: dictionary, of items in the production line, with current left tasks.
    key = 1 -> worker number 1.
    :param chosen_item: what item to add to production line
    :return: update items_prod_line by changing location of the items in line + adding the new item data.
    """
    for idx in range(N_WORKERS)[1:][::-1]:
        items_prod_line[idx] = items_prod_line[idx - 1]
    items_prod_line[0] = {ITEM_NAME: chosen_item, ITEM_LOC: 0}
    #return items_prod_line


def init_production_line():
    # the last worker in each array is the one that is working. the others are blocked, waiting for her to continue.
    # worker1 works on the first item. worker2 works on the second item. workers can't change location.
    items_prod_line = {
        0: {ITEM_NAME: I1, ITEM_LOC: 2},
        1: {ITEM_NAME: I3, ITEM_LOC: 4},
        2: {ITEM_NAME: I3, ITEM_LOC: 19},
        3: {ITEM_NAME: I2, ITEM_LOC: 21},
        4: {ITEM_NAME: I1, ITEM_LOC: 40}
    }
    items_in_queue = {I1: 5, I2: 10, I3: 1}
    return items_prod_line, items_in_queue


def run_one_cycle(items_prod_line, CT, items_arrive_in_process, seed_num):
    cycle_time = 0
    n = 0
    time_from_prev_event = 0
    # during a cycle, velocities don't change.
    while cycle_time <= CT:
        r = np.random.RandomState(seed_num)
        for w_idx in range(N_WORKERS)[::-1]:
            # go over all items except the last worker
            item_d = items_prod_line[w_idx]
            item_name = item_d[ITEM_NAME]
            curr_x_location = item_d[ITEM_LOC] / N_PARTS
            curr_work = work_accum(curr_x_location, item_name=item_name)
            #delta_work = get_delta_work(TIME_DELTA * WORKERS_POWER_DICT[w_idx], item_name=item_name)
            delta_work = TIME_DELTA * WORKERS_POWER_DICT[w_idx]
            worker_new_loc = get_work_inverse(curr_work + delta_work, item_name=item_name) * N_PARTS
            # print "cycle_time is %s, worker index: %s, " \
            #       "curr_x_location - %s and worker_new_loc %s " % (cycle_time, w_idx, curr_x_location, worker_new_loc)
            if w_idx == N_WORKERS - 1: #last worker
                items_prod_line[w_idx][ITEM_LOC] = worker_new_loc
            else:
                upstream_worker_loc = items_prod_line[w_idx+1][ITEM_LOC]
                if int(worker_new_loc) >= int(upstream_worker_loc): # the stations are the integers..
                    #print ">>>>>   worker  %s is blocked.. " % (w_idx)
                    continue
                else:
                    items_prod_line[w_idx][ITEM_LOC] = worker_new_loc
        n += 1
        # add arrival of new items during the cycle..
        time_from_prev_event += TIME_DELTA
        # generate an event, by probability.
        alpha = r.rand()
        if alpha <= p_event(time_from_prev_event):
            items_arrive_in_process[get_random_item_type(r)] += 1
            time_from_prev_event = 0
        cycle_time += TIME_DELTA
        seed_num += 1
    # make the location integers (work that was done in a station will get lost..)
    for w_idx in items_prod_line.keys():
        d = int(items_prod_line[w_idx][ITEM_LOC])
        items_prod_line[w_idx][ITEM_LOC] = d
    return seed_num

def run_episode(policy="weighted_rand", n_cycles=N_CYCLES, policy_arr=None, seed_num=1):
    cur_state = get_first_state()
    n_inserted_items = 0
    total_time_of_system = 0
    all_processed_items = constract_finished_items_dict()
    visited_states = []
    while n_inserted_items < n_cycles:
        r = np.random.RandomState(seed_num)
        if n_inserted_items % 2000 == 0:
            print "Processed %s products so far" % n_inserted_items
        # choose what item to insert to system

        if n_inserted_items in [300, 1007, 2684, 8306, 8920, 9894, 10466, 11055]: #[108, 500, 1052, 4295, 5291, 6981, 7524, 10503]:

            print "n_insterted items is : %s " % (n_inserted_items)
        t, chosen_action = choose_action_to_move(cur_state, method=policy, policy_arr=policy_arr, r=r, s=n_inserted_items, seed_num=seed_num)  #immidiate_reward = CT
        if n_inserted_items in [300, 1007, 2684, 8306, 8920, 9894, 10466, 11055]: #[108, 500, 1052, 4295, 5291, 6981, 7524, 10503]:
            print "n_insterted items is : %s and chosen_action is - %s" % (n_inserted_items, chosen_action)
        # change the workers location,
        add_item_change_workers(cur_state.items_prod_line, chosen_action)
        # cycle time doesn't depand on the (immidiate) action
        cycle_time = cur_state.get_cycle_time()
        total_time_of_system += t + cycle_time
        # print "CYCLE  number - %s, cycle time %s, chosen action %s" % (n_inserted_items, cycle_time, chosen_action)
        #print "items in queue: %s " % cur_state.items_in_queue
        # print "last worker - before runing the cycle  -  ", cur_state.items_prod_line[N_WORKERS-1]
        #print "seed num before cycle run - ", seed_num
        seed_num = run_one_cycle(cur_state.items_prod_line, cycle_time, cur_state.items_in_queue, seed_num) # values are mutable, inplace.
        #print "Items arrive in process - ", cur_state.items_in_queue
        #print "seed num - ", seed_num
        #print "state of the last worker, after cycle run:", cur_state.items_prod_line[N_WORKERS-1]
        n_inserted_items += 1
        # TODO return an object. just make sure it doesn't overite..
        k = dummy_f(chosen_action)
        visited_states.append([get_arr_state(cur_state.items_prod_line), cur_state.items_in_queue.items(),
                               total_time_of_system / float(n_inserted_items), k])
        #print "chosen_action - ", chosen_action
        all_processed_items[chosen_action] += 1
        #print "run number - %s, %s, %s" % (n_inserted_items, cur_state.items_in_queue, cur_state.items_prod_line)
        #cur_state = State(items_prod_line, items_in_queue)
    print "-->>> Finished processing %s items, in total time of %s" % (n_cycles, total_time_of_system)
    print "-->>> Processes items: %s " % all_processed_items
    return visited_states, total_time_of_system, all_processed_items


def dummy_f(chosen_action):
    if chosen_action == I1:
        return 1
    elif chosen_action == I2:
        return 2
    else:
        return 3


def get_first_state():
    items_prod_line, items_in_queue = init_production_line()
    # cur_state = State(items_prod_line, items_in_queue)
    # CT, chosen_action = choose_action_to_move(cur_state, method, policy_arr)
    # run_one_cycle(items_prod_line, CT, items_in_queue)  # values are mutable, inplace.
    # return State(items_prod_line, items_in_queue)
    return State(items_prod_line, items_in_queue)


def choose_action_to_move(state, method, policy_arr, r, s=1, seed_num=100):
    available_items = []
    for i, v in state.items_in_queue.items():
        for k in range(v):
            available_items.append(i)
    t = 0
    if len(available_items) > 0:
        if policy_arr is not None:
            sim_states_idx = get_similar_states_idx(policy_arr, state)
            act = policy_arr[sim_states_idx][3]  # Make sure it's 3
            if act in available_items:
                chosen_action = act
        else:
            alpha = r.rand()
            if method == "weighted_rand":
                #r = np.random.RandomState(seed_num)
                #k = random.choice(available_items)
                #avl = available_items[:]
                #k = np.random.choice(avl)
                #k = r.choice(available_items)
                #if s in [800, 1727, 2295, 4071, 4417, 5812, 5989, 6497, 6522, 6750, 6945, 9392, 9870, 11794, 11887]:
                #     print "s is %s and k - %s and some other rand %s" % (s, k, np.random.choice(available_items))
                alpha = r.rand()
                d = dict(Counter(available_items).items())
                ss = float(np.sum(d.values()))
                p1 = d["I1"] / ss
                p2 = d["I2"] / ss

                k = rand_by_dist(p1, p2, alpha)
                if s in [300, 1007, 2684, 8306, 8920, 9894, 10466, 11055]:# [108, 500, 1052, 4295, 5291, 6981, 7524, 10503]:
                    print "p1 - %s, p2 - %s, s is %s and k - %s and some other rand %s" % (p1, p2, s, k, alpha)


                chosen_action = k
            if method == "total_rand":
                p1 = p2 = p3 = 0.333
                k = rand_by_dist(p1, p2, alpha)
                chosen_action = r.choice(np.unique(available_items))
        state.items_in_queue[chosen_action] -= 1
    else:
        # TODO - not necessary the right thing todo! it might be better to wait for another item..
        t = time_to_event(r, total_lamb)
        chosen_action = get_random_item_type(r)
    return t, chosen_action


def rand_by_dist(p1, p2, alpha):
    if alpha <= p1:
        k = I1
    elif alpha <= p1 + p2:
        k = I2
    else:
        k = I3
    return k


# s = get_first_state()
# print s.items_prod_line
visited_states, total_time_of_system, all_processed_items = run_episode()
print "hhhhhhhhhhhhhhh"
