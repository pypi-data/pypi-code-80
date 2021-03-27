import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree, Delaunay

# Original code provided by George Killick


def cartesian_to_polar(coordinates):

    x = coordinates[:, 0]
    y = coordinates[:, 1]
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    return np.stack([theta, rho], 1)


def polar_to_cartesian(coordinates):

    theta = coordinates[:, 0]
    rho = coordinates[:, 1]
    x = rho*np.cos(theta)
    y = rho*np.sin(theta)

    return np.stack([x, y], 1)


def display_tessellation(points, figsize=(15, 15), s=1):

    plt.figure(figsize=figsize)
    plt.scatter(points[:, 0], points[:, 1], s=s, c='black')
    plt.show()

    return


def display_stats(points, figsize=(15, 8), k=7):

    nbs = KDTree(points)

    distance, index = nbs.query(points, k=k)

    eccentricity = np.linalg.norm(points, axis=1)
    distance = 1/np.mean(distance[:, 1:], axis=1)

    distance = distance[np.argsort(eccentricity)]
    eccentricity = np.sort(eccentricity)

    plt.figure(figsize=figsize)
    plt.plot(eccentricity, distance)
    plt.xlabel("Eccentricity")
    plt.ylabel("1/mean distance to neighbours")
    plt.show()

    return


def normalize(points):

    points = cartesian_to_polar(points)
    points[:, 1] /= np.max(points[:, 1])
    points = polar_to_cartesian(points)

    return points


def randomize(points, alpha=0.25):

    x = np.copy(points)
    nbs = KDTree(x)

    distance, index = nbs.query(x, k=5)
    distance = np.mean(distance[:, 1:], axis=1)

    delta_rho = distance*np.sqrt(np.random.uniform())
    delta_theta = 2*np.random.uniform(size=distance.shape[0])*np.pi
    delta_x = delta_rho*np.cos(delta_theta)
    delta_y = delta_rho*np.sin(delta_theta)

    x[:, 0] += (delta_x*alpha)
    x[:, 1] += (delta_y*alpha)

    return normalize(x)


def point_generation(points, mode='sierpinski', concatenate=True):

    # Generates points using delaunay triangulation
    # and barycentre or sierpinski methods for generating
    # points.

    points = points
    triangulation = Delaunay(points)
    d_tri = points[triangulation.simplices]

    if(mode == 'barycentre'):
        new_points = np.sum(d_tri, axis=1)/3

    elif(mode == 'sierpinski'):

        a = (d_tri[:, 0] + d_tri[:, 1])/2
        b = (d_tri[:, 1] + d_tri[:, 2])/2
        c = (d_tri[:, 2] + d_tri[:, 0])/2

        new_points = np.concatenate((a, b, c), axis=0)
        new_points = np.unique(new_points, axis=0)

    else:
        print("Unknown mode; Choose from 'barycentre' or 'sierpinski'.")
        return None

    if(concatenate):
        new_points = np.concatenate((points, new_points), axis=0)

    return normalize(new_points)
