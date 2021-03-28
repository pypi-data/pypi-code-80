
import numpy as np

#import calculate


'''
We have:
- a function to calculate angle recieves a reference(default 0, 0) and a feature coordinate
- a function that takes an angle and a pair of coordinates and rotates the point (below)
- a function that takes [del_x, del_y] and a pair of coordinates and translates the point (below)

--------------->  Y
|*
| *
|  *
|   *
|
v

X

'''

# @profile
# def arc(position, origo=np.array([0., 0.]), radians=False):
#     '''
# Returns the angle between the input coordinate and the vertical axis Y
# '''
#     rho = np.sqrt( (position[0]-origo[0])**2 + (position[1]-origo[1])**2 )
#     angle = np.arccos( (position[0]-origo[0]) / rho )
    
#     if radians==False:
#         angle = angle*180.0/np.pi
        
#     return angle

#@profile
def arc(position, origo=np.array([0., 0.]), radians=False):
    """Returns the angle between the input coordinate and the vertical 
       axis Y using the projection principle
    """

    #TODO: position[0,0] or generally position=origin should raise error
    # in fact division by rho = 0 should raise error
    position_norm = np.sqrt((position[0]-origo[0])**2 + (position[1]-origo[1])**2)
    # computing norm via np.linalg.norm(position) is much slower
    if radians==False:
        return position_norm, 180.0 * (np.arccos( (position[0]-origo[0]) / position_norm )) / np.pi
    else:
        return position_norm, np.arccos( (position[0]-origo[0]) / position_norm )


    
# apply rotation
#@profile
def rotate(position, angle, origo=np.array([0., 0.]), radians=False, discrete=True):
    #TODO: position [0,0] cannot be rotated

    rho, theta = arc(position, radians=radians)
    theta += angle
    #theta = angle + arc(position, radians=radians)

    # Use the compiled version of arc():
    # theta = angle + calculate.get_angle(position, radians=radians)

    if radians==False:
        theta = theta*(np.pi/180.0)   

    # rho now comes directly from arc()
    #rho = np.sqrt((position[0]-origo[0])**2 + (position[1]-origo[1])**2)
    
    x = rho*np.cos(theta)
    y = rho*np.sin(theta)

    if discrete:
        rotated_position = np.rint([x, y])     
        return np.array( [int(rotated_position[0]), int(rotated_position[1])] )
    else:
        return np.array( [x, y] )





