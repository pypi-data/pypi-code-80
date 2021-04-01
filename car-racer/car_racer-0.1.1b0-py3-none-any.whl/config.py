import pyglet
from dotmap import DotMap
from car_racer.track import Track
from car_racer.car import Car

window = pyglet.window.Window(800, 800)
pyglet.gl.glClearColor(1, 0.7, 0.5, 1)
car_group = pyglet.graphics.OrderedGroup(1)
wall_group = pyglet.graphics.OrderedGroup(0)
text_group = pyglet.graphics.OrderedGroup(2)
segments = []
batch = pyglet.graphics.Batch()
frames_per_second = 60
draw_distance = 10
track = Track(1, 0, DotMap(chance=70, max_angle=90))
car = Car(track)

