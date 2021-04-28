import os
import random

def create_temp_dir(tailor_home_path):
    temp_dir_path = os.path.join(tailor_home_path, "temp")
    if not os.path.exists(temp_dir_path): os.mkdir(temp_dir_path)
    return temp_dir_path

def create_temp_result_file(temp_dir_path):
    temp_result_file_path = os.path.join(temp_dir_path, "temp_result.txt")
    initial_temp_data = "Warnings:TIMEOUT\nRunningTime:TIMEOUT\nTotalAssertions:TIMEOUT\n"
    file = open(temp_result_file_path, "w")
    file.write(initial_temp_data)
    file.close()
    return temp_result_file_path

def read_temp_results(temp_file_path):
    results = dict()
    with open(temp_file_path, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.find("Warnings:") != -1:
                warnings = line.replace("Warnings:", "")
                results["warnings"] = warnings
            if line.find("RunningTime:") != -1:
                time = line.replace("RunningTime:", "") # This time is in milli seconds
                results["time"] = time
            if line.find("TotalAssertions:") != -1:
                total_assertions = line.replace("TotalAssertions:", "")
                results["total_assertions"] = total_assertions
    if results["warnings"] == "TIMEOUT": results["total_assertions"] = "TIMEOUT"
    return results

def pick_a_random_program(tailor_main_home):
    benchmarks = os.path.join(tailor_main_home, "benchmarks")
    for r,d,f in os.walk(benchmarks):
        picked_file = random.choice(f)
        return os.path.join(benchmarks, picked_file)

