import sys
filename = sys.argv[1]
source = open(filename, 'r')
atoms = set()
for line in source:
    name = line.strip()
    atoms.add(name)
source.close()
print atoms
