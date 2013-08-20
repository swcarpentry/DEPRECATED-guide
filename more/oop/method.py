class Dinosaur(object):
    def __init__(self, my_species, my_color, my_speed):
        self.species = my_species
        self.color = my_color
        self.speed = my_speed

    def stats(self):
        return "%s %s with speed %d" % (self.color, self.species, self.speed)

cuddles = Dinosaur("Velociraptor mongoliensis", "red", 8)
print "Cuddles is a", cuddles.stats()

stumbles = Dinosaur("Saurolophus osborni", "blue", 10)
print "Stumbles is a", stumbles.stats()
