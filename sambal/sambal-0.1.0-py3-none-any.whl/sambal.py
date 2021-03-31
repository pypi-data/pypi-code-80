# sambal --- Sample balls, spheres, spherical caps
# Copyright © 2021 Arun I <arunisaac@systemreboot.net>
# Copyright © 2021 Murugesan Venkatapathi <murugesh@iisc.ac.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

from numpy import cos, dot, empty, log, sin, sqrt, pi
from numpy.random import default_rng
from numpy.linalg import norm

def random_on_sphere(dim, rng=default_rng()):
    """Return a random vector uniformly distributed on the unit sphere."""
    x = rng.standard_normal(dim)
    return x / norm(x)

def rotate_from_nth_canonical(x, axis):
    """Rotate vector from around the nth canonical axis to the given axis.

    """
    xn = x[-1]
    axisn = axis[-1]
    if axisn != 1:
        b = norm(axis[:-1])
        a = (dot(x, axis) - xn*axisn) / b
        s = sqrt(1 - axisn**2)
        x = x + (xn*s + a*(axisn - 1))/b * axis
        x[-1] = x[-1] + xn*(axisn - 1) - a*s \
            - axisn*(xn*s + a*(axisn - 1))/b
    return x

def random_on_disk(axis, planar_angle, rng=default_rng()):
    """Return a random vector uniformly distributed on the periphery of a
disk.

    """
    dim = axis.size
    x = empty(dim)
    x[:-1] = sin(planar_angle) * random_on_sphere(dim - 1, rng)
    x[-1] = cos(planar_angle)
    return rotate_from_nth_canonical(x, axis)

def random_on_cap(axis, maximum_planar_angle, rng=default_rng()):
    """Return a random vector uniformly distributed on a spherical
cap. The random planar angle is generated using rejection sampling.

    """
    # We apply the log function just to prevent the floats from
    # underflowing.
    dim = axis.size
    box_height = (dim-2)*log(sin(min(maximum_planar_angle, pi/2)))
    while True:
        theta = maximum_planar_angle*rng.random()
        f = box_height + log(rng.random())
        if f < (dim-2)*log(sin(theta)):
            break
    return random_on_disk(axis, theta, rng)
