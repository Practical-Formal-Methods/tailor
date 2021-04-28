#!/usr/bin/env python3
import optAI


#### Run a particular configuration on a file

print("Running configuration on a file")
path_to_input_file = "/home/numair/Desktop/Progressive_AbsInt_Benchmarks/FinalBenchmarks1/curl/Batch/curl-tool_cb_prg_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc"
domains = ["as-boxes", "term-int", "pk"] 
backward = ["1", "0", "1"] # term-int without backward. The other two with backward analaysis enabled
global_settings = [2, 3, 10] # wid_delay, narr_iter, wid_jump_set
timeout = "30"  # 30 seconds
analysis_results = optAI.run_config(path_to_input_file, domains, backward, global_settings, timeout)

print("cost = " + str(analysis_results["cost"]))
print("warnings = " + str(analysis_results["warnings"]))
print("time = " + str(analysis_results["time"]) + " milli-seconds")
print("safe = " + str(analysis_results["safe"]))










#### Find the best configuration for a file
#### DARS will be used

path_to_input_file = "/home/numair/Desktop/Progressive_AbsInt_Benchmarks/FinalBenchmarks1/curl/Batch/curl-tool_cb_prg_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc"
timeout = "30"  # 30 seconds. Timeout for one iteration
iterations = 40  # optimization iterations
seed = 42
best_configuration = optAI.optimize(path_to_input_file, timeout, iterations, seed)

print(best_configuration["domains"]) # best domains
print(best_configuration["backward"]) # best backward
print(best_configuration["global_settings"]) # Best global settings. wid_delay, narr_iter, wid_jump_set 
print(best_configuration["best_safe"]) # Best safe

"""
dict best_configuration has the following structure:

            "domains"  : ['as-dis-int', 'pk', 'bool'],
            "backward" : ['0', '1', '0'],                   only pk is backward enabled
            "global_settings" : [16, 4, 0],
            "best_warnings" : 3.0,
            "best_time" : 10.2,
            "best_cost" : 900.324,
            "best_safe" : 10.0
"""