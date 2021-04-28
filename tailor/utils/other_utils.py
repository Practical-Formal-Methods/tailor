from termcolor import colored

def synthesize_tailor_flags(parameters):
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
    tailor_flags = " --autoAI" + domains + list_of_domains + list_of_backwardFlags + global_variables
    return tailor_flags


def get_basic_clam_flags():
    basic_clam_flags = " --crab-check=assert --crab-do-not-print-invariants --crab-disable-warnings --crab-track=arr --crab-singleton-aliases"
    basic_clam_flags = basic_clam_flags + " --crab-heap-analysis=cs-sea-dsa --crab-do-not-store-invariants --devirt-functions=types --externalize-addr-taken-functions"
    basic_clam_flags = basic_clam_flags + " --lower-select --lower-unsigned-icmp"
    return basic_clam_flags


def get_initial_configuration():
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


def pretty_print_configuration(configuration, results=None):
    if configuration["domains"] == 1:
        print(colored(" domain1: ", attrs=["bold"]) + colored(configuration["dom1"] + " <" + str(configuration["back1"]) + ">", "yellow", attrs=["bold"])) 
    if configuration["domains"] == 2:
        print(colored(" domain1: ", attrs=["bold"]) + colored(configuration["dom1"] + " <" + str(configuration["back1"]) + ">", "yellow", attrs=["bold"]))
        print(colored(" domain2: ", attrs=["bold"]) + colored(configuration["dom2"] + " <" + str(configuration["back2"]) + ">", "yellow", attrs=["bold"]))
    if configuration["domains"] == 3:
        print(colored(" domain1: ", attrs=["bold"]) + colored(configuration["dom1"] + " <" + str(configuration["back1"]) + ">", "yellow", attrs=["bold"]))
        print(colored(" domain2: ", attrs=["bold"]) + colored(configuration["dom2"] + " <" + str(configuration["back2"]) + ">", "yellow", attrs=["bold"]))
        print(colored(" domain3: ", attrs=["bold"]) + colored(configuration["dom3"] + " <" + str(configuration["back3"]) + ">", "yellow", attrs=["bold"]))
    print(colored(" Narrowing Iterations: ", attrs=["bold"]) + colored(configuration["narr_iter"], "yellow", attrs=["bold"]))
    print(colored(" Widening Delay: ", attrs=["bold"]) + colored(configuration["wid_delay"], "yellow", attrs=["bold"]))
    print(colored(" Widening Jump Set: ", attrs=["bold"]) + colored(configuration["wid_jump_set"], "yellow", attrs=["bold"]))
    print("")
    if results is not None:
        print(" Warnings: " + colored(results["warnings"], "yellow", attrs=["bold"]))
        print(" RunningTime: " + colored(results["time"] + " ms", "yellow", attrs=["bold"]))
        print(" TotalAssertions: " + colored(results["total_assertions"], "yellow", attrs=["bold"]))