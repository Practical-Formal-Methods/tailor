  
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

from random import randint
import sets
from tailor.optimization_algorithms import clam_parameters

def dars():
    """
        Domain aware random sampling
    """
    parameters = dict()
    number_of_domains = randint(1,3)
    list_of_domains = []
    list_of_domains.append(sets.array_normalizer[clam_parameters.USABLE_LIST_OF_DOMAINS[randint(0, len(clam_parameters.USABLE_LIST_OF_DOMAINS)-1)]])
    for i in range(1, number_of_domains):
        candidate_domains = sets.get_addition_candidate_domains(list_of_domains)
        if len(candidate_domains) > 0:
            list_of_domains.append(candidate_domains[randint(0, len(candidate_domains) - 1)])
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
    parameters["wid_delay"] = clam_parameters.WIDENING_DELAYS[randint(0, len(clam_parameters.WIDENING_DELAYS)-1)]
    parameters["narr_iter"] = clam_parameters.NARROWING_ITERATIONS[randint(0, len(clam_parameters.NARROWING_ITERATIONS)-1)]
    parameters["wid_jump_set"] = clam_parameters.WIDENING_JUMP_SETS[randint(0, len(clam_parameters.WIDENING_JUMP_SETS)-1)]

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

