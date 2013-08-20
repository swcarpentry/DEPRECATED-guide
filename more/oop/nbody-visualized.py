# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3

import sys
from math import pi
import time
from turtle import Turtle, setworldcoordinates, setup, screensize, mainloop

SOLAR_MASS = 4 * pi * pi
DAYS_PER_YEAR = 365.24

class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __div__(self, scalar):
        return self * (1. / scalar)

    def muladd(self, other, scalar):
        self.x += other.x * scalar
        self.y += other.y * scalar
        self.z += other.z * scalar

    def squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

class Body(object):
    def __init__(self, name, pos, vel, mass, color, scaling):
        self.name = name
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.scaling = scaling
        self.turtle = Turtle()
        self.turtle.speed("fastest")
        self.turtle.pencolor(color)
        self.turtle.penup()
        self.move()
        self.turtle.pendown()

    def move(self):
        x = self.pos.x * self.scaling
        y = self.pos.y * self.scaling
        self.turtle.goto((x, y))

#-------------------------------------------------------------------------------

def advance(dt, num_steps, bodies):

    for step in range(num_steps):

        for i in xrange(len(bodies)-1, -1, -1):
            for j in xrange(i-1, -1, -1):
                left = bodies[i]
                right = bodies[j]
                d_pos = left.pos - right.pos
                mag = dt * (d_pos.squared() ** -1.5)
                left_force = left.mass * mag
                right_force = right.mass * mag
                left.vel.muladd(d_pos, - right_force)
                right.vel.muladd(d_pos, left_force)

        for b in bodies:
            b.pos.muladd(b.vel, dt)
            b.move()

#-------------------------------------------------------------------------------

def total_energy(bodies):

    e = 0.0

    for i in xrange(len(bodies)-1, -1, -1):
        for j in xrange(i-1, -1, -1):
            left = bodies[i]
            right = bodies[j]
            d_pos = left.pos - right.pos
            e -= (left.mass * right.mass) / (d_pos.squared() ** 0.5)

    for b in bodies:
        e += b.mass * b.vel.squared() / 2.

    return e

#-------------------------------------------------------------------------------

def offset_momentum(ref, bodies):

    origin = Vec3(0., 0., 0.)

    for b in bodies:
        origin.muladd(b.vel, - b.mass)

    ref.vel = origin / ref.mass

#-------------------------------------------------------------------------------

half_screen_size = 150
setup(3 * half_screen_size, 3 * half_screen_size)
screensize(2 * half_screen_size, 2 * half_screen_size)
half_universe_size = 3.0e+01
scaling = half_screen_size / half_universe_size
bodies = [
    Body('Sun',
         Vec3(0.0, 0.0, 0.0),
         Vec3(0.0, 0.0, 0.0),
         1.0 * SOLAR_MASS,
         "yellow",
         scaling),

    Body('Jupiter',
         Vec3( 4.84143144246472090e+00,
              -1.16032004402742839e+00,
              -1.03622044471123109e-01),
         Vec3( 1.66007664274403694e-03 * DAYS_PER_YEAR,
               7.69901118419740425e-03 * DAYS_PER_YEAR,
             -6.90460016972063023e-05 * DAYS_PER_YEAR),
         9.54791938424326609e-04 * SOLAR_MASS,
         "green",
         scaling),

    Body('Saturn',
         Vec3( 8.34336671824457987e+00,
               4.12479856412430479e+00,
              -4.03523417114321381e-01),
         Vec3(-2.76742510726862411e-03 * DAYS_PER_YEAR,
               4.99852801234917238e-03 * DAYS_PER_YEAR,
               2.30417297573763929e-05 * DAYS_PER_YEAR),
         2.85885980666130812e-04 * SOLAR_MASS,
         "brown",
         scaling),

    Body('Uranus',
         Vec3( 1.28943695621391310e+01,
              -1.51111514016986312e+01,
              -2.23307578892655734e-01),
         Vec3( 2.96460137564761618e-03 * DAYS_PER_YEAR,
               2.37847173959480950e-03 * DAYS_PER_YEAR,
              -2.96589568540237556e-05 * DAYS_PER_YEAR),
         4.36624404335156298e-05 * SOLAR_MASS,
         "red",
         scaling),

    Body('Neptune',
         Vec3( 1.53796971148509165e+01,
              -2.59193146099879641e+01,
               1.79258772950371181e-01),
         Vec3( 2.68067772490389322e-03 * DAYS_PER_YEAR,
               1.62824170038242295e-03 * DAYS_PER_YEAR,
              -9.51592254519715870e-05 * DAYS_PER_YEAR),
         5.15138902046611451e-05 * SOLAR_MASS,
         "blue",
         scaling)
]

timesteps = int(sys.argv[1])
offset_momentum(bodies[0], bodies)
e_original = total_energy(bodies)
t_original = time.time()
advance(0.01, timesteps, bodies)
t_final = time.time()
e_final = total_energy(bodies)
d_energy = 100 * abs((e_final - e_original) / e_original)
d_time = t_final - t_original
print "%-9s: %.9f - %.9f (%f %%) / %.9f" % \
      ("Optimized", e_final, e_original, d_energy, d_time)
mainloop()
