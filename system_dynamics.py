from CONFIG import *
from stochasic_arrival import *
from utils import *
from processing import *
from state_obj import *
# update the order of items in the production line:
# this is done at the end of each cycle:


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
        0: {ITEM_NAME: I1, ITEM_LOC: 1},
        1: {ITEM_NAME: I3, ITEM_LOC: 2},
        2: {ITEM_NAME: I3, ITEM_LOC: 5},
        3: {ITEM_NAME: I2, ITEM_LOC: 11},
        4: {ITEM_NAME: I1, ITEM_LOC: 38}
    }
    items_in_queue = {I1: 1, I2: 0, I3: 1}
    return items_prod_line, items_in_queue


def run_one_cycle(items_prod_line, CT, items_arrive_in_process):
    cycle_time = 0
    n = 0
    time_from_prev_event = 0
    #items_arrive_in_process = constract_finished_items_dict()
    # during a cycle, velocities don't change.
    while cycle_time <= CT:
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
        alpha = random.random()
        if alpha <= p_event(time_from_prev_event):
            items_arrive_in_process[get_random_item_type()] += 1
            time_from_prev_event = 0
        cycle_time += TIME_DELTA
    # make the location integers (work that was done in a station will get lost..)
    for w_idx in items_prod_line.keys():
        d = int(items_prod_line[w_idx][ITEM_LOC])
        items_prod_line[w_idx][ITEM_LOC] = d


def run_episode(policy="rand"):
    cur_state = get_first_state()
    n_inserted_items = 0
    total_time_of_system = 0
    all_processed_items = constract_finished_items_dict()
    visited_states = []
    while n_inserted_items < N_CYCLES:
        # choose what item to insert to system
        t, chosen_action = choose_action_to_move(cur_state)  #immidiate_reward = CT
        # change the workers location,
        add_item_change_workers(cur_state.items_prod_line, chosen_action)
        # cycle time doesn't depand on the (immidiate) action
        cycle_time = cur_state.get_cycle_time()
        total_time_of_system += t + cycle_time
        # print "CYCLE  number - %s, cycle time %s, chosen action %s" % (n_inserted_items, cycle_time, chosen_action)
        # print "items in queue: %s " % cur_state.items_in_queue
        # print "last worker - before runing the cycle  -  ", cur_state.items_prod_line[N_WORKERS-1]
        run_one_cycle(cur_state.items_prod_line, cycle_time, cur_state.items_in_queue) # values are mutable, inplace.
        #print "state of the last worker, after cycle run:", cur_state.items_prod_line[N_WORKERS-1]
        n_inserted_items += 1
        visited_states.append([get_arr_state(cur_state.items_prod_line), cur_state.items_in_queue.items(), total_time_of_system / float(n_inserted_items)])
        if n_inserted_items==4:
            print "a"
        all_processed_items[chosen_action] += 1
        #print "run number - %s, %s, %s" % (n_inserted_items, cur_state.items_in_queue, cur_state.items_prod_line)
        #cur_state = State(items_prod_line, items_in_queue)
    print "-->>> Finished processing %s items, in total time of %s" % (N_CYCLES, total_time_of_system)
    print "-->>> Processes items: %s " % all_processed_items
    return visited_states, total_time_of_system, all_processed_items


def get_first_state():
    items_prod_line, items_in_queue = init_production_line()
    cur_state = State(items_prod_line, items_in_queue)
    CT, chosen_action = choose_action_to_move(cur_state)
    run_one_cycle(items_prod_line, CT, items_in_queue)  # values are mutable, inplace.
    return State(items_prod_line, items_in_queue)


def choose_action_to_move(state, method="greedy"):
    available_items = []
    for i, v in state.items_in_queue.items():
        for k in range(v):
            available_items.append(i)
    #[i[0] for i in state.items_in_queue.items() if i[1] > 0]
    t = 0
    if len(available_items) > 0:
        chosen_action = np.random.choice(available_items)
        state.items_in_queue[chosen_action] -= 1
    else:
        # TODO - not necessary the right thing todo! it might be better to wait for another item..
        t = time_to_event(total_lamb)
        chosen_action = get_random_item_type()
    return t, chosen_action

# s = get_first_state()
# print s.items_prod_line
visited_states, total_time_of_system, all_processed_items = run_episode()
print "hhhhhhhhhhhhhhh"
