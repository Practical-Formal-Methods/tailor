  
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