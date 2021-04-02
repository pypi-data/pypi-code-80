import ipywidgets as widgets
from traitlets import Unicode, Bool, validate, TraitError, Int, List, Dict, Float
import asyncio
from .base import Base
import re as _re
import os

_directions = [ (0, 1), (-1, 0), (0, -1), (1, 0) ]
_orient_dict = { 'E': 3, 'S': 2, 'W': 1, 'N': 0}

class Robot(object):
    def __init__(self, world, avenue = 1, street = 1, orientation = 'E', beepers = 0, index = 0):
        self._dir = _orient_dict[orientation]
        self._x = avenue
        self._y = street
        self._beeper_bag = beepers
        self._trace = None
        self._delay = 0
        self._steps = 0
        self.my_index = index
        self.world = world
        self._update_pos()
    
    def _update_pos(self):
        x, y  = self.world.cr2xy(2 * self._x - 1, 2 * self._y - 1)
        self.world.move_to(self.my_index, x,y)

    def _trace_pos(self):
        x, y  = self.world.cr2xy(2 * self._x - 1, 2 * self._y - 1)
        xr, yr =  _directions[(self._dir - 1) % 4]
        xb, yb =  _directions[(self._dir - 2) % 4]
        return x + 5 * (xr + xb), y - 5 * (yr + yb)
    
    def _update_trace(self):
        if self._trace:
            x, y = self._trace_pos()
            self.world.add_point(self.my_index, x,y)
        
    def set_trace(self, color = None):
        """Without color argument, turn off tracing.
        With color argument, start a new trace in that color."""
        if not color:
            if self._trace:
                self.world.remove_trace(self.my_index)
            self._trace = None
        else:
            x, y  = self._trace_pos()
            self.world.set_trace(self.my_index, x, y, color)
    #   self._trace = _g.Path([_g.Point(x, y)])
    #   self._trace.setBorderColor(color)
    #   _scene.add(self._trace)

    def set_pause(self, delay = 0):
        """Set a pause to be made after each move."""
        self._delay = delay
        self.world.set_pause(self.my_index, delay)

    def get_pos(self):
        """Returns current robot position."""
        return self._x, self._y
    
    def turn_left(self):
        """Rotate left by 90 degrees."""
        # self._image[self._dir].moveTo(-100, -100)
        self._dir = (self._dir + 1) % 4
        self._update_pos()
        self._update_trace()

    def move(self):
        """Move one street/avenue in direction where robot is facing."""
        if self.front_is_clear():
            xx, yy = _directions[self._dir]
            self._x += xx
            self._y += yy
        self._update_pos()
        self._update_trace()

    def front_is_clear(self):
        """Returns True if no wall or border in front of robot."""
        col = 2 * self._x - 1
        row = 2 * self._y - 1
        xx, yy = _directions[self._dir]
        return self.world.is_clear(col + xx, row + yy)

    def left_is_clear(self):
        """Returns True if no walls or borders are to the immediate left
        of the robot."""
        col = 2 * self._x - 1
        row = 2 * self._y - 1
        xx, yy = _directions[(self._dir + 1) % 4]
        return self.world.is_clear(col + xx, row + yy)

    def right_is_clear(self):
        """Returns True if no walls or borders are to the immediate right
        of the robot."""
        col = 2 * self._x - 1
        row = 2 * self._y - 1
        xx, yy = _directions[(self._dir - 1) % 4]
        return self.world.is_clear(col + xx, row + yy)

    def facing_north(self):
        """Returns True if Robot is facing north."""
        return (self._dir == 0)

def _check_world(contents):
    # safety check
    safe = contents[:]
    # only allow known keywords
    keywords = ["avenues", "streets", "walls", "beepers", "robot",
                "'s'", "'S'", '"s"', '"S"',
                "'e'", "'E'", '"e"', '"E"',
                "'w'", "'W'", '"w"', '"W"',
                "'n'", "'N'", '"n"', '"N"', ]
    for word in keywords:
        safe = safe.replace(word, '')
    safe = list(safe)
    for char in safe:
        if char.isalpha():
            raise ValueError("Invalid word or character in world file")


