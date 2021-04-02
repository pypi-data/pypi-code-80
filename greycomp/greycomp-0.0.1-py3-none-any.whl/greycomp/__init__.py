import cv2
import numpy as np 
import math 
import os 
import random
from zipfile import ZipFile, ZIP_LZMA
import shutil

def compress_handler(img):
    intensity = img

    dictionary = {}
    for i in intensity:
        if i not in dictionary:
            dictionary[i] = 0
        dictionary[i] += 1

    max_intensity = max(dictionary, key=dictionary.get) 

    bit_array = []
    for i in intensity:
        if i == max_intensity:
            bit_array.append(1)
        else:
            bit_array.append(0)
    
    intensity = intensity[intensity != max_intensity]

    return np.uint8(intensity), max_intensity, bit_array

def compress(directory, image, degree, output):
    f = open(directory + '/' + image,'rb')
    file = f.read()
    img = []
    size = len(file) // 3
    for i in range(0, size):
        img.append(file[i])
    f.close()

    files = []
    img = np.array(img)

    if not os.path.exists(output):
        os.makedirs(output)

    config_dir = output + '/' + image + '_compressing'
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    for d in range(degree):
        print('Compressing ' + image + ' : ' + str(((d)/degree) * 100) + '%')

        img, max_intensity, bit_array = compress_handler(img)
        
        byte = bytearray()
        zeros = 8 - len(bit_array) % 8
        byte.append(max_intensity)
        byte.append(zeros)
        
        bit_array = [0] * zeros + bit_array

        for i in range(0, len(bit_array), 8):
            byte.append(int(''.join(str(x) for x in bit_array[i:i+8]), 2))
        
        files.append(config_dir + '/config' + str(d) + '.bin')

        f = open(config_dir + '/config' + str(d) + '.bin', 'wb')
        f.write(byte)
        f.close()
    
    files.append(config_dir + '/' + image)

    f = open(config_dir + '/' + image, 'wb')
    f.write(bytearray(img))
    f.close()
    
    with ZipFile(output + '/' + image + '.zip','w', compression = ZIP_LZMA) as zip: 
        for file in files:
            zip.write(file, file.split('/')[-1]) 

    shutil.rmtree(config_dir)

    print('Compressed ' + image + '\n')

def decompress(directory, image, output):
    with ZipFile(directory + '/' + image, 'r', compression = ZIP_LZMA) as zip: 
        files = zip.namelist()
        
        config_count = len(files) - 1

        for f in files:
            if 'config' not in f:
                image = f
                break

        image_file = zip.open(image, 'r')
        image_file = image_file.read()

        for i in range(config_count-1, -1, -1):
            print('Decompressing ' + image + ' : ' + str(((config_count - 1 - i)/config_count) * 100) + '%')

            with zip.open('config' + str(i) + '.bin') as config:
                config = config.read()
                
                max_intensity = config[0]
                zeros = config[1]
                bit_array = []

                for j in range(2, len(config)):
                    bi = '{0:08b}'.format(int(config[j]))
                    bit_array += list(bi)

                bit_array = bit_array[zeros:]
                new_image_file = []
                index = 0

                for j in bit_array:
                    if j == '1':
                        new_image_file.append(max_intensity)
                    else: 
                        new_image_file.append(image_file[index])
                        index += 1
                
                image_file = new_image_file

        if not os.path.exists(output):
            os.makedirs(output)
        
        f = open(output + '/' + image, 'wb')
        image_file = image_file + image_file + image_file
        f.write(bytearray(image_file))
        f.close()

        print('Decompressed ' + image + '\n')