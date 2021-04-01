import math
import time
import pyglet
import dotmap
import car_racer.config as config
from shapely.geometry import Polygon
from pyglet.gl import glTranslatef
from car_racer.tictoc import timed_function
from os.path import join, dirname


class Car:
    def __init__(self, track):
        script_dir = dirname(__file__)
        path = join(script_dir, 'car.png')
        car_image = pyglet.image.load(path)
        car_image.anchor_x = int(car_image.width / 2)
        car_image.anchor_y = int(car_image.height / 2)
        self.track = track
        self.car = pyglet.sprite.Sprite(car_image, group=config.car_group, batch=config.batch, x=car_image.width)
        self.car.rotation = track.segments[0].coordinates[0].angle + 90
        self.accelerate = 0
        self.previous_direction = dotmap.DotMap(x=0, y=0, rotation=self.car.rotation)
        self.rolling = True
        self.drifting = False
        self.speed = 0
        self.speed_label = pyglet.text.Label(f"{round(self.speed * 21.6, 2)} km/h",
                                             font_name='Arial',
                                             font_size=12, color=(0, 0, 0, 255),
                                             x=self.car.x + config.window.width//2 - 50,
                                             y=self.car.y - config.window.height//2 + 100,
                                             anchor_x='right', anchor_y='bottom',
                                             group=config.text_group, batch=config.batch)
        self.finish_label = pyglet.text.Label("",
                                              font_name='Arial',
                                              font_size=12, color=(0, 0, 0, 255),
                                              x=self.car.x, y=self.car.y,
                                              anchor_x='center', anchor_y='center',
                                              group=config.text_group, batch=config.batch)
        self.rotation = track.segments[0].coordinates[0].angle + 90
        self.steer = 0
        self.segment = 0
        self.distance = 0
        self.checkpoints = []
        self.finish = -1
        self.stop = False
        self.started = False
        self.timer = time.monotonic()

    def __del__(self):
        self.car.delete()
        self.speed_label.delete()
        self.finish_label.delete()

    @timed_function()
    def process_next_frame(self):
        if not self.stop:
            self.calculate_speed()
            self.calculate_position()

    @timed_function()
    def rotate(self, factor):
        if self.stop or self.finish > 0:
            return
        if factor == 0:
            self.steer = 0
        else:
            self.steer += (1 / config.frames_per_second) * factor

        if abs(self.steer) > 1:
            self.steer = 1 * factor

        if self.drifting:
            self.car.rotation += factor + (self.steer * 3)
        else:
            self.car.rotation += factor + self.steer

    @timed_function()
    def calculate_speed(self):
        if self.rolling and self.speed != 0:
            self.speed += (abs(self.speed) / self.speed) / -50
            if self.speed < 0.05:
                self.speed = 0
                self.accelerate = 0
        elif not self.rolling:
            if not self.started:
                self.timer = time.monotonic()
                self.started = True
            self.speed += self.accelerate
            if self.speed >= 18:
                self.speed = 18
            elif self.speed <= -2:
                self.speed = -2

        self.speed_label.text = f"{round(self.speed * 21.6, 2)} km/h"

    @timed_function()
    def calculate_position(self):
        if self.speed == 0:
            return
        y = self.speed * math.cos(math.radians(self.car.rotation))
        x = self.speed * math.sin(math.radians(self.car.rotation))
        # if self.previous_direction.rotation != self.car.rotation:
        #    self.car.x += x + self.previous_direction.x / 5
        #    self.car.y += y + self.previous_direction.y / 5
        # else:
        self.car.x += x
        self.car.y += y
        self.previous_direction.x = x
        self.previous_direction.y = y
        self.previous_direction.rotation = self.car.rotation
        glTranslatef(-x, -y, 0)
        self.speed_label.x += x
        self.speed_label.y += y
        self.calculate_checkpoint()
        self.set_segments_visible()
        if self.calculate_collision():
            self.speed = 0
            self.stop = True

    @timed_function()
    def calculate_checkpoint(self):
        if len(self.track.segments) > self.segment + 1:
            segment = self.track.segments[self.segment + 1]
            if self.rect_distance(segment.start, Polygon(self.get_car_boundaries())) == 0:
                self.segment += 1
                self.checkpoints.append(time.monotonic() - self.timer)
                # print(f"checkpoint at {self.checkpoints[-1]}")
        else:
            segment = self.track.segments[self.segment]
            if self.rect_distance(segment.end, Polygon(self.get_car_boundaries())) == 0:
                self.finish = time.monotonic() - self.timer
                # print(f"finished in {round(self.finish, 2)} seconds")
                self.finish_label.text = f"you finished in {round(self.finish, 2)} seconds - press R to restart"
                self.finish_label.x = self.car.x
                self.finish_label.y = self.car.y

    @timed_function()
    def set_segments_visible(self):
        for segment in self.track.segments:
            if segment.id < self.segment + config.draw_distance:
                segment.group.visible = True
            else:
                segment.group.visible = False

    @timed_function()
    def calculate_collision(self):
        segment = self.track.segments[self.segment]
        car_boundaries = self.get_car_boundaries()
        car_polygon = Polygon(car_boundaries)
        for wall in segment.wall_lines:
            if self.rect_distance(wall, car_polygon) == 0:
                return True
        return False

    @timed_function()
    def rect_distance(self, obj, car_polygon):
        return car_polygon.distance(obj)

    @timed_function()
    def get_car_boundaries(self):
        rotation_radians = math.radians(self.car.rotation)
        cos_rotation = math.cos(rotation_radians)
        sin_rotation = math.sin(rotation_radians)
        img = self.car._texture
        x1 = -img.anchor_x
        y1 = -img.anchor_y
        x2 = x1 + img.width
        y2 = y1 + img.height
        x = self.car._x
        y = self.car._y
        ax = x1 * cos_rotation - y1 * sin_rotation + x
        ay = x1 * sin_rotation + y1 * cos_rotation + y
        bx = x2 * cos_rotation - y1 * sin_rotation + x
        by = x2 * sin_rotation + y1 * cos_rotation + y
        cx = x2 * cos_rotation - y2 * sin_rotation + x
        cy = x2 * sin_rotation + y2 * cos_rotation + y
        dx = x1 * cos_rotation - y2 * sin_rotation + x
        dy = x1 * sin_rotation + y2 * cos_rotation + y

        return [(ax, ay), (bx, by), (cx, cy), (dx, dy)]
