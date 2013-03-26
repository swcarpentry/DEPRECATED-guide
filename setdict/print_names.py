# Print the name of each atom in the data file once.
reader = open('atoms.txt', 'r')
seen = set()
for line in reader:
    name = line.strip()
    if name in seen:
        print name
    else:
        seen.add(name)
reader.close()
