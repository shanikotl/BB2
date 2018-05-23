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
        4: {ITEM_NAME: I1, ITEM_LOC: 30}
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
            curr_work = item_dist(curr_x_location, item_name=item_name)
            delta_work = get_delta_work(TIME_DELTA * WORKERS_POWER_DICT[w_idx], item_name=item_name)
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
    #return items_arrive_in_process



def run_mdp_on_system(policy="rand"):
    cur_state = get_first_state()
    n_inserted_items = 0
    total_time_of_system = 0
    all_processed_items = constract_finished_items_dict()
    while n_inserted_items < N_CYCLES:
        # choose what item to insert to system
        t, chosen_action = choose_action_to_move(cur_state)  #immidiate_reward = CT
        # change the workers location,
        #print "Before changing location : ", cur_state.items_prod_line
        add_item_change_workers(cur_state.items_prod_line, chosen_action)
        #print "after changing location : ", cur_state.items_prod_line
        # cycle time doesn't depand on the (immidiate) action
        cycle_time = cur_state.get_cycle_time()
        total_time_of_system += t + cycle_time
        print "cycle time %s, chosen action %s" %(cycle_time, chosen_action)
        #print "state of the last worker, << before >> cycle run:", cur_state.items_prod_line[4]
        run_one_cycle(cur_state.items_prod_line, cycle_time, cur_state.items_in_queue) # values are mutable, inplace.
        #print "state of the last worker, after cycle run:", cur_state.items_prod_line[4]
        n_inserted_items += 1
        all_processed_items[chosen_action] += 1
        #print "run number - %s, %s, %s" % (n_inserted_items, cur_state.items_in_queue, cur_state.items_prod_line)
        #cur_state = State(items_prod_line, items_in_queue)
    print "-->>> Finished processing %s items, in total time of %s" % (N_CYCLES, total_time_of_system)
    print "-->>> Processes items: %s " % all_processed_items


def get_first_state():
    items_prod_line, items_in_queue = init_production_line()
    cur_state = State(items_prod_line, items_in_queue)
    CT, chosen_action = choose_action_to_move(cur_state)
    run_one_cycle(items_prod_line, CT, items_in_queue)  # values are mutable, inplace.
    return State(items_prod_line, items_in_queue)


def choose_action_to_move(state, method="greedy"):
    available_items = [i[0] for i in state.items_in_queue.items() if i[1] > 0]
    t = 0
    if len(available_items) > 0:
        #if method == "rand":
        chosen_action = np.random.choice(available_items)
    else:
        # TODO - not necessary the right thing todo! it might be better to wait for another item..
        t = time_to_event(total_lamb)
        chosen_action = get_random_item_type()
    state.items_in_queue[chosen_action] -= 1
    return t, chosen_action

# s = get_first_state()
# print s.items_prod_line
run_mdp_on_system()
    #
    # def calc_reward_per_state(self, action=I3):
    #     """
    #     :param self:
    #     :param action:
    #     :return: cycle_time = immidiate reward.
    #     """
    #     # add the new item to the production
    #     items_prod_line = add_item_to_line(self.items_prod_line, ITEMS_WORK_DIST_DICT, chosen_item=action)
    #     # re-arrange the workers
    #     workers_prod_line = workers_change_bb(self.workers_prod_line)
    #     # remove the chosen item for queue
    #     self.all_items_in_queue[action] -= 1
    #     # run a cycle. finished when last item finish!
    #     cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
    #                                                                                         items_prod_line)
    #     all_items_in_queue = sum_dicts(self.all_items_in_queue, items_arrive_in_process)
    #     new_s = [workers_prod_line, items_prod_line, all_items_in_queue]
    #     return cycle_time, new_s

    # def calc_rewards_for_actions(self):
    #     for action in self.available_items:
    #         immidiate_reward, next_state = self.calc_reward_per_state(action=action)
    #         self.rewards_states[action] = {REWARD: immidiate_reward, NEXT_STEP: next_state}


# items_prod_line, items_in_queue = init_production_line()
# first_state = State(items_prod_line, items_in_queue)
# CT = first_state.get_cycle_time()
# k = run_one_cycle(items_prod_line, CT)
# print items_prod_line
# print k

#     last_worker_working = True
#     total_time = 0
#     time_from_prev_event = 0
#     items_arrive_in_process = constract_finished_items_dict()
#     while last_worker_working:
#         # time.sleep(delta_time)
#         total_time += TIME_DELTA
#         time_from_prev_event += TIME_DELTA
#         # generate an event, by probability.
#         alpha = random.random()
#         if alpha <= p_event(time_from_prev_event):
#             items_arrive_in_process[get_random_item_type()] += 1
#             time_from_prev_event = 0
#         # print "time from beginning of cycle: %s and workers in line: %s " % (total_time, workers_prod_line)
#         for station_idx, station in enumerate(workers_prod_line):
#             if len(station) > 0:
#                 active_worker = station[-1]
#                 item_number = workers_order[active_worker]
#                 task = items_prod_line[item_number][WORK_TYPES][station_idx]
#                 delta_work = WORKERS_POWER_DICT[active_worker][task] * TIME_DELTA
#                 items_prod_line[item_number][WORK_UNITS][station_idx] -= delta_work
#                 curr_work_units = items_prod_line[item_number][WORK_UNITS][station_idx]
#                 if curr_work_units <= 0:
#                     if (active_worker == LAST_WORKER) & (station_idx == N_STATIONS - 1):
#                         last_worker_working = False
#                         print "Last worker finished"
#                         break
#                     else:
#                         w = station.pop()  # removes the last worker in the station.
#                         workers_prod_line[station_idx + 1].insert(0, w)
#                         # worker is moving together with item she is working on.
#     #                     print workers_prod_line
#     print "total_time of cycle - %s " % total_time
#     #print "items arrivied into queue during cycle: %s" % items_arrive_in_process
#     return total_time, items_prod_line, workers_prod_line, items_arrive_in_process
