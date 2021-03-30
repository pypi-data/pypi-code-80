# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

import numpy as np

""" Representation of a Line
"""
class Line():

    base: np.array          #  (3,) A point on the line
    direction: np.array     #  (3,) Unit Vector describing the direction of line at base

    def __init__(self, base: np.array, dir: np.array):
        """Initialize a Line Representation
        
        Parameters
        ----------
        base : np.array
            A point on the line
        dir : np.array
            The direction that the line is going
        """
        self.base = base
        self.direction = dir/np.linalg.norm(dir)

    def __str__(self):
        return "Line - Point:{} Direction:{}".format(self.base, self.direction)

    def point_at_t(self, t: float) -> np.array:
        """Given the initialize point, return another point where it is t * direction vector away on the line
        
        Parameters
        ----------
        t : float
            scalar of direction vector
        
        Returns
        -------
        np.array
            Point on the line that is t * direction vector away from the base point.
        """
        return self.base + (self.direction * t)

    #def distance_to_point(self, point: np.array) -> (float, t):
