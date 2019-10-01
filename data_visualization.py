#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 09:46:48 2019

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
# =============================================================================
# mean_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Gad1b-GFP-combined.tif"
# mean_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Vglut2a-GFP-combined.tif"
# 
# indiv_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/Gad1b_individual_zbrain_stacks"
# indiv_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/vglutGFP_individual_zbrain_stacks"
# =============================================================================

# Read individual image stacks into lists
# =============================================================================
# gad_img_list = my_func.read_img_dir(indiv_gad_path)
# glut_img_list = my_func.read_img_dir(indiv_glut_path)
# =============================================================================

#gad_vox_df = pd.read_csv("gad_vox_vals.txt", header=None, delim_whitespace=True)
# =============================================================================
# gad_vox_means = np.array(gad_vox_df.mean())
# gad_vox_sds = gad_vox_df.std()
# =============================================================================

sample_lines = my_func.sample_file_lines("gad_vox_vals.txt", 100000)
gad_vox_df = my_func.df_from_file_sample(sample_lines)
sns.distplot(gad_vox_df.std(axis=1))


"""
### Next Steps ###
The next step is to use the my_func.get_voxel_vector in a for loop to get a dataframe in 
pandas that has each voxel "number" as the row, and then for each row has a columns for 
each voxel value and perhaps also some summary statistics (mean, sd, etc.). Then, I can 
plot a random sample of 20 or so voxels disributions, and then a histogram of the means 
and the sds for all voxels. I want to figure out how the distribution of values for each
voxel looks, and then also the distribution of means/sd for each voxel
"""