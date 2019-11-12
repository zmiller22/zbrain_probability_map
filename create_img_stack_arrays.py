#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:35:17 2019

@author: Zachary Miller

Reads in the glut and gad image stacks and saves them as 4d arrays 
"""

import skimage as si
import numpy as np
import zbrain_analysis_functions as my_func

indiv_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/Gad1b_individual_zbrain_stacks"
indiv_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/vglutGFP_individual_zbrain_stacks"

gad_img_list = my_func.read_img_dir(indiv_gad_path, as_float=False)
glut_img_list = my_func.read_img_dir(indiv_glut_path, as_float=False)

#%%
my_func.save_img_list_as_array(gad_img_list, "created_data/gad_img_stacks_arr")
my_func.save_img_list_as_array(glut_img_list, "created_data/glut_img_stacks_arr")