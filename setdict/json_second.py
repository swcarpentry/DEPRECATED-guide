import json
original = {'Curie' : 1867, 'Hopper' : 1906, 'Franklin' : 1920}

writer = open('/tmp/example.json', 'w')
json.dump(original, writer)
writer.close()

reader = open('/tmp/example.json', 'r')
duplicate = json.load(reader)
reader.close()

print 'original:', original
print 'duplicate:', duplicate
print 'original == duplicate:', original == duplicate
print 'original is duplicate:', original is duplicate