def load_world(filename):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, filename)
    txt = open(os.path.abspath(filename), 'r').read()
    txt = _re.sub('\r\n', '\n', str(txt))
    txt = _re.sub('\r', '\n', str(txt))
    _check_world(txt)
    try:
        robot =  None
        wd = locals()
        exec(txt, globals(), wd)

        w = Maze(
                avenues= wd["avenues"], 
                walls= wd["walls"], 
                beepers= wd["beepers"], 
                streets= wd["streets"],
                robot=wd["robot"])
        return w
    except:
        raise ValueError("Error interpreting world file.")



@widgets.register
class Maze(Base):

    # Name of the widget view class in front-end
    _view_name = Unicode('MazeView').tag(sync=True)
    # Name of the widget model class in front-end
    _model_name = Unicode('MazeModel').tag(sync=True)
    
    def __init__(self, **kwargs):
        super(Maze, self).__init__(**kwargs)
        options = {"avenues": 10, "streets": 10, "beepers": {}, "walls": [], "robot": (8, 1, 'E', 0)}
        options.update(kwargs)
        self.av = options["avenues"]
        self.st = options["streets"]
        self.robot = options["robot"] 
        self.width = self.av * 50
        self.height = self.st * 50
        self.num_cols = 2*self.av + 1
        self.num_rows = 2*self.st + 1
        self.walls = options["walls"]
        for (col, row) in self.walls:
            if not (col+row) % 2:
                raise RuntimeError("Wall in impossible position (%d, %d)." % (col,row))
        self.beepers = options["beepers"]
        self.borders = []
        self.beeper_icons = {}
        self.set_borders()
        self.robots = []
    


    def set_borders(self):
        """The world is surrounded by a continuous wall.  This function
            sets the corresponding "wall" or "border" based on the world's
            dimensions."""
        for col in range(1, self.num_cols-1, 2):
            if (col, 0) not in self.borders:
                self.borders.append( (col, 0) )
            if (col, self.num_rows) not in self.borders:
                self.borders.append( (col, self.num_rows-1) )
            for row in range(1, self.num_rows-1, 2):
                if (0, row) not in self.borders:
                    self.borders.append( (0, row) )
                if (self.num_cols, row) not in self.borders:
                    self.borders.append( (self.num_cols-1, row) )
    
    def cr2xy(self, col, row):
        x = self.left + self.ts * col
        y = self.bottom - self.ts * row
        return x, y
    
    def toggle_wall(self, col, row):
        """This function is intended for adding or removing a
            wall from a GUI world editor."""
        if (col+row) % 2 :  # safety check
            if (col, row) in self.walls: # toggle value
                self.walls.remove((col, row))
            else:
                self.walls.append((col, row))
        else:
            raise RuntimeError("Wall in impossible position (%d, %d)." % (col,row))

    def is_clear(self, col, row):
        """Returns True if there is no wall or border here."""
        return not ((col, row) in self.walls or (col, row) in self.borders)

    def create_layer(self):

        tsx =  self.width / (self.num_cols + 2)
        tsy =  self.height / (self.num_rows + 2)
        self.ts = min(tsx, tsy)
        self.left = 2 * self.ts
        self.right = self.left + 2 * self.ts * self.av
        self.bottom = self.height - 2 * self.ts
        self.top = self.bottom - 2 * self.ts * self.st

        #UI Add layer
        _beepers = [{'key':k, 'value': v} for k, v in self.beepers.items()]
        self.js_call('draw_grid', [self.width, self.height, self.av, self.st,  self.ts, self.walls, _beepers])

    def move_to(self, rindex, x, y):
        self.js_call('move_to', [rindex, x,y])
    
    def add_point(self, rindex,  x, y):
        self.js_call('add_point', [rindex, x,y])
    
    def add_robot(self, src):
        avenue, street, orientation, beepers = self.robot
        _rindex = len(self.robots)
        self.js_call('add_robot', [_rindex, src, avenue, street,orientation, beepers])
        robot = Robot(self, avenue, street, orientation, beepers, _rindex)
        self.robots.append(robot)
        return robot

    def remove_trace(self, rindex):
        self.js_call("remove_trace", [_rindex])
    
    def set_pause(self, rindex,  delay):
        self.js_call('set_pause', [rindex, delay])
    
    def set_trace(self, rindex, x,y, color):
        self.js_call('set_trace', [rindex, x, y, color])