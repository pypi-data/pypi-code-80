
import copy

import numpy as np
from ...math import inverse_transformation_matrix
from .line import Line
from .ray import Ray

def _kross(p1, p2):
    return p1[0]*p2[1] - p2[0]*p1[1]


"""Representation of a 3D Box (Orient Bounding box)
"""
class Box():

    center : np.array           # Center of the box
    orientation : np.array      # Orientation of the Box
    half_extents: np.array      # Half extense
    length : float              # Length of the box
    width : float               # Width of the box
    height : float              # Height of the box


    def __init__(self, *args):

        self.length = 0 # X-axis 
        self.width = 0 # Y-axis
        self.height = 0 # Z-axis
        self.half_extents = np.zeros((3,))

        # Default orientation is axis aligned
        self.orientation = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,1],
        ])

        if len(args) == 2:
            # we assume its two 3D points (min and max)
            self._create_from_points(args[0], args[1])
            
        elif len(args) == 6 or len(args) == 9:
            # we assume its six values, center_x, center_y, center_z, length, width and height 
            self.center = np.array([args[0],args[1],args[2]])
            self.length = args[3]
            self.half_extents[0] = args[3]/2.0
            self.width = args[4]
            self.half_extents[1] = args[4]/2.0
            self.height = args[5]
            self.half_extents[2] = args[5]/2.0

            if len(args) == 9:
                self.orientation[0, :] = args[6]
                self.orientation[1, :] = args[7]
                self.orientation[2, :] = args[8]
        
        else:
            # creates an empty box
            pass

    def __str__(self):
        exp = "Box -\tCenter:{}".format(self.center)
        exp += "\nOrieintation:\n{}".format(self.orientation)
        exp += "\nlength(x):{} width(y):{} height(z):{}".format(self.length, self.width, self.height)
        return exp

    def _create_from_points(self, min_points, max_points):

        min_points = np.array(min_points)
        max_points = np.array(max_points)
        diff = max_points - min_points

        self.center = min_points + (diff/2)
        self.length = diff[0]
        self.half_extents[0] = diff[0]/2
        self.width = diff[1]
        self.half_extents[1] = diff[1]/2
        self.height = diff[2]
        self.half_extents[2] = diff[2]/2

    @staticmethod
    def inflate_box(curr_box: 'Box', length: float = 0, width: float = 0, height: float = 0) -> 'Box':
        """Return a new inflated box according to the sizes.

        """

        box = copy.deepcopy(curr_box)
        box.length += length
        box.half_extents[0] += length/2
        box.width += width
        box.half_extents[1] += width/2
        box.height += height
        box.half_extents[2] += height/2

        return box


    def contains_point(self, point: np.array) -> bool:

        # change point to T format
        if np.size(point, 0) == 3:
            new_point = np.ones((4,))
            new_point[0:3] = point
            point = new_point
        elif np.size(point, 0) != 4:
            raise AttributeError("point not the correct size")

        # create the transformation matrix
        T = np.eye(4)
        T[0:3, 0:3] = self.orientation.T
        T[0:3, 3] = self.center

        T_inverse = inverse_transformation_matrix(T)
        corrected_point = T_inverse.dot(point)
        abs_corrected_point = np.abs(corrected_point)

        return np.all(np.less_equal(abs_corrected_point[0:3], self.half_extents))
    


    def distance_from_point(self, point: np.array):
        """ Algorithm from Ch. 10 - Geometric tools for computer graphics (2003)
        """
        
        # change point to T format
        if np.size(point, 0) == 3:
            new_point = np.ones((4,))
            new_point[0:3] = point
            point = new_point

        # create the transformation matrix
        T = np.eye(4)
        T[0:3, 0:3] = self.orientation.T
        T[0:3, 3] = self.center

        T_inverse = inverse_transformation_matrix(T)
        corrected_point = T_inverse.dot(point)
        projected_point = np.ones((4,))

        dist_squared = 0
        dist = 0

        def _project_point_on_surface(point_on_axis, half_rect_dist_in_axis):
            
            dist = 0
            if (point_on_axis < -half_rect_dist_in_axis):
                # the point is outside of the Negative X axis
                dist = point_on_axis + half_rect_dist_in_axis # take out the distance to the box
                projected_point = -half_rect_dist_in_axis
            elif (point_on_axis > half_rect_dist_in_axis):
                # outside of Positive X
                dist = point_on_axis - half_rect_dist_in_axis
                projected_point = half_rect_dist_in_axis
            else:
                projected_point = point_on_axis        

            return projected_point, dist

        # calculate for each surface
        for i in range(0, 3):
            projected_point[i], d = _project_point_on_surface(corrected_point[i], self.half_extents[i])
            dist_squared += d * d 
        
        # retransform projected point back to normal_space
        return np.sqrt(dist_squared), (T.dot(projected_point))[0:3]

    def distance_from_line(self, line: Line):
        """ Algorithm from Ch. 10 pg. 450 - Geometric tools for computer graphics (2003)
        """

        # create the transformation matrix from base to box space
        T = np.eye(4)
        T[0:3, 0:3] = self.orientation.T
        T[0:3, 3] = self.center

        # calculate the transformation matrxi from box space to base
        T_inverse = inverse_transformation_matrix(T)

        # calculate the corrected base point in the line
        corrected_base = T_inverse.dot(np.append(line.base, 1))
        corrected_direction = T_inverse.dot(np.append(line.direction, 0))

        num_zeros = 3 - np.count_nonzero(corrected_direction[0:3])
        # if the direction is all zero, its a point in the transform space, use the point algorithm
        if num_zeros == 3:
            dist, proj_point = self.distance_from_point(line.base)
            return dist, proj_point, line.base

        original_corrected_base = np.copy(corrected_base)
        # TRICK: flip the non-zero components
        flipped_array = [False, False, False]
        for i in range(0, 3):
            if corrected_direction[i] < 0:
                flipped_array[i] = True
                corrected_direction[i] *= -1
                corrected_base[i] *= -1

        if num_zeros == 2:
            # only one of the direction is non-zero, so its perpendicular to two and parallel to third.

            def cal_parallel_to_two_components(non_zero_index):
                
                dist = np.zeros((3,))
                proj_point = np.ones((4,))
                proj_point[non_zero_index] = self.half_extents[non_zero_index]

                # loop through all axis
                for i in range(0,3):
                    # skip the non-zero axis
                    if i == non_zero_index:
                        continue
                    
                    if corrected_base[i] > self.half_extents[i]:
                        dist[i] = corrected_base[i] - self.half_extents[i]
                        proj_point[i] = self.half_extents[i]
                    elif corrected_base[i] < -self.half_extents[i]:
                        dist[i] = corrected_base[i] + self.half_extents[i]
                        proj_point[i] = -self.half_extents[i]
                    else:
                        proj_point[i] = corrected_base[i]
                
                # get the closest point on the line
                t = (self.half_extents[non_zero_index] - corrected_base[non_zero_index]) / line.direction[non_zero_index]

                return np.sqrt(np.sum(np.square(dist))), proj_point, t

            # check which element is non-zero
            for i in range(0, 3):
                if corrected_direction[i] != 0:
                    dist, proj, t = cal_parallel_to_two_components(i)
                    for i in range(0,3):
                        if flipped_array:
                            proj[i] *= -1
                    closest_line = original_corrected_base + corrected_direction * t
                    return dist, (T.dot(proj))[0:3], (T.dot(closest_line))[0:3]
        
        elif num_zeros == 1:
            # only one of the direction is ZERO. only one axis is perpendicular.

            def cal_dist_to_square(zero_index):

                # figure out the other index
                nz_idx1 = (zero_index + 1)%3
                nz_idx2 = (zero_index + 2)%3

                # setup variables
                proj_point = np.ones((4,))
                dist_squared = 0
                t_on_line = 0

                # base to half_extents
                line_to_corner = corrected_base[0:3] - self.half_extents

                # Kross product
                prod_0 = corrected_direction[nz_idx1] * line_to_corner[nz_idx2] # nz_idx2 = 0
                prod_1 = corrected_direction[nz_idx2] * line_to_corner[nz_idx1]

                # see if Kross product is negative or positive
                if prod_0 >= prod_1:
                    proj_point[nz_idx2] = self.half_extents[nz_idx2]
                    tmp = (corrected_base[nz_idx1] + self.half_extents[nz_idx1])
                    delta = prod_0 - corrected_direction[nz_idx2] * tmp
                    if delta >= 0:
                        # no intersect
                        inv_L_squared = 1.0 / (corrected_direction[nz_idx2]**2 + corrected_direction[nz_idx1]**2)
                        dist_squared += delta**2 * inv_L_squared

                        proj_point[nz_idx1] = - self.half_extents[nz_idx1]
                        t_on_line = -(corrected_direction[nz_idx2] * line_to_corner[nz_idx2] * corrected_direction[nz_idx1] + tmp) * inv_L_squared
                    else:
                        # intersects
                        inv = 1.0 / corrected_direction[nz_idx2]
                        proj_point[nz_idx1] = corrected_base[nz_idx1] - (prod_0 * inv)
                        t_on_line = - line_to_corner[nz_idx2] * inv
                else:
                    # prod_1 > prod 0:
                    proj_point[nz_idx1] = self.half_extents[nz_idx1]
                    tmp = (corrected_base[nz_idx2] + self.half_extents[nz_idx2])
                    delta = prod_0 - corrected_direction[nz_idx1] * tmp
                    if delta >= 0:
                        # no intersect
                        inv_L_squared = 1.0 / (corrected_direction[nz_idx1]**2 + corrected_direction[nz_idx2]**2)
                        dist_squared += delta**2 * inv_L_squared

                        proj_point[nz_idx2] = - self.half_extents[nz_idx2]
                        t_on_line = -(corrected_direction[nz_idx1] * line_to_corner[nz_idx1] * corrected_direction[nz_idx2] + tmp) * inv_L_squared
                    else:
                        # intersects
                        inv = 1.0 / corrected_direction[nz_idx1]
                        proj_point[nz_idx2] = corrected_base[nz_idx2] - (prod_0 * inv)
                        t_on_line = - line_to_corner[nz_idx1] * inv
                
                # handle the zero direction
                if (corrected_base[zero_index] < -self.half_extents[zero_index]):
                    # outside of the positive axis
                    delta = corrected_base[zero_index] + self.half_extents[zero_index]
                    dist_squared += delta * delta
                    proj_point[zero_index] = -self.half_extents[zero_index]
                elif (corrected_base[zero_index] > self.half_extents[zero_index]):
                    delta = corrected_base[zero_index] - self.half_extents[zero_index]
                    dist_squared += delta * delta
                    proj_point[zero_index] = self.half_extents[zero_index]    

                return np.sqrt(dist_squared), proj_point, t_on_line

            # check which element is zero
            for i in range(0, 3):
                if corrected_direction[i] == 0:
                    dist, proj, t = cal_dist_to_square(i)
                    for i in range(0,3):
                        if flipped_array:
                            proj[i] *= -1
                    closest_line = original_corrected_base + corrected_direction * t
                    return dist, (T.dot(proj))[0:3], (T.dot(closest_line))[0:3] 
        
        else:
            # non-zero case

            def cal_to_face(face_idx):

                proj_point = np.copy(corrected_base)
                dist_squared = 0
                t_on_line = 0

                # figure out the other index
                idx1 = (face_idx + 1)%3 # YY
                idx2 = (face_idx + 2)%3 # ZZ
                # face_idx = XX

                pt_plus_extent = corrected_base[0:3] + self.half_extents
                pt_minus_extent = corrected_base[0:3] - self.half_extents
                if (corrected_direction[face_idx] * pt_plus_extent[idx1] >= corrected_direction[idx1] * pt_minus_extent[face_idx]):
                    # region 0,5, or 4
                    if (corrected_direction[face_idx] * pt_plus_extent[idx2] >= corrected_direction[idx2] * pt_minus_extent[face_idx]):
                        # region 0
                        proj_point[face_idx] = self.half_extents[face_idx]
                        inv = 1.0 / corrected_direction[face_idx]
                        proj_point[idx1] -= (corrected_direction[idx1] * pt_minus_extent[face_idx] * inv)
                        proj_point[idx2] -= (corrected_direction[idx2] * pt_minus_extent[face_idx] * inv)
                        t_on_line = -pt_minus_extent[face_idx] * inv
                    else:
                        # region 4 or 5
                        l_sqr = corrected_direction[face_idx]**2 + corrected_direction[idx2]**2
                        tmp = l_sqr * pt_plus_extent[idx1] - corrected_direction[idx1] * (corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx2] * pt_plus_extent[idx2])
                        if tmp <= (2 * l_sqr * self.half_extents[idx1]):
                            # region 4
                            tmp = pt_plus_extent[idx1] - (tmp / l_sqr)
                            l_sqr += corrected_direction[idx1]**2
                            delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * tmp + corrected_direction[idx2] * pt_plus_extent[idx2]
                            t_on_line = -delta/l_sqr
                            dist_squared += pt_minus_extent[face_idx]**2 + tmp**2 + pt_plus_extent[idx2]**2 + delta * t_on_line

                            proj_point[face_idx] = self.half_extents[face_idx]
                            proj_point[idx1] = t_on_line - self.half_extents[idx1]
                            proj_point[idx2] = - self.half_extents[idx2]
                        else:
                            # region 5
                            l_sqr += corrected_direction[idx1]**2
                            delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_minus_extent[idx1] + corrected_direction[idx2] * pt_plus_extent[idx2]
                            t_on_line = -delta/l_sqr
                            dist_squared += pt_minus_extent[face_idx]**2 + pt_minus_extent[idx1]**2 + pt_plus_extent[idx2]**2 + delta * t_on_line

                            proj_point[face_idx] = self.half_extents[face_idx]
                            proj_point[idx1] = self.half_extents[idx1]
                            proj_point[idx2] = - self.half_extents[idx2]
                else:
                    if (corrected_direction[face_idx] * pt_plus_extent[idx2] >= corrected_direction[idx2] * pt_minus_extent[face_idx]):
                        # region 1 or 2
                        l_sqr = corrected_direction[face_idx]**2 + corrected_direction[idx1]**2
                        tmp = l_sqr * pt_plus_extent[idx2] - corrected_direction[idx2] * (corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_plus_extent[idx1])
                        if tmp <= (2 * l_sqr * self.half_extents[idx2]):
                            # region 2
                            tmp = pt_plus_extent[idx2] - (tmp/l_sqr)
                            l_sqr += corrected_direction[idx2]**2
                            delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_plus_extent[idx1] + corrected_direction[idx2] * tmp
                            t_on_line = -delta/l_sqr
                            dist_squared += pt_minus_extent[face_idx]**2 + pt_minus_extent[idx1]**2 + tmp * tmp + delta * t_on_line

                            proj_point[face_idx] = self.half_extents[face_idx]
                            proj_point[idx1] = - self.half_extents[idx1]
                            proj_point[idx2] = t_on_line - self.half_extents[idx2]
                        else:
                            # region 1
                            l_sqr += corrected_direction[idx2]**2
                            delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_minus_extent[idx1] + corrected_direction[idx2] * pt_plus_extent[idx2]
                            t_on_line = -delta/l_sqr
                            dist_squared += pt_minus_extent[face_idx]**2 + pt_plus_extent[idx1]**2 + pt_minus_extent[idx2]**2 + delta * t_on_line

                            proj_point[face_idx] = self.half_extents[face_idx]
                            proj_point[idx1] = - self.half_extents[idx1]
                            proj_point[idx2] = self.half_extents[idx2]
                    else:
                        l_sqr = corrected_direction[face_idx]**2 + corrected_direction[idx2]**2
                        tmp = l_sqr * pt_plus_extent[idx1] - corrected_direction[idx1] * (corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx2] * pt_plus_extent[idx2])
                        if tmp >= 0:
                            # region 4 or 5
                            if tmp <= (2 * l_sqr * self.half_extents[idx1]):
                                # region 4
                                tmp = pt_plus_extent[idx1] - (tmp / l_sqr)
                                l_sqr += corrected_direction[idx1]**2
                                delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * tmp + corrected_direction[idx2] * pt_plus_extent[idx2]
                                t_on_line = -delta/l_sqr
                                dist_squared += pt_minus_extent[face_idx]**2 + tmp**2 + pt_plus_extent[idx2]**2 + delta * t_on_line

                                proj_point[face_idx] = self.half_extents[face_idx]
                                proj_point[idx1] = t_on_line - self.half_extents[idx1]
                                proj_point[idx2] = - self.half_extents[idx2]
                            else:
                                # region 5
                                l_sqr += corrected_direction[idx1]**2
                                delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_minus_extent[idx1] + corrected_direction[idx2] * pt_plus_extent[idx2]
                                t_on_line = -delta/l_sqr
                                dist_squared += pt_minus_extent[face_idx]**2 + pt_minus_extent[idx1]**2 + pt_plus_extent[idx2]**2 + delta * t_on_line

                                proj_point[face_idx] = self.half_extents[face_idx]
                                proj_point[idx1] = self.half_extents[idx1]
                                proj_point[idx2] = - self.half_extents[idx2]

                            # RETURN
                            return np.sqrt(dist_squared), proj_point, t_on_line
                        
                        l_sqr = corrected_direction[face_idx]**2 + corrected_direction[idx1]**2
                        tmp = l_sqr * pt_plus_extent[idx2] - corrected_direction[idx2] * (corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_minus_extent[idx1])
                        if tmp >= 0:
                            if tmp <= (2 * l_sqr * self.half_extents[idx2]):
                                # region 2
                                tmp = pt_plus_extent[idx2] - (tmp/l_sqr)
                                l_sqr += corrected_direction[idx2]**2
                                delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_plus_extent[idx1] + corrected_direction[idx2] * tmp
                                t_on_line = -delta/l_sqr
                                dist_squared += pt_minus_extent[face_idx]**2 + pt_minus_extent[idx1]**2 + tmp * tmp + delta * t_on_line

                                proj_point[face_idx] = self.half_extents[face_idx]
                                proj_point[idx1] = - self.half_extents[idx1]
                                proj_point[idx2] = t_on_line - self.half_extents[idx2]
                            else:
                                # region 1
                                l_sqr += corrected_direction[idx2]**2
                                delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_minus_extent[idx1] + corrected_direction[idx2] * pt_plus_extent[idx2]
                                t_on_line = -delta/l_sqr
                                dist_squared += pt_minus_extent[face_idx]**2 + pt_plus_extent[idx1]**2 + pt_minus_extent[idx2]**2 + delta * t_on_line

                                proj_point[face_idx] = self.half_extents[face_idx]
                                proj_point[idx1] = - self.half_extents[idx1]
                                proj_point[idx2] = self.half_extents[idx2]

                            # RETURN
                            return np.sqrt(dist_squared), proj_point, t_on_line
                        
                        # region 3 
                        l_sqr += corrected_direction[idx1]**2
                        delta = corrected_direction[face_idx] * pt_minus_extent[face_idx] + corrected_direction[idx1] * pt_plus_extent[face_idx] + corrected_direction[idx2] * pt_plus_extent[idx2]
                        t_on_line = -delta/l_sqr
                        dist_squared += pt_minus_extent[face_idx]**2 +  pt_minus_extent[idx1]**2 +  pt_minus_extent[idx2]**2 + delta * t_on_line

                        proj_point[face_idx] = self.half_extents[face_idx]
                        proj_point[idx1] = - self.half_extents[idx1]
                        proj_point[idx2] = - self.half_extents[idx2]
                
                # RETURN
                return np.sqrt(dist_squared), proj_point, t_on_line


            pt_minus_extent = corrected_base[0:3]  - self.half_extents
            dx_ey = corrected_direction[0] * pt_minus_extent[1]
            dy_ex = corrected_direction[1] * pt_minus_extent[0]

            if dy_ex >= dx_ey:
                dz_ex = corrected_direction[2] * pt_minus_extent[0]
                dx_ez = corrected_direction[0] * pt_minus_extent[2]

                if dz_ex >= dx_ez:
                    dist, proj, t = cal_to_face(0)
                else:
                    dist, proj, t = cal_to_face(2)
            else:
                dz_ey = corrected_direction[2] * pt_minus_extent[1]
                dy_ez = corrected_direction[1] * pt_minus_extent[2]

                if dz_ey >= dy_ez:
                    dist, proj, t = cal_to_face(1)
                else:
                    dist, proj, t = cal_to_face(2)
        
            for i in range(0,3):
                if flipped_array[i]:
                    proj[i] *= -1
            return dist, (T.dot(proj))[0:3], t

    def distance_from_ray(self, ray: Ray):
        # implement Algorithm from Ch. 10 pg. 464 - Geometric tools for computer graphics (2003)

        l = Line(ray.origin, ray.direction)    
        dist, proj, t = self.distance_from_line(l)
        if t < 0:
            dist, proj = self.distance_from_point(ray.origin)
            return dist, proj, 0 # the closet point is the origin 
        else:
            return dist, proj, t 