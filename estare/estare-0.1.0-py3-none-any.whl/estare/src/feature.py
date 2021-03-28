from skimage import io, data
import numpy as np
from skimage import img_as_float as imfloat
from copy import copy

# TODO: see this for sub-classing np arrays to add metadata
# https://stackoverflow.com/questions/34967273/add-metadata-comment-to-numpy-ndarray
# TODO: unit-testing


def extract(image, xRng=[0, 1], yRng=[0, 1], kapa=1.0):

    # Lower- and upper bounds for clipping the x-range
    xLB = xRng[0]
    xUB = xRng[1]

    # Lower- and upper bounds for clipping the yx-range
    yLB = yRng[0]
    yUB = yRng[1]
    
    # Clip the raw image into the region of interest
    imgClip = copy(image)

    # Find and count the pixels with maximum luminousity
    position = np.where(imgClip >= kapa)
    featureCount = position[1].size

    if featureCount > 0:
        for pair_0, pair_1 in zip(position[0], position[1]):
            if pair_0 > 3 and pair_1 > 3:
                imgClip[pair_0-4:pair_0+4, pair_1-4:pair_1+4] = 0

    return featureCount, position, imgClip


if __name__ == "__main__":

    from init import examine
    from matplotlib import pyplot as plt
    
    image = './Orion_1.jpg'
    img_as_array, x_range, y_range = examine(image, verbose=False, graphics=False)
    imgGray = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale

    fig1, (left, right) = plt.subplots(1, 2)
    left.imshow(imgGray)
    left.set_title('Raw image', fontsize=14)

    print(f'The input image has x_range = {x_range}, and y_range = {y_range}')

    numFeatures, indices, markers = extract(imgGray, xRng=[2110, 2130], yRng=[850, 870], kapa=0.9)

    imgGray[2110:2130, 850:870] = markers[:, :]

    right.imshow(imgGray)
    right.set_title('Marked features', fontsize=14)
    plt.show()
    
    print(numFeatures, indices)
