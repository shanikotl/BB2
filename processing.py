from CONFIG import *


def item_dist(x, item_name=I1): # W(x)
    if item_name == I1:
        return ITEM_1_S * x + ITEM_1_b
    elif item_name == I2:
        return ITEM_2_S * x + ITEM_2_b
    else:
        return ITEM_3_S * x + ITEM_3_b


def get_work_inverse(w, item_name=I1):
    if item_name == I1:
        return (w - ITEM_1_b) / ITEM_1_S
    elif item_name == I2:
        return (w - ITEM_2_b) / ITEM_2_S
    else:
        return (w - ITEM_3_b) / ITEM_3_S


def get_delta_work(dx, item_name=I1):
    # the derivative of the function * delta time = delta work
    # TODO on In general, when function is not linear we will need the x to calculate the derivative
    # TODO in that point.
    if item_name == I1:
        return ITEM_1_S * dx
    elif item_name == I2:
        return ITEM_2_S * dx
    else:
        return ITEM_3_S * dx


def get_work_last_worker(x, item_name=I1):
    return item_dist(1, item_name) - item_dist(x, item_name)



#
#
# def get_progress(x0, w_vel, item_name=I1):
#
#      return item_dist(x + STEP_SIZE, item_name) - item_dist(x, item_name)



