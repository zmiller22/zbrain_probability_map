#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:42:02 2019

@author: tracingpc1
"""
import os
import numpy as np
import numpy.random as rand
import random
import pandas as pd
import skimage as si
import time

def read_img_dir(dir_path):
    """Reads in all images located inside the specified directory as numpy arrays using
    skimage. The directory should contain only the images and all images should be in a 
    format supported by skimage"""
    
    img_directory = os.fsencode(dir_path)
    img_list = []
    
    for file in os.listdir(img_directory):
        filename = os.fsdecode(file)
        file_path = os.path.join(dir_path, filename)
        img_list.append(si.io.imread(file_path))
        
    return img_list

def get_voxel_vector(z, x, y, img_list):
    """Returns a numpy vecotr of the values contained in voxel x,y,z for each image stack
    in img_list"""
    
    vox_list = []
    
    for img in img_list:
        vox_list.append(img[z,x,y])
        
    vox_vec = np.array(vox_list)
    
    return vox_vec

# I am going to test writing this to a data file instead of reading it into a list...
# =============================================================================
# def get_voxel_data(img_list):
#     """Given a list of images (as numpy arrays), iterates through all the images in the 
#     list for each voxel in the in the images, collecting a vector of all the voxel values,
#     the mean value of the voxel, and the sd of that voxel"""
#     start = time.time()
#     
#     dims = img_list[0].shape
#     row_list = []
#     name_list = []
#     
#     
#     # Iterate over each voxel
#     for z in range(dims[0]):
#         for y in range(dims[1]):
#             for x in range(dims[2]):
#                 vox_vals = []
#                 # For each voxel, iterate over each image in the img_list
#                 for img in img_list:
#                     vox_vals.append(img[z,y,x])
#                 name = str(z)+"_"+str(y)+"_"+str(x)
#                 
#                 row_list.append({"Voxel Values":[vox_vals], "Mean":np.mean(vox_vals),
#                                  "SD":np.std(vox_vals)})
#                 name_list.append(name)
#     
#     vox_df = pd.DataFrame(row_list, index=name_list)
#     end = time.time()
#     print(end-start)
#     return vox_df
# =============================================================================

def create_voxel_data_file(img_list, file_name):
    """Given a list of images (as numpy arrays), iterates trhough all the images in the
    list for each voxel in the images. For each voxel, writes the value for each image 
    as a new line in a space delimited text file with the format: name val1 val2... valn
    where n is the number of images in the image list"""
    
    start = time.time()
    
    dims = img_list[0].shape
    file = open(file_name, "w")
    
    # iterate over each voxel
    for z in range(dims[0]):
        for y in range(dims[1]):
            for x in range(dims[2]):
                
                # For each voxel, iterate over each image in the img_list
                name = str(z)+"_"+str(y)+"_"+str(x)
                file.write(name+" ")
                
                for img in img_list:
                    file.write(str(img[z,y,x])+ " ")
                    
                file.write("\n")
                
    file.close()
    end = time.time()
    print(end-start)
    
    return None

def reservoir_sample_file(data_file, sample_size):
    """Given a data file, uses the resevoir sampling algorithm to generate a random sample of lines in the 
    file and returns a list containing the strings in those lines"""
    reservoir = [1]*sample_size
    file = open(data_file)
    counter = 0
    
    for line in file:
        if line[0] == "#":
            continue
        elif counter < sample_size:
            reservoir[counter] = line
            counter += 1
        else:
            r = rand.randint(1, counter+1)
            if r <= sample_size:
                reservoir[r-1] = line
            counter += 1
            
    file.close()
    
    return reservoir

def sample_file_lines(data_file, sample_size):
    """Takes a random sample of the lines in a data file and returns them as a list of 
    strings"""
    file = open(data_file)
    lines = list(file)
    sample_lines = random.sample(lines, sample_size)
    file.close()
    
    return sample_lines

def df_from_file_sample(sample_lines):
    """Given a list of line strings from a data_file, creates a numeric pandas dataframe,
    assumes that the first column in the dataframe is the row name"""
    sample_lines = [i.strip("\n").split() for i in sample_lines]
    df = pd.DataFrame(sample_lines)
    df = df.set_index([0])
    df = df.apply(pd.to_numeric)
    
    return df
    