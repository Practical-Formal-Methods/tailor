from random import randint
from tailor.optimization_algorithms import clam_parameters

def random_sampling():
    """
        Random Sampling
    """
    parameters = dict()
    number_of_domains = randint(1,3)
    parameters["domains"] = number_of_domains
    parameters["dom1"] = clam_parameters.USABLE_LIST_OF_DOMAINS[randint(0, len(clam_parameters.USABLE_LIST_OF_DOMAINS)-1)]
    parameters["dom2"] = clam_parameters.USABLE_LIST_OF_DOMAINS[randint(0, len(clam_parameters.USABLE_LIST_OF_DOMAINS)-1)] if number_of_domains > 1 else None
    parameters["dom3"] = clam_parameters.USABLE_LIST_OF_DOMAINS[randint(0, len(clam_parameters.USABLE_LIST_OF_DOMAINS)-1)] if number_of_domains > 2 else None
    parameters["back1"] = randint(0,1)
    parameters["back2"] = randint(0,1)
    parameters["back3"] = randint(0,1)
    parameters["wid_delay"] = clam_parameters.WIDENING_DELAYS[randint(0, len(clam_parameters.WIDENING_DELAYS)-1)]
    parameters["narr_iter"] = clam_parameters.NARROWING_ITERATIONS[randint(0, len(clam_parameters.NARROWING_ITERATIONS)-1)]
    parameters["wid_jump_set"] = clam_parameters.WIDENING_JUMP_SETS[randint(0, len(clam_parameters.WIDENING_JUMP_SETS)-1)]
    return parameters