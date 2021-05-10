  
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

from tailor.optimization_algorithms.dars.dars import dars
from tailor.optimization_algorithms.sa.sa import sa

def hc(previous_configuration, loop_step, total_optimization_iteration):
    next_configuration = dict()
    if loop_step % 10 == 0: next_configuration = dars()
    else:
        onlyModifyDomains = True if loop_step >= 10 else False
        next_configuration = sa(previous_configuration, onlyModifyDomains, loop_step, total_optimization_iteration)
    return next_configuration