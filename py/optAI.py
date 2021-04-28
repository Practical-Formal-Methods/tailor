#!/usr/bin/env python3
import os
import random
from random import randint
import sets
import math


ALL_DOMAINS = ['int', 'ric', 'term-int',
                'dis-int', 'term-dis-int', 'boxes',  
                'zones', 'oct', 'pk',
                'as-int', 'as-ric', 'as-term-int', 
                'as-dis-int', 'as-term-dis-int', 'as-boxes', 
                'as-zones', 'as-oct', 'as-pk',
                'bool']

USABLE_LIST_OF_DOMAINS = ALL_DOMAINS
WIDENING_DELAYS = [1, 2, 4, 8, 16]
NARROWING_ITERATIONS = [1, 2, 3, 4]
WIDENING_JUMP_SETS = [0, 10, 20, 30, 40]


def dars():
    """
        Domain aware random sampling
    """
    print("################## optAI.py: Optimization strategy = LATTICE RANDOM")
    parameters = dict()
    number_of_domains = randint(1,3)
    list_of_domains = []
    list_of_domains.append(sets.array_normalizer[USABLE_LIST_OF_DOMAINS[randint(0, len(USABLE_LIST_OF_DOMAINS)-1)]])
    for i in range(1, number_of_domains):
        candidate_domains = sets.get_addition_candidate_domains(list_of_domains)
        if len(candidate_domains) > 0:
            list_of_domains.append(candidate_domains[randint(0, len(candidate_domains) - 1)])

    # Random array flip for the selected list of domains
    parameters["dom1"] = list_of_domains[0] if randint(0,1) == 0 else sets.array_flip[list_of_domains[0]]
    if len(list_of_domains) > 1:
        parameters["dom2"] = list_of_domains[1] if randint(0,1) == 0 else sets.array_flip[list_of_domains[1]]
    else:
        parameters["dom2"] = None
    if len(list_of_domains) > 2:
        parameters["dom3"] = list_of_domains[2] if randint(0,1) == 0 else sets.array_flip[list_of_domains[2]]
    else:
        parameters["dom3"] = None

    parameters["domains"] = len(list_of_domains)
    parameters["back1"] = randint(0,1)
    parameters["back2"] = randint(0,1)
    parameters["back3"] = randint(0,1)
    parameters["wid_delay"] = WIDENING_DELAYS[randint(0, len(WIDENING_DELAYS)-1)]
    parameters["narr_iter"] = NARROWING_ITERATIONS[randint(0, len(NARROWING_ITERATIONS)-1)]
    parameters["wid_jump_set"] = WIDENING_JUMP_SETS[randint(0, len(WIDENING_JUMP_SETS)-1)]

    # some sanity checks
    if len(list_of_domains) == 1 :
        assert(parameters["dom1"] is not None)
    if len(list_of_domains) == 2 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
    if len(list_of_domains) == 3 :
        assert(parameters["dom1"] is not None)
        assert(parameters["dom2"] is not None)
        assert(parameters["dom3"] is not None)
    return parameters




##############################
############## Util Functions
def argument_parser():
    import argparse
    parser = argparse.ArgumentParser(description='wrapper for optAI')
    parser.add_argument('--inputFile', help="path to input C file")
    parser.add_argument('--optAlgo', help="Optimization Algorithm")
    parser.add_argument('--timeOut', help="Time out")
    parser.add_argument('--benchmarkFolder', help="Path to benchmark folder")
    parser.add_argument('--iterations', help="number of optimization iterations")
    parser.add_argument('--debug', help="debug mode")
    parser.add_argument('--seed', help="random seed")
    args = vars(parser.parse_args())
    return args



def synthesize_optAI_flags(parameters):
    """
        inputs:
            parameters: dict()
        outputs:
            Flags that are only accepted and processed by autoAI
    """

    # ELINA PK BACKWARD ERROR
    if parameters["dom1"] == "pk" or parameters["dom1"] == "as-pk":
        parameters["back1"] = 0
    if parameters["dom2"] == "pk" or parameters["dom2"] == "as-pk":
        parameters["back2"] = 0
    if parameters["dom3"] == "pk" or parameters["dom3"] == "as-pk":
        parameters["back3"] = 0
    # Number of domains
    domains = " --domains=" + str(parameters["domains"])
    # domain names
    list_of_domains = " --dom1=" + str(parameters['dom1'])
    list_of_domains = list_of_domains + " --dom2=" + str(parameters["dom2"]) if parameters["domains"] > 1 else list_of_domains
    list_of_domains = list_of_domains + " --dom3=" + str(parameters["dom3"]) if parameters["domains"] > 2 else list_of_domains
    # backward flags for each domain
    list_of_backwardFlags = " --back1" if parameters["back1"] == 1 else ""
    list_of_backwardFlags = list_of_backwardFlags + " --back2" if parameters["back2"] == 1 and parameters["domains"] > 1 else list_of_backwardFlags
    list_of_backwardFlags = list_of_backwardFlags + " --back3" if parameters["back3"] == 1 and parameters["domains"] > 2 else list_of_backwardFlags
    # Global Variables
    global_variables = " --crab-widening-delay=" + str(parameters["wid_delay"])
    global_variables = global_variables + " --crab-narrowing-iterations=" + str(parameters["narr_iter"])
    global_variables = global_variables + " --crab-widening-jump-set=" + str(parameters["wid_jump_set"]) 

    flags = " --autoAI" + domains + list_of_domains + list_of_backwardFlags + global_variables
    return flags



