from tailor.optimization_algorithms import clam_parameters
from  tailor.optimization_algorithms.dars import sets
from tailor.utils.other_utils import get_initial_configuration
from random import randint

def sa(previous_configuration, onlyModifyDomains, loop_step, total_optimization_iteration):
    """
        Simulated annealing optimization algorithm
        loop step is current iteration number
    """
    successful_mutation  = False
    new_configuration = []
    if onlyModifyDomains:
        if previous_configuration["dom1"] != None:
            new_configuration.append(sets.array_normalizer[previous_configuration["dom1"]])
        if previous_configuration["dom2"] != None:
            new_configuration.append(sets.array_normalizer[previous_configuration["dom2"]])    
        if previous_configuration["dom3"] != None:
            new_configuration.append(sets.array_normalizer[previous_configuration["dom3"]])
    else:
        if previous_configuration["dom1"] != None:
            new_configuration.append(previous_configuration["dom1"])
        if previous_configuration["dom2"] != None:
            new_configuration.append(previous_configuration["dom2"])    
        if previous_configuration["dom3"] != None:
            new_configuration.append(previous_configuration["dom3"])


    while(not successful_mutation and onlyModifyDomains):
        # Decide an action: 20% addition, 80% modification
        action_pool = [1,2,2,2] # 1:add, 2:modification
        action = action_pool[randint(0, len(action_pool) - 1)]

        # Line 15,16,17 in Algo 1 in the paper
        maxLength = 1
        if total_optimization_iteration <= 80:
            if loop_step < 70:
                maxLength = 2
            if loop_step < 50:
                maxLength = 3
        
        if total_optimization_iteration <= 40:
            if loop_step < 35:
                maxLength = 2
            if loop_step < 25:
                maxLength = 3
        maxLength = 3
        if action == 1 and len(new_configuration) < maxLength :
            # ADDTION
            # add the LEAST IN-COMPARABLE DOMAIN
            candidate_domains = sets.get_addition_candidate_domains_for_mutation_algo(new_configuration)
            if len(candidate_domains) > 0:
                new_configuration.append(candidate_domains[randint(0, len(candidate_domains) - 1)])
                successful_mutation = True
        else:
            # Modificaiton
            # First decide a modification location
            mod_loc = randint(0, len(new_configuration) - 1)
            # Decide a sub-action: 
            # 1: higher in the lattice  50%
            # 2: lower in the lattice   30%
            # 3: some least incomparable    20%
            sub_action_pool = [1,1,1,1,1,2,2,2,3,3]
            sub_action = sub_action_pool[randint(0, len(sub_action_pool)-1)]
            candidate_domains = []
            if sub_action == 1:
                candidate_domains = sets.one_step_higher_comparable_elements[new_configuration[mod_loc]]
                # Take difference from the current configuraiton
                candidate_domains = sets.set_difference(candidate_domains, new_configuration)
            if sub_action == 2: 
                candidate_domains = sets.one_step_lower_comparable_elements[new_configuration[mod_loc]]
                # Take difference from the current configuraiton
                candidate_domains = sets.set_difference(candidate_domains, new_configuration)
                # Check that the candidate_domains set does not contain an element that is lower_comaprable to any
                # element in new_configuration   
                lower_comparable_union = sets.get_lower_comparable_domains(new_configuration)
                candidate_domains = sets.set_difference(candidate_domains, lower_comparable_union)
            if sub_action == 3:
                candidate_domains = sets.get_addition_candidate_domains_for_mutation_algo(new_configuration)
            if len(candidate_domains) > 0 :
                new_configuration[mod_loc] = candidate_domains[randint(0, len(candidate_domains) - 1)]
                successful_mutation = True

    parameters = dict()
    parameters["domains"] = len(new_configuration)
    parameters["back1"] = previous_configuration["back1"]
    parameters["back2"] = previous_configuration["back2"]
    parameters["back3"] = previous_configuration["back3"]
    parameters["wid_delay"] = previous_configuration["wid_delay"]
    parameters["narr_iter"] = previous_configuration["narr_iter"]
    parameters["wid_jump_set"] = previous_configuration["wid_jump_set"]

    # Mutate global + local parameters
    if(not onlyModifyDomains):
        # Random Array Flipping
        for i in range(0, len(new_configuration) - 1) :
            new_configuration[i] = new_configuration[i] if randint(0,1) == 0 else sets.array_flip[new_configuration[i]]
        parameters["back1"] = randint(0,1)
        parameters["back2"] = randint(0,1)
        parameters["back3"] = randint(0,1)
        parameters["wid_delay"] = clam_parameters.WIDENING_DELAYS[randint(0, len(clam_parameters.WIDENING_DELAYS)-1)]
        parameters["narr_iter"] = clam_parameters.NARROWING_ITERATIONS[randint(0, len(clam_parameters.NARROWING_ITERATIONS)-1)]
        parameters["wid_jump_set"] = clam_parameters.WIDENING_JUMP_SETS[randint(0, len(clam_parameters.WIDENING_JUMP_SETS)-1)]

    parameters["dom1"] = new_configuration[0]
    if len(new_configuration) > 1:
        parameters["dom2"] = new_configuration[1]
    else:
        parameters["dom2"] = None
    if len(new_configuration) > 2:
        parameters["dom3"] = new_configuration[2]
    else:
        parameters["dom3"] = None
    # some sanity checks
    if len(new_configuration) == 1 :
        assert(parameters["dom1"] is not None)
    if len(new_configuration) == 2 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
    if len(new_configuration) == 3 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
        assert(parameters["dom3"] is not None)

    return parameters



def acceptance_probability(previousConfigCost, newConfigurationCost, NumberOfSteps):
    """
        e = previous config
        e' = new config
        T = NumberOfSteps
        *  Implementation of P(e, e', T).
        *  The probability of making a transition from the current state s
        *  to a candidate state s' is specified by the acceptance probability P().
        *  e  ==> getCost(s)
        *  e' ==> getCost(s')
        *  T  ==> Temperature      [number of steps/iterations in our setting].
        * 
        * s and s' are configurations in our setting.
        * 
        * According to the kirkpatrick 1983 paper:
        *   P(e, e', T) =  1                            if e' < e
        *                  exp( -(e' - e) / T )      otherwise
        */
    """
    if newConfigurationCost < previousConfigCost:
        return 1
    else:
        acceptance_prob = pow(2.7, -(newConfigurationCost - previousConfigCost) / NumberOfSteps)
        return acceptance_prob