import numpy as np



def arc(position_vector, origo=np.array([0., 0.]), radians=False):
    
    vector_size = np.size(position_vector)   
    position_matrix = np.zeros( (vector_size//2, vector_size), dtype=float)

    for i in range(vector_size//2):
        col_index = i*2
        position_matrix[i, col_index:col_index+2] = position_vector[col_index], position_vector[col_index+1] 


    sqrd_pos = np.dot(position_matrix, position_vector)
    return sqrd_pos


if __name__ == '__main__':
    pos_vec = np.array([0, 1, 2, 3, 4, 4, 6, 7])
    pos_mtx = arc(pos_vec)
    print(pos_mtx)
