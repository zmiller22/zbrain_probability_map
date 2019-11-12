#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:53:42 2019

@author: Zachary Miller

Gets the mean of each MECE region in all glut and gad images and saves the results a 3d 
3d array for each
"""
#%% Import dependencies
import scipy.io
import os
import numpy as np
import skimage as si
import zbrain_analysis_functions as my_func
import matplotlib.pyplot as plt
import seaborn as sns

#%% Set paths
# This path should be a folder containing the MECE masks
MECE_masks_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/MECE-Masks"
# These paths should be the files containing the images as 4d arrays
gad_img_arr_path = "created_data/gad_img_stacks_arr.npy"
glut_img_arr_path = "created_data/glut_img_stacks_arr.npy"
#%% Read in the image arrays
gad_img_arr = np.load(gad_img_arr_path)
glut_img_arr = np.load(glut_img_arr_path)

gad_img_num = gad_img_arr.shape[0]
glut_img_num = glut_img_arr.shape[0]

#%% Create lists of all the masked images means for both gad and glut
mask_names_list = []
mask_volume_list = []
masked_gad_means_list = []
masked_glut_means_list = []

#TODO paralellize this loop so that it is applying the masks simultaniously
directory = os.fsencode(MECE_masks_path)
for mask_file in os.listdir(directory):
    filename = os.fsdecode(mask_file)
    file_path = os.path.join(MECE_masks_path, filename)
    if os.path.isdir(file_path) == False:
        mask = si.io.imread(file_path)
        mask = mask.astype(bool)
        
        # get mask information
        mask_names_list.append(filename) 
        mask_volume_list.append(np.sum(mask))
        
        # get masked means
        masked_gad_means_list.append([np.mean(gad_img_arr[i, :, :, :][mask]) for i in range(gad_img_num)])
        masked_glut_means_list.append([np.mean(glut_img_arr[i, :, :, :][mask]) for i in range(glut_img_num)])

#%% Save the results as 3d arrays      
my_func.save_img_list_as_array(masked_gad_means_list, "created_data/gad_MECE_mask_means")
my_func.save_img_list_as_array(masked_glut_means_list, "created_data/glut_MECE_mask_means")

np.save("created_data/MECE_mask_names", np.asarray(mask_names_list))
np.save("created_data/MECE_mask_volumes", np.asarray(mask_volume_list))    