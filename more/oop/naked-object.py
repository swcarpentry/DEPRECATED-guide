class Dinosaur(object):
    pass

cuddles = Dinosaur()
print "type(cuddles):", type(cuddles)

cuddles.species = "Velociraptor mongoliensis"
cuddles.color = "red"
cuddles.speed = 8
print "Cuddles is a", cuddles.color, cuddles.species
