from tailor.optimization_algorithms.dars.dars import dars
from tailor.optimization_algorithms.sa.sa import sa

def hc(previous_configuration, loop_step, total_optimization_iteration):
    next_configuration = dict()
    if loop_step % 10 == 0: next_configuration = dars()
    else:
        onlyModifyDomains = True if loop_step >= 10 else False
        next_configuration = sa(previous_configuration, onlyModifyDomains, loop_step, total_optimization_iteration)
    return next_configuration