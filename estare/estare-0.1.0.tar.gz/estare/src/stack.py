
from estare.src.rotate import rotate


def stack(img_1, img_2, x_range, y_range, del_x, del_y, theta, discrete=True):

    for i in range(x_range):
        for j in range(y_range):
            #uncorrected_coor = [x_array[i, j], y_array[i, j]]
            uncorrected_coor = [i-del_x, j-del_y]
            
            corrected_coor = rotate(uncorrected_coor, -theta, discrete=discrete)
            
            #x_array[i, j] = corrected_coor[0]
            #y_array[i, j] = corrected_coor[1]
            
            x_corrected = corrected_coor[0]
            y_corrected = corrected_coor[1]

            # stack +needs unittesting if the stacking algorithm is to be changed+
            #if x_array[i, j] > 0 and x_array[i, j] < x_range and y_array[i, j] > 0 and y_array[i, j] < y_range:
            #    img_1[x_array[i, j], y_array[i, j]] += img_2[i, j]   # Broadcasting to all three channels is implicit
                
            if x_corrected > 0 and x_corrected < x_range and y_corrected > 0 and y_corrected < y_range:
                img_1[x_corrected, y_corrected] += img_2[i, j]   # Broadcasting to all three channels is implicit

    return img_1
                
            
