#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:42:50 2019

@author: tracingpc1
"""

import skimage as si
import numpy as np
import zbrain_analysis_functions as my_func

#%% Initialize the empty mean and variance arrays

gad_mean_arr = np.empty((138,1406,621),dtype=np.uint16)
gad_var_arr = np.empty((138,1406,621),dtype=np.uint16)


#%% Read the image stacks into a list of image stacks
mean_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Gad1b-GFP-combined.tif"
#mean_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Vglut2a-GFP-combined.tif"

indiv_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/Gad1b_individual_zbrain_stacks"
#indiv_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/vglutGFP_individual_zbrain_stacks"

gad_img_list = my_func.read_img_dir(indiv_gad_path, as_float=False)
#glut_img_list = my_func.read_img_dir(indiv_glut_path, as_float=False)

#%% Get the normalized mean, varianve, and difference between the mean and variance of each
# voxel accross the images
gad_img_arr = np.stack(gad_img_list)

gad_mean_arr = np.rint(np.mean(gad_img_arr, axis=0))
gad_var_arr = np.rint(np.var(gad_img_arr, axis=0))

norm_gad_mean_arr = gad_mean_arr/np.max(gad_mean_arr)
norm_gad_var_arr = gad_var_arr/np.max(gad_var_arr)
norm_gad_diff_arr = np.abs(norm_gad_mean_arr-norm_gad_var_arr)

si.external.tifffile.imsave("/mnt/c/Users/TracingPC1/Pictures/gad_mean_stack.tiff", 
                            si.img_as_uint(norm_gad_mean_arr))
si.external.tifffile.imsave("/mnt/c/Users/TracingPC1/Pictures/gad_var_stack.tiff", 
                            si.img_as_uint(norm_gad_var_arr))
si.external.tifffile.imsave("/mnt/c/Users/TracingPC1/Pictures/gad_diff_stack.tiff", 
                            si.img_as_uint(norm_gad_diff_arr))