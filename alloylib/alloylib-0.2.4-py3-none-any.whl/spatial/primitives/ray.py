# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

import numpy as np

""" Representation of a Ray
"""
class Ray():

    origin: np.array        #  (3,) Origin of the Ray
    direction: np.array     #  (3,) Unit Vector describing the direction of ray from origin.


    def __init__(self, *args):
        """ Create an instance that represents Ray
        """

        self.origin = np.array([0,0,0])
        self.direction = np.array([0,0,0])

        if len(args) == 2:
            self.origin = np.array(args[0])
            self.direction = np.array(args[1])
        
        elif len(args) == 6:
            # we assume its six values, origin_x, origin_y, origin_z, vec_x, vec_y, vec_x
            self.origin = np.array([args[0],args[1],args[2]])
            self.direction = np.array([args[3], args[4], args[5]])

        else:
            # creates an empty ray
            pass

    def __str__(self):
        return "Ray - Origin:{} Direction:{}".format(self.origin, self.direction)

    def point_at_t(self, t: float) -> np.array:
        """ Return another point on the ray where it is t distance away from the origin point.
        
        Parameters
        ----------
        t : float
            scalar of direction vector
        
        Returns
        -------
        np.array
            Point on the ray that is t distance away from the origin point.
        
        Raises
        ------
        ArithmeticError
            Thrown if t is less than 0. Impossible for Ray to travel backwards.
        """
        if t < 0:
            raise ArithmeticError("t cannot be less than 0. Ray cannot travel backwards")
        else:
            return self.base + (self.direction * t)
