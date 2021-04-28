import os
from termcolor import colored
import pyfiglet
import argparse
import time, sys
import progressbar
import subprocess
import math
from tailor.home import get_tailor_path, get_crab_home
from tailor.utils.file_operations import create_temp_dir, create_temp_result_file, read_temp_results, pick_a_random_program
from tailor.utils.other_utils import synthesize_tailor_flags, get_basic_clam_flags, get_initial_configuration, pretty_print_configuration
from tailor.cost.default import default_cost_function
from tailor.optimization_algorithms.dars.dars import dars
from tailor.optimization_algorithms.rs.rs import random_sampling
from tailor.optimization_algorithms.hc.hc import hc
from tailor.optimization_algorithms.sa.sa import sa, acceptance_probability
import random


def parse_arguments():
    parser = argparse.ArgumentParser(description='TAILOR')
    parser.add_argument("--docker", nargs='?', const=True, default=False, help="Running in docker")
    parser.add_argument("--program", default=None, help="Program")
    parser.add_argument("--timeout", default="20", help="Timeout for one iteration")
    parser.add_argument("--iterations", default="40", help="Number of iterations")
    parser.add_argument("--algo", default="dars", help="Optimization algorithm")
    parser.add_argument("--cost", default="def", help="Cost function")
    args = vars(parser.parse_args())
    return args


def run_test():
    if DOCKER: os.system("export LD_LIBRARY_PATH=/clam/build/run/lib")
    test_file_path = os.path.join(TAILOR_HOME, "test.c")
    command = CRAB_EXECUTABLE + " --crab-do-not-print-invariants --crab-check=assert " + test_file_path
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    standard_error = p.stderr.read().decode()
    standard_output = p.stdout.read().decode()
    if standard_output == "":
        print(colored(" no output produced", "red", attrs=["bold"]))
        return False
    if standard_error.find("not found") != -1:
        print(colored(" " + standard_error, "red", attrs=["bold"]))
        return False
    return True


def accept_configuration(optimizationAlgorithm, acceptanceProb):
    if optimizationAlgorithm == "sa":
        random_bw_0_1 = random.random()
        if acceptanceProb  >= random_bw_0_1: return True
        else: return False
    else: return True

def optimize():
    best_configuration = get_initial_configuration()
    best_cost = float("inf")
    best_result = None
    previous_config = get_initial_configuration()
    previous_config_cost = float("inf")
    #for i in range(int(ITERATIONS)):
    for i in progressbar.progressbar(range(int(ITERATIONS)), redirect_stdout=True):
        if OPTIMIZATION_ALGORITHM == "dars": config = dars()
        elif OPTIMIZATION_ALGORITHM == "rs" : config = random_sampling()
        elif OPTIMIZATION_ALGORITHM == "hc": config = hc(previous_configuration=previous_config, loop_step=int(ITERATIONS) - i, total_optimization_iteration=ITERATIONS)
        elif OPTIMIZATION_ALGORITHM == "sa" : 
            onlyModifyDomains = True if i >= 10 else False
            config = sa(previous_configuration=previous_config, onlyModifyDomains=onlyModifyDomains, loop_step=int(ITERATIONS) - i, total_optimization_iteration=ITERATIONS)      
        else: 
            print(colored("ERROR: Optimzation algorithm not implemented", "red", attrs=["bold"]))
            return None, None
        #print("Iteration " + str(i+1) + ": " + colored(config, "cyan", attrs=["bold"]))
        results = run_config(config)
        if results["total_assertions"] == "0":
            print(colored("Error: No assertions in the program", "red", attrs=["bold"]))
            return None, None
        if COST_FUNCTION == "def": cost = default_cost_function(results, TIMEOUT)        
        #pretty_print_configuration(config, results)
        #print(" Cost: " + colored(cost, "yellow", attrs=["bold"]))
        acceptanceProb = acceptance_probability(previous_config_cost, cost, int(ITERATIONS) - i)
        if accept_configuration(OPTIMIZATION_ALGORITHM, acceptanceProb):
            #print(colored("CONFIG ACCEPTED", "green", attrs=["bold"]))
            previous_config = config
            previous_config_cost = cost
            # Best Configuration
            if cost < best_cost:
                #print(colored("BEST SO FAR!!! ", "white", "on_red", attrs=["bold"]))
                best_cost = cost
                best_configuration = config
                best_result = results
        else:
            #print(colored("CONFIG REJECTED", "red", attrs=["bold"]))
            pass
        #print("---------------------------------------------------")
    return best_configuration, best_result


