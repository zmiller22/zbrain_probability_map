#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 21:32:06 2019

@author: Zachary Miller
"""

import skimage as si
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zbrain_analysis_functions as my_func
import time

# Set up paths
mean_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Gad1b-GFP-combined.tif"
mean_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Vglut2a-GFP-combined.tif"

indiv_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/Gad1b_individual_zbrain_stacks"
indiv_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/vglutGFP_individual_zbrain_stacks"


# Read individual image stacks into lists
gad_img_list = my_func.read_img_dir(indiv_gad_path, as_float=False)[0]
glut_img_list, glut_img_names_list = my_func.read_img_dir(indiv_glut_path, as_float=False)[0]

float_gad_img_list = my_func.read_img_dir(indiv_gad_path, as_float=True)[0]
float_glut_img_list  = my_func.read_img_dir(indiv_glut_path, as_float=True)[0]

#%% Write voxel data to a text file
my_func.create_voxel_data_file(gad_img_list, "gad_vox_vals.txt")
my_func.create_voxel_data_file(glut_img_list, "glut_vox_vals.txt")

my_func.create_voxel_data_file(float_gad_img_list, "float_gad_vox_vals.txt")
my_func.create_voxel_data_file(float_glut_img_list, "float_glut_vox_vals.txt")

