"""
Copyright 2021 MPI-SWS
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


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
