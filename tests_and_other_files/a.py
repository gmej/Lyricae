
from random import random


d1 = {
    'a': {
        'a1': 'b1',
        'a2': 'b2',
        'a3': 'b3'},
    'b': 2
    }

#def iter_dict(dict, n):
    
def dict_iter(dictionary: dict, deep: int = 3):
    print('DEEP: ', deep)
    deep -= 1
    if(deep == 0):
        return dictionary
    for el in dictionary:
        new_items = generate_random_list()
        new_d = {}
        for item in new_items:
            new_d[item] = None  # espacio para el nuevo dict
        dictionary[el] = dict_iter(new_d, deep)
    return dictionary
          
def dict_iter_V2(dictionary: dict, deep: int = 3):
    deep -= 1
    if(deep == 0):
        return dictionary
    for el in dictionary:
        new_items = generate_random_list()
        new_d = {}
        if(deep > 1):
            for item in new_items:
                new_d[item] = None  # espacio para el nuevo dict
            dictionary[el] = dict_iter_V2(new_d, deep)
        else:
            dictionary[el] = new_items
    return dictionary
        
'''
def create_dict_iteratively(dictionary: dict, recursions_left: int = 3, subrecursions_left: int = 3):
    recursions_left -= 1
    if(recursions_left == 0):
        return dictionary
    subrecursions_left = 3
    for v in dictionary:
        subrecursions_left -= 1
        
        print(v)
        new_items = generate_random_list()
        new_dict = {}
        for el in new_items:
            new_dict[el] = None
            #dictionary[v][el] = None
        print(new_dict)
        dictionary[v] = new_dict
        create_dict_iteratively(new_dict, subrecursions_left)
'''

def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))

def generate_random_list():
    l = []
    for  i in range(0, 3):
        l.append(str(random()))
    return l

d2 = {
    'aaa': None,
    'bbbb': None,
    'cccc': None,
}
#ddd = create_dict_iteratively(d2, 3)
#ddd = dict_iter(d2, 3)
ddd = dict_iter_V2(d2, 4)
pretty(ddd)
print(ddd)