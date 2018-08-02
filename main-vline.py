#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import arange
from numpy import array
from numpy import column_stack
from numpy import cos
from numpy import linspace
from numpy import pi
from numpy import sin
from numpy import sort, reshape
from numpy import zeros
from numpy.random import randint
from numpy.random import random
from sand import Sand
from scipy.interpolate import splev
from scipy.interpolate import splprep

from fn import Fn


SIZE = 6400
EDGE = 0.08
INUM = SIZE * 10
STP = 0.000004 * 0.15
GAMMA = 1.5
BG = [1, 1, 1, 1]
FRONT = [0, 0, 0, 0.002]


class Noise(object):
    def __init__(self, points_number):
        self.points_number = points_number
        self.scale = arange(points_number).astype('float') * STP
        self.noise = zeros(points_number, 'float')

    def __next__(self): # Python 3: def __next__(self)
        r = 1.0 - 2.0 * random(self.points_number)
        self.noise[:] += r * self.scale
        return self.noise

    def __iter__(self):
        return self


class Shape(object):
    def __init__(self, points_number):
        self.points_number = points_number
        self.path = self.vertical_line()

    def vertical_line(self):
        px = zeros(self.points_number, 'float')
        py = linspace(EDGE, 1.0 - EDGE, self.points_number)
        return column_stack([px, py])

    def get_points(self):
        return self.path

    def mutate(self, noise):
        self.path += noise


def bspline_interpolate(xy, num_points=INUM):
    tck, u = splprep([xy[:, 0], xy[:, 1]], s=0)
    unew = random(num_points)
    # unew = sort(unew)
    out = splev(unew, tck)
    return column_stack(out)


def translation():
    for x in linspace(EDGE, 1.0 - EDGE, SIZE * 10):
        yield array([[x, 0.0]])


# I've no idea what this does
def mutation(points_number, noise):
    a = random(points_number) * pi * 2
    rnd = column_stack((cos(a), sin(a)))
    return rnd * reshape(noise, (points_number, 1))


def spline_iterator():
    points_number = randint(20, 40)
    print('Number of points is {}'.format(points_number))
    shape = Shape(points_number)
    noise = Noise(points_number)

    for t in translation():
        yield t + bspline_interpolate(shape.get_points())
        shape.mutate(mutation(points_number, next(noise)))


def main():
    sand = Sand(SIZE)
    sand.set_bg(BG)
    sand.set_rgba(FRONT)
    fn = Fn(prefix='./res/', postfix='.png')

    for index, spline in enumerate(spline_iterator()):
        sand.paint_dots(spline)
        if not index % SIZE:
            print('Iteration {}'.format(index))
    sand.write_to_png(fn.name(), GAMMA)


if __name__ == '__main__':
    main()