def initial_configuration():
    inital_configuration = {
        "domains" : 1,
        "dom1" : "bool",
        "dom2" : None,
        "dom3" : None,
        "back1" : 1,
        "back2" : 0,
        "back3" : 0,
        "wid_delay" : 1,
        "narr_iter" : 1,
        "wid_jump_set" : 0
    }
    return inital_configuration


def get_cost(run_command, input_file_path, timeout, algo):
    """
        Run the final command and get the cost of the configuration
    """    
    input_file_path = input_file_path.replace("/", "_")
    input_file_path = input_file_path.replace(".", "_")
    result_file_name = input_file_path + "_" + algo + ".txt"
    actual_results_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), result_file_name)
    result_file_path = " --resultPath='" + actual_results_file_path + "'"
    run_command = run_command + result_file_path

    print("################## optAI.py: Sythesized Command: " + run_command)
    os.system(run_command)
    cost = math.inf # cost intialized to inf
    # Read the results
    try:
        with open(actual_results_file_path, 'r') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print("################## optAI.py: Error while opening results file")
        print(e)
        return "timeout","timeout", "timeout", "timeout"
    warnings = None
    time = None
    total_assertions = None
    for line in lines:
        if line.find("Warnings:") != -1:
            warnings = line.replace("Warnings:", "")
        if line.find("RunningTime:") != -1:
            time = line.replace("RunningTime:", "") # This time is in milli seconds
        if line.find("TotalAssertions:") != -1:
            total_assertions = line.replace("TotalAssertions:", "")
    if warnings == "TIMEOUT":
        print("THE CONFIGURATION TIMED OUT")
        os.system("rm " + actual_results_file_path)        
        return "timeout","timeout", "timeout", "timeout"
    print("################## optAI.py: WARNINGS = " + warnings)
    print("################## optAI.py: SAFE = " + str(int(total_assertions) - int(warnings)))
    print("################## optAI.py: TOTAL ASSERTIONS = " + total_assertions)
    print("################## optAI.py: TIME = " + time + " MILLI-SECONDS") # This time is in milli seconds
    # delete the temporary results file
    os.system("rm " + actual_results_file_path)
    # Compute cost
    #Convert time out to milli seconds
    timeout = float(timeout) * 1000
    warnings = float(warnings)
    time = float(time)
    total_assertions = float(total_assertions)

    if total_assertions == 0:
        print("################## optAI.py: TOTAL ASSERTIONS = 0. NO ASSERTIONS FOUND IN THIS PROGRAM")
        os.system("rm " + actual_results_file_path)
        return 0,0,0,0
    if time > timeout:
        cost = math.inf
    else:
        boostingFactor = 1000
        cost = (boostingFactor / total_assertions) * (warnings + (time/timeout))
    print("################## optAI.py: COST of the configuration = " + str(cost))
    return cost, warnings, time, total_assertions



def get_basic_clam_flags():
    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants --crab-disable-warnings --crab-track=arr --crab-singleton-aliases"
    basic_clam_flags = basic_clam_flags + " --crab-heap-analysis=cs-sea-dsa --crab-do-not-store-invariants --devirt-functions=types --externalize-addr-taken-functions"
    basic_clam_flags = basic_clam_flags + " --lower-select --lower-unsigned-icmp"
    return basic_clam_flags

def decode_config(parameters):
    domains = []
    backward = []
    global_settings = []
    domains.append(parameters["dom1"])
    backward.append(str(parameters["back1"]))
    if parameters["dom2"] is not None:
        domains.append(parameters["dom2"])
        backward.append(str(parameters["back2"]))
    if parameters["dom3"] is not None:
        domains.append(parameters["dom3"])
        backward.append(str(parameters["back3"]))
    global_settings.append(parameters["wid_delay"])
    global_settings.append(parameters["narr_iter"])
    global_settings.append(parameters["wid_jump_set"])

    return {"domains" : domains,
            "backward": backward,
            "global_settings" : global_settings
            }