def run_config(config):
    temp_dir_path = create_temp_dir(TAILOR_HOME)
    temp_result_file_path = create_temp_result_file(temp_dir_path)
    tailor_flags = synthesize_tailor_flags(config)
    timeout_kill = "timeout " + str(TIMEOUT) + "s "
    basic_clam_flags = get_basic_clam_flags()
    command = ""
    if DOCKER: command  = "export LD_LIBRARY_PATH=/clam/build/run/lib && "
    command += timeout_kill + CRAB_EXECUTABLE + basic_clam_flags + " " + PROGRAM + " " + tailor_flags + " --resultPath='" + temp_result_file_path + "'" 
    #print(command)
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)    
    standard_error = p.stderr.read().decode()
    standard_output = p.stdout.read().decode()
    #print(standard_output)
    results = read_temp_results(temp_result_file_path)
    return results
    

def main():    
    global DOCKER
    global CLAM
    global TAILOR_HOME
    global CRAB_HOME
    global CRAB_EXECUTABLE
    global PROGRAM
    global TIMEOUT  # timeout for one iteration
    global ITERATIONS
    global OPTIMIZATION_ALGORITHM
    global COST_FUNCTION

    os.system("clear")
    initial_text = pyfiglet.figlet_format("Tailor")
    print(colored(initial_text, "yellow", attrs=["bold"]))
    args = parse_arguments()
    # Set global variables
    DOCKER = args["docker"]
    TAILOR_HOME = get_tailor_path()
    CRAB_HOME = get_crab_home()
    TIMEOUT = args["timeout"]
    ITERATIONS = args["iterations"]
    OPTIMIZATION_ALGORITHM = args["algo"]
    COST_FUNCTION = args["cost"]
    if DOCKER: CRAB_EXECUTABLE = os.path.join(CRAB_HOME, "build", "run", "bin", "clam.py")
    else: CRAB_EXECUTABLE = os.path.join(CRAB_HOME, "build", "_DIR_", "bin", "clam.py")
    PROGRAM = args["program"]
    if PROGRAM is None: 
        print(colored(" No program provided. Picking a random program from " + os.path.join(CRAB_HOME, "benchmarks"), "blue", attrs=["bold"]))
        print(colored(" You can provide path to a program to analyze by using the --program flag", "blue", attrs=["bold"]))
        print(colored(" For example: ","blue", attrs=["bold"]) + colored("tailor --program=/path/to/program.c ", "blue", attrs=["bold"]))  
        PROGRAM = pick_a_random_program(CRAB_HOME)
    if not os.path.exists(PROGRAM):
        print(colored("Can't find ","red") + colored(PROGRAM, "yellow"))  
        return 1
    #print("")
    #print(colored(" CRAB_HOME = ", attrs=["bold"]) + colored(CRAB_HOME, "yellow", attrs=["bold"]))
    #print(colored(" CRAB_EXE = ", attrs=["bold"]) + colored(CRAB_EXECUTABLE, "yellow", attrs=["bold"]))
    print(colored(" TAILOR_HOME = ", attrs=["bold"]) + colored(TAILOR_HOME, "yellow", attrs=["bold"]))
    print(colored(" PROGRAM = ", attrs=["bold"]) + colored(PROGRAM, "yellow", attrs=["bold"]))
    print(colored(" TIMEOUT = ", attrs=["bold"]) + colored(TIMEOUT + "s", "yellow", attrs=["bold"]))
    print(colored(" ITERATIONS = ", attrs=["bold"]) + colored(ITERATIONS, "yellow", attrs=["bold"]))
    print(colored(" COST FUNCTION = ", attrs=["bold"]) + colored(COST_FUNCTION, "yellow", attrs=["bold"]))
    print(colored(" OPTIMIZATION ALGORITHM = ", attrs=["bold"]) + colored(OPTIMIZATION_ALGORITHM, "yellow", attrs=["bold"]))
    letsgo = raw_input(colored("\n Are you happy with these parameters? (y/n) ", attrs=["bold"]))    
    best_configuration = None
    if letsgo == "y":
        # Run a small test
        if not run_test():
            print(" Basic sanity check: " + colored("Failed. Are you running in a docker container?", "red", attrs=["bold"]))
            return 1
        else: print(" Basic sanity check: " + colored("success", "green", attrs=["bold"]))
        print(colored(" Optimizing CLAM configuration for this program", "magenta", attrs=["bold"]))
        best_configuration, best_result = optimize()
        if best_result is None: print(colored("Optimization failed:(  Maybe the timeout was too small", "red", attrs=["bold"]))
        if best_configuration is not None: print("\nBest Configuration: ")
        if best_configuration is not None: pretty_print_configuration(best_configuration, best_result)
        print("\n")
    else: print(colored("\nSeems like you are not happy with the global parameters\n", "red", attrs=["bold"]))

if __name__ == '__main__': signal = main()

# good example: /home/bmariano/tailor/benchmarks/git_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc