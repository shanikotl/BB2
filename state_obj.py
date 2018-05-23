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
        remain_work = get_work_last_worker(last_item[ITEM_LOC] / N_PARTS, last_item_name)
        if last_item_name == I1:
            return (remain_work - ITEM_1_b) / (ITEM_1_S * WORKERS_POWER_DICT[N_WORKERS - 1])
        elif last_item_name == I2:
            return (remain_work - ITEM_2_b) / (ITEM_2_S * WORKERS_POWER_DICT[N_WORKERS - 1])
        else:
            return (remain_work - ITEM_3_b) / (ITEM_3_S * WORKERS_POWER_DICT[N_WORKERS - 1])

    # def get_cycle_time(self):
    #     last_item = self.items_prod_line[N_WORKERS-1]
    #     last_item_name = last_item[ITEM_NAME]
    #     #remain_work = get_work_last_worker( / N_PARTS, last_item_name)
    #     if last_item_name == I1:
    #         return (remain_work - ITEM_1_b) / (ITEM_1_S * WORKERS_POWER_DICT[N_WORKERS - 1])
    #     elif last_item_name == I1:
    #         return (remain_work - ITEM_2_b) / (ITEM_2_S * WORKERS_POWER_DICT[N_WORKERS - 1])
    #     else:
    #         return (remain_work - ITEM_3_b) / (ITEM_3_S * WORKERS_POWER_DICT[N_WORKERS - 1])



#     def calc_rewards_for_actions(self):
#         for action in self.available_items:
#             immidiate_reward, next_state = self.do_cycle_process(action=action)
#             self.rewards_states[action] = {REWARD: immidiate_reward, NEXT_STEP: next_state}
#
#     def do_cycle_process(self, action=I3):
#         """
#         :param self:
#         :param action:
#         :return: cycle_time = immidiate reward.
#         """
#         # add the new item to the production
#         items_prod_line = add_item_change_workers(self.items_prod_line, ITEMS_WORK_DIST_DICT, chosen_item=action)
#         # re-arrange the workers
#         workers_prod_line = workers_change_bb(self.workers_prod_line)
#         # remove the chosen item for queue
#         self.all_items_in_queue[action] -= 1
#         # run a cycle. finished when last item finish!
#         cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
#                                                                                             items_prod_line)
#         all_items_in_queue = sum_dicts(self.all_items_in_queue, items_arrive_in_process)
#         new_s = [workers_prod_line, items_prod_line, all_items_in_queue]
#         return cycle_time, new_s
#
#
# print "bye"
# # # immidiate_reward, new_state = calc_reward_per_state(state, action=I3)
#
# # immidiate_reward, new_state, chosen_action = choose_action_greedy(state)
