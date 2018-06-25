from CONFIG import *


def work_accum(x, item_name=I1): # W(x)
    a, b = get_func_patameters(item_name)
    return a * x**2 / 2. + b * x


def get_work_inverse(w, item_name=I1):
    a, b = get_func_patameters(item_name)
    return (-b + np.sqrt(b**2 + 2 * a*w)) / a


# def get_delta_work(dx, item_name=I1):
#     # the derivative of the function * delta time = delta work
#     # TODO on In general, when function is not linear we will need the x to calculate the derivative
#     # TODO in that point.
#     if item_name == I1:
#         return ITEM_1_S * dx
#     elif item_name == I2:
#         return ITEM_2_S * dx
#     else:
#         return ITEM_3_S * dx
#

def get_work_last_worker(x, item_name=I1):
    return work_accum(1, item_name) - work_accum(x, item_name)




#
#
# def get_progress(x0, w_vel, item_name=I1):
#
#      return item_dist(x + STEP_SIZE, item_name) - item_dist(x, item_name)



