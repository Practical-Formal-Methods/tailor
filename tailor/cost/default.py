import math

def default_cost_function(results, timeout):
    if results["warnings"] == "TIMEOUT": return float("inf")
    cost = float("inf") # cost intialized to inf
    timeout = float(timeout) * 1000 # Convert time out to milli seconds
    warnings = float(results["warnings"])
    time = float(results["time"])
    total_assertions = float(results["total_assertions"])
    if time > timeout: cost = float("inf")
    else:
        boostingFactor = 1000
        cost = (boostingFactor / total_assertions) * (warnings + (time/timeout))
    return cost
