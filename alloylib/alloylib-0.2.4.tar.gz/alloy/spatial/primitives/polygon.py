# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

import numpy as np
import typing
from .line import Line
from .ray import Ray
import scipy.spatial

""" Representation of a Polygon in 3D
"""
class Polygon():

    _vertices: np.array
    _normal: np.array
    def __init__(self, points: np.array, normal: np.array = None):
        self._vertices = points
        if np.size(points,0) < 3:
            raise RuntimeError("Polygon cannot have less than 3 elements")
        if normal == None:
            # calculate the normal from the 3 of these points
            vec1 = points[1,:] - points[0,:]
            vec2 = points[2,:] - points[1,:]
            self._normal = np.cross(vec1, vec2)
        else:
            self._normal = normal
        # normalize the normal just in case 
        self._normal = self._normal/np.linalg.norm(self._normal)

    def intersect_with_line(self, line: Line) ->np.array:
        return self._intersect_with_linear(line.base, line.direction)

    def intersect_with_ray(self, ray: Ray) -> np.array:
        return self._intersect_with_linear(ray.origin, ray.direction, lambda t: t < 0)

    def _intersect_with_linear(self, base, dir, t_over_limit = None) -> np.array:

        # check whether the line is perpendicular to the polygon
        check = dir.dot(self._normal)
        if not np.isclose(check, 0):
            p1 = self._vertices[0,:]
            # check whether its behind the line
            check2 = self._normal.dot(p1 - base)
            # get there the point is along the line.
            t = check2/check
            if t_over_limit != None:
                if t_over_limit(t):
                    return None
            # the point that intersects the plane the polygon is in
            p = base + t * dir

            # merge all the points together
            all_points = np.concatenate((self._vertices, p.reshape(1,3)))

            # find the highest number in the normal
            proj_index = np.argmax(np.abs(self._normal))

            # project the points onto a basis plane by removing the proj index
            proj_all_points = np.delete(all_points, proj_index, axis=1)

            # now we run a convex hull algorithm on p, if p is not in it, then
            # we assume its not on the polygon
            # This is a hack for now, it won't work if 
            # (1) Its on the edge
            hull = scipy.spatial.ConvexHull(proj_all_points)
            if len(proj_all_points) - 1 in hull.vertices:
                return None

            return p 
        else:
            return None
