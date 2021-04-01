import math
import pyglet
import car_racer.config as config
from pyglet import clock
from pyglet.window import key
from pyglet.gl import glTranslatef
from car_racer.car import Car
from car_racer.tictoc import timed_function, timed_function_statistics, tic_toc


keys = key.KeyStateHandler()
turn = 0
sleep_counter = 0
label = pyglet.text.Label("",
                          font_name='Arial',
                          font_size=36, color=(0, 0, 0, 255),
                          x=config.car.car.x, y=config.car.car.y, group=config.text_group, batch=config.batch)


@timed_function()
def on_draw(interval):
    handle_car_stop()
    key_handler()
    config.window.clear()
    if config.car.finish < 0:
        config.car.process_next_frame()
    config.batch.draw()


@timed_function()
def handle_car_stop():
    global sleep_counter, label
    if config.car.stop and sleep_counter < config.frames_per_second * 3:
        if sleep_counter % config.frames_per_second == 0:
            seconds_left = 3 - math.ceil(sleep_counter / config.frames_per_second)
            label.text = str(seconds_left)
            label.x = config.car.car.x
            label.y = config.car.car.y
        sleep_counter += 1
    elif config.car.stop:
        label.text = ""
        sleep_counter = 0
        glTranslatef(config.car.car.x, config.car.car.y, 0)
        config.car = Car(config.track)


def key_handler():
    # exit
    if keys[key.ESCAPE]:
        pyglet.app.exit()
    # acceleration and breaking
    if keys[key.UP] == keys[key.DOWN]:
        config.car.rolling = True
        config.car.accelerate = 0
    elif keys[key.UP]:
        config.car.accelerate = 0.03
        config.car.rolling = False
    elif keys[key.DOWN]:
        config.car.accelerate = -0.1
        config.car.rolling = False
    # turning
    if keys[key.RIGHT] == keys[key.LEFT]:
        config.car.rotate(0)
    elif keys[key.RIGHT]:
        config.car.rotate(1)
    elif keys[key.LEFT]:
        config.car.rotate(-1)
    if keys[key.SPACE]:
        config.car.drifting = True
    else:
        config.car.drifting = False
    # restart
    if keys[key.R] and config.car.finish > 0:
        glTranslatef(config.car.car.x, config.car.car.y, 0)
        config.car = Car(config.track)


def start_game():
    config.window.push_handlers(keys)
    width, height = config.window.get_size()
    glTranslatef((width/2), (height/2), 0)
    clock.schedule_interval(on_draw, 1 / config.frames_per_second)
    pyglet.app.run()

    # for k in tic_toc.keys():
    #     print(f"{k}: {timed_function_statistics(k)}; executions: {len(tic_toc[k])}")


if __name__ == '__main__':
    start_game()
