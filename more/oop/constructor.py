class Dinosaur(object):
    def __init__(self, my_species, my_color, my_speed):
        self.species = my_species
        self.color = my_color
        self.speed = my_speed

cuddles = Dinosaur("Velociraptor mongoliensis", "red", 8)
print "Cuddles is a", cuddles.color, cuddles.species
