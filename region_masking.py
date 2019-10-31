#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:53:42 2019

@author: tracingpc1
"""
#%% Import dependencies
import scipy.io
import os
import numpy as np
import skimage as si
import matplotlib.pyplot as plt
import seaborn as sns

#%% Set paths
MECE_masks_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/MECE-Masks"
gad_img_arr_path = "gad_img_stacks_arr.npy"
glut_img_arr_path = "glut_img_stacks_arr.npy"
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
        
#%% Create mean vs variance scatter plots
# Get the means and variances accross image stacks for each region
gad_means = [np.mean(vals) for vals in masked_gad_means_list]
glut_means = [np.mean(vals) for vals in masked_glut_means_list]

gad_vars = [np.var(vals) for vals in masked_gad_means_list]
glut_vars = [np.var(vals) for vals in masked_glut_means_list]

max_volume = np.max(mask_volume_list)
mask_volume_list = [vol/max_volume for vol in mask_volume_list]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
c = ax1.scatter(gad_means, gad_vars, c=mask_volume_list, s=80, alpha=0.8)
ax1.set_title("Gad", fontsize=16)
ax2.scatter(glut_means, glut_vars, c=mask_volume_list, s=80, alpha=0.8)
ax2.yaxis.tick_right()
ax2.set_title("Glut", fontsize=16)

cbar_ax = fig.add_axes([0.5, 0.13, 0.02, 0.4])
fig.colorbar(c, cax=cbar_ax, orientation="vertical")
fig.text(0.51, 0, "Mean", ha="center", fontsize=16)
fig.text(0.05, 0.5, "Variance", rotation="vertical", fontsize=16)
fig.text(0.7, 0, "*Color indicates relative region size", fontsize=16)
fig.suptitle("Mean vs. Variance for MECE Regions", fontsize=20)