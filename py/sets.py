"""
Helper set functions for optAI
"""


ALL_DOMAINS = ['int', 'ric', 'term-int',
                'dis-int', 'term-dis-int', 'boxes',  
                'zones', 'oct', 'pk', 
                'as-int', 'as-ric', 'as-term-int', 
                'as-dis-int', 'as-term-dis-int', 'as-boxes', 
                'as-zones', 'as-oct', 'as-pk',
                'bool']


all_incomparable_elements = { 
                                "pk" : ["bool","term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "oct" : ["bool", "term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "zones" : ["bool", "term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "term-int" : ["pk", "oct", "zones", "ric", "dis-int", "boxes", "bool", "term-dis-int"],
                                "ric" : ["pk", "oct", "zones", "term-int", "dis-int", "boxes", "term-dis-int", "bool"], 
                                "dis-int" : ["pk", "oct", "zones", "term-int", "ric", "bool"],
                                "boxes" : ["pk", "oct", "term-int", "ric", "term-dis-int", "bool"],
                                "term-dis-int" : ["pk", "oct", "zones", "term-int", "ric", "boxes", "bool"],
                                "bool" : ["pk", "oct", "zones", "term-int", "int", "ric", "boxes", "dis-int", "term-dis-int"],
                                "int" : ["bool"]
                            }


lowest_incomparable_elements = {
                                "pk" : ["ric", "term-int", "dis-int", "bool"],
                                "oct" : ["ric", "term-int", "dis-int", "bool"],
                                "zones" : ["term-int", "ric", "dis-int", "bool"],
                                "term-int" : ["zones", "ric", "dis-int", "bool"],
                                "ric" : ["zones", "term-int", "dis-int", "bool"], 
                                "dis-int" : ["zones", "term-int", "ric", "bool"],
                                "boxes" : ["zones", "term-int", "ric", "term-dis-int", "bool"],
                                "term-dis-int" : ["zones", "term-int", "ric", "boxes", "bool"],
                                "bool" : ["int"],
                                "int" : ["bool"]                          
                                }


lower_comparable_elements = {
                                "pk" : ["oct", "zones", "int"],
                                "oct" : ["zones", "int"],
                                "zones" : ["int"],
                                "term-int" : ["int"],
                                "ric" : ["int"], 
                                "dis-int" : ["int"],
                                "boxes" : ["dis-int", "int"],
                                "term-dis-int" : ["dis-int", "int"],
                                "bool" : [],
                                "int" : []                          
                                }


one_step_higher_comparable_elements = {
                                "pk" : [],
                                "oct" : ["pk"],
                                "zones" : ["oct"],
                                "term-int" : [],
                                "ric" : [], 
                                "dis-int" : ["boxes", "term-dis-int"],
                                "boxes" : [],
                                "term-dis-int" : [],
                                "bool" : [],
                                "int" : ["zones", "term-int", "ric", "dis-int"]                          
                                }

one_step_lower_comparable_elements = {
                                "pk" : ["oct"],
                                "oct" : ["zones"],
                                "zones" : ["int"],
                                "term-int" : ["int"],
                                "ric" : ["int"], 
                                "dis-int" : ["int"],
                                "boxes" : ["dis-int"],
                                "term-dis-int" : ["dis-int"],
                                "bool" : [],
                                "int" : []      
                            }

all_comparable_elements = {
                                "pk" : ["oct", "zones", "int"],
                                "oct" : ["pk", "zones", "int"],
                                "zones" : ["pk", "oct", "int"],
                                "int" : ["pk", "oct", "zones", "term-int", "ric", "dis-int", "boxes", "term-dis-int"],
                                "term-int" : ["int"],
                                "ric" : ["int"],
                                "dis-int" : ["int", "boxes", "term-dis-int"],
                                "boxes" : ["dis-int", "int"],
                                "term-dis-int" : ["dis-int", "int"],
                                "bool" :  []
                        }

array_normalizer = {
                    "int" : "int",
                    "ric" : "ric",
                    "term-int" : "term-int",
                    "dis-int" : "dis-int", 
                    "term-dis-int" : "term-dis-int", 
                    "boxes" : "boxes",  
                    "zones" : "zones", 
                    "oct" : "oct", 
                    "pk" : "pk", 
                    "as-int" : "int", 
                    "as-ric" : "ric", 
                    "as-term-int" : "term-int", 
                    "as-dis-int" : "dis-int", 
                    "as-term-dis-int" : "term-dis-int", 
                    "as-boxes" : "boxes", 
                    "as-zones" : "zones", 
                    "as-oct" : "oct", 
                    "as-pk" : "pk", 
                    "bool" : "bool"
}


array_flip = {
                    "int" : "as-int",
                    "ric" : "as-ric",
                    "term-int" : "as-term-int",
                    "dis-int" : "as-dis-int", 
                    "term-dis-int" : "as-term-dis-int", 
                    "boxes" : "as-boxes",  
                    "zones" : "as-zones", 
                    "oct" : "as-oct", 
                    "pk" : "as-pk", 
                    "as-int" : "int", 
                    "as-ric" : "ric", 
                    "as-term-int" : "term-int", 
                    "as-dis-int" : "dis-int", 
                    "as-term-dis-int" : "term-dis-int", 
                    "as-boxes" : "boxes", 
                    "as-zones" : "zones", 
                    "as-oct" : "oct", 
                    "as-pk" : "pk", 
                    "bool" : "bool",
                    None : None
}


def array_smashing_domain(domain):
    if domain in ['as-int', 'as-ric', 'as-term-int', 'as-dis-int', 'as-term-dis-int', 'as-boxes', 'as-zones', 'as-oct', 'as-pk']:
        return True
    else:
        return False


def set_difference(a, b):
    return [x for x in a if x not in b]

def set_union(a, b):
    c = set_difference(b, a)
    return a + c

def get_addition_candidate_domains(currentConfiguration):
        """
            FOR RANDOM LATTICE ALGORITHM
            Given a configuration, return a set of possible next domains,
            that respect the lattice
            ALGORITHM:
                <1> : union of all incomparable elements in the current configuration
                <2> : union of all comparable elements in the current configuration
                <3> : union of <2> and current configuration
                <4> : difference of <1> and <3>
        """
        # <1>
        incomp_union = []
        for element in currentConfiguration:
            incomp_union = set_union(incomp_union, all_incomparable_elements[element])
        # <2>
        comp_union = []
        for element in currentConfiguration:
            comp_union = set_union(comp_union, all_comparable_elements[element])
        # <3>
        union_comparable_and_current_configuraiton = set_union(comp_union, currentConfiguration)
        # <4>
        candidate_domains = set_difference(incomp_union, union_comparable_and_current_configuraiton)
        return candidate_domains



def get_addition_candidate_domains_for_mutation_algo(currentConfiguration):
        """
            FOR MUTATION BASED ALGORITHMS
            Given a configuration, return a set of possible next domains,
            that respect the lattice
            ALGORITHM:
                <1> : union of all LOWEST-incomparable elements in the current configuration
                <2> : union of all LOWER-comparable elements in the current configuration
                <3> : union of <2> and current configuration
                <4> : difference of <1> and <3>
        """
        # <1>
        incomp_union = []
        for element in currentConfiguration:
            incomp_union = set_union(incomp_union, lowest_incomparable_elements[element])
        # <2>
        comp_union = []
        for element in currentConfiguration:
            comp_union = set_union(comp_union, lower_comparable_elements[element])
        # <3>
        union_comparable_and_current_configuraiton = set_union(comp_union, currentConfiguration)
        # <4>
        candidate_domains = set_difference(incomp_union, union_comparable_and_current_configuraiton)
        return candidate_domains


def get_lower_comparable_domains(currentConfiguration):
    lower_comparable_union = []
    for domain in currentConfiguration:
        lower_comparable_union = set_union(lower_comparable_union, lower_comparable_elements[domain])
    return lower_comparable_union