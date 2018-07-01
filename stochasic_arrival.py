from CONFIG import *


def get_arrival_times_types(total_lamb, r):
    t = 0
    cum_time_to_event = []
    for i in range(20):
        t += time_to_event(r, total_lamb)
        cum_time_to_event.append(t)
    item_types = [get_random_item_type(r) for i in range(10000)]
    # times_types_for_event = zip(cum_time_to_event, item_types)
    return cum_time_to_event, dict(Counter(item_types))


def time_to_event(r, lamb=3.):
    return -math.log(1.0 - r.rand()) / lamb


def get_random_item_type(r):
    rand_num = r.rand()
    if rand_num <= p_lamb1:
        return I1
    elif rand_num <= p_lamb1 + p_lamb2:
        return I2
    else:
        return I3


def p_event(time_to_event, lamb=LAMB1):
    return 1 - np.exp(-lamb * time_to_event)