########### Utils end
#######################





#######################
####### optAI API

def run_config(path_to_input_file, domains, backward, global_settings, timeout):
    analysis_results = dict()
    timeout_kill = "timeout " + timeout + "s "
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    basic_clam_flags = get_basic_clam_flags()
    # Inital run command    
    prefix_run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + path_to_input_file
    # Parameters    
    parameters = dict()
    number_of_domains = len(domains)
    parameters["domains"] = number_of_domains
    parameters["dom1"] = domains[0]
    parameters["dom2"] = domains[1] if number_of_domains > 1 else None
    parameters["dom3"] = domains[2] if number_of_domains > 2 else None
    parameters["back1"] = int(backward[0])
    parameters["back2"] = int(backward[1]) if len(backward) > 1 else 0
    parameters["back3"] = int(backward[2]) if number_of_domains > 2 else 0
    parameters["wid_delay"] = global_settings[0]
    parameters["narr_iter"] = global_settings[1]
    parameters["wid_jump_set"] = global_settings[2]
    optAIflags = synthesize_optAI_flags(parameters)
    run_command = prefix_run_command + optAIflags
    print(run_command)
    algo = "dars"
    config_cost = get_cost(run_command, path_to_input_file, timeout, algo)
    if config_cost[0] == "timeout":
        cost = math.inf
        warnings = 0
        time = math.inf
        total_assertions = 0
    else:
        cost = float(config_cost[0])
        warnings = float(config_cost[1])
        time = float(config_cost[2])
        total_assertions = float(config_cost[3])
    analysis_results["cost"] = cost
    analysis_results["warnings"] = warnings
    analysis_results["time"] = time
    analysis_results["safe"] = total_assertions - warnings
    return analysis_results

def optimize(path_to_input_file, timeout, iterations, seed):
    random.seed(seed)
    timeout_kill = "timeout " + timeout + "s "
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace("/py", "")
    path_to_clamPy = os.path.join(dir_path, "build", "_DIR_", "bin", "clam.py")
    basic_clam_flags = get_basic_clam_flags()
    prefix_run_command = timeout_kill + path_to_clamPy + basic_clam_flags + " " + path_to_input_file
    initial_optAI_flag = synthesize_optAI_flags(initial_configuration())
    initial_run_command = prefix_run_command + initial_optAI_flag
    initial_cost = get_cost(initial_run_command, path_to_input_file, timeout, "dars")
    best_warnings = 0
    best_time = 0
    best_safe = 0 
    best_config = initial_configuration()
    best_cost = math.inf
    if initial_cost[0] == "timeout":
        pass
    else:
        best_cost = float(initial_cost[0])
        best_warnings = float(initial_cost[1])
        best_time = float(initial_cost[2])
        best_safe = initial_cost[3] - best_warnings
    if initial_cost[3] == 0:
        best_configuration = decode_config(initial_configuration)
        return { 
            "domains"  : best_configuration["domains"],
            "backward" : best_configuration["backward"],
            "global_settings" : best_configuration["global_settings"],
            "best_warnings" : best_warnings,
            "best_time" : best_time,
            "best_cost" : best_cost,
            "best_safe" : best_safe
            }
    # Start iteration loop
    for loop_step in range(int(iterations), 1, -1):
        print("\n\n\n\n\noptimization iteration = " + str(loop_step))
        new_configuration = dars()
        optAIflags = synthesize_optAI_flags(new_configuration)
        run_command = prefix_run_command + optAIflags
        run_results = get_cost(run_command, path_to_input_file, timeout, "dars")
        if run_results[0] == "timeout":
            print("THIS ITERATION TIMED OUT !")
            continue
        new_configuration_cost = float(run_results[0])
        warnings = run_results[1]
        config_time = run_results[2]
        total_assertions = run_results[3]
        safe = total_assertions - warnings
        if new_configuration_cost < best_cost:
            best_cost = new_configuration_cost
            best_config = new_configuration
            best_warnings = warnings
            best_time = config_time
            best_safe = safe

    best_configuration = decode_config(best_config)
    return { 
            "domains"  : best_configuration["domains"],
            "backward" : best_configuration["backward"],
            "global_settings" : best_configuration["global_settings"],
            "best_warnings" : best_warnings,
            "best_time" : best_time,
            "best_cost" : best_cost,
            "best_safe" : best_safe
            }

####### optAI API ends
######################


def main():
    print("Please use the API")


if __name__ == '__main__':
    main()