'''Calculate how many molecules of each type can be made with the atoms on hand.'''

import sys
import json

def main(argv):
    '''Main driver for program.'''
    inventory = read_data(argv[1])
    formulas = read_data(argv[2])
    counts = calculate_counts(inventory, formulas)
    show_counts(counts)

def read_data(filename):
    '''Read a JSON-formatted data file.'''
    reader = open(filename, 'r')
    result = json.load(reader)
    reader.close()
    return result

def calculate_counts(inventory, formulas):
    '''Calculate how many of each molecule can be made with inventory.'''

    counts = {}
    for name in formulas:
        counts[name] = dict_divide(inventory, formulas[name])

    return counts

def dict_divide(inventory, molecule):
    '''Calculate how much of a single molecule can be made with inventory.'''

    number = None
    for atom in molecule:
        required = molecule[atom]
        available = inventory.get(atom, 0)
        limit = available / required
        if (number is None) or (limit < number):
            number = limit

    return number

def show_counts(counts):
    '''Show how many of each kind of molecule we can make.'''

    names = counts.keys()
    names.sort()
    for name in names:
        print name, counts[name]

if __name__ == '__main__':
    main(sys.argv)
