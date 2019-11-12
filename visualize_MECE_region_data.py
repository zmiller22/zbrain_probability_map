#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:36:17 2019

@author: Zachary Miller

Script for visualizing masked means data
"""

#%% Import dependencies
import scipy.io
import os
import numpy as np
import skimage as si
import zbrain_analysis_functions as my_func
import matplotlib.pyplot as plt
import seaborn as sns

#%% Load the data
masked_gad_means_arr = np.load("created_data/gad_MECE_mask_means.npy")
masked_glut_means_arr = np.load("created_data/glut_MECE_mask_means.npy")

masked_gad_means_list = list(masked_gad_means_arr)
masked_glut_means_list = list(masked_glut_means_arr)
mask_volume_list = list(np.load("created_data/MECE_mask_volumes.npy"))
mask_names_list = list(np.load("created_data/MECE_mask_names.npy"))

#%% Create mean vs variance scatter plots
#NOTE do I need to pay attantion to the sampling bias here?
# Get the means and variances accross image stacks for each region
gad_means = [np.mean(vals) for vals in masked_gad_means_list]
glut_means = [np.mean(vals) for vals in masked_glut_means_list]

gad_vars = [np.var(vals) for vals in masked_gad_means_list]
glut_vars = [np.var(vals) for vals in masked_glut_means_list]

max_volume = np.max(mask_volume_list)
mask_volume_list = [vol/max_volume for vol in mask_volume_list]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
c = ax1.scatter(gad_means, gad_vars, c=mask_volume_list, s=80, alpha=0.8)
ax1.plot(np.unique(gad_means), np.poly1d(np.polyfit(gad_means, gad_vars, 2))(np.unique(gad_means)))
ax1.set_title("Gad", fontsize=16)
ax2.scatter(glut_means, glut_vars, c=mask_volume_list, s=80, alpha=0.8)
ax2.plot(np.unique(glut_means), np.poly1d(np.polyfit(glut_means, glut_vars, 2))(np.unique(glut_means)))
ax2.yaxis.tick_right()
ax2.set_title("Glut", fontsize=16)

cbar_ax = fig.add_axes([0.5, 0.13, 0.02, 0.4])
fig.colorbar(c, cax=cbar_ax, orientation="vertical")
fig.text(0.51, 0, "Mean", ha="center", fontsize=16)
fig.text(0.05, 0.5, "Variance", rotation="vertical", fontsize=16)
fig.text(0.7, 0, "*Color indicates relative region size", fontsize=16)
fig.suptitle("Mean vs. Variance for MECE Regions", fontsize=20)

#%% Create mean vs sd scatter plots
# Get the stds accross image stacks for each region
gad_stds = [np.std(vals) for vals in masked_gad_means_list]
glut_stds = [np.std(vals) for vals in masked_glut_means_list]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
c = ax1.scatter(gad_means, gad_stds, c=mask_volume_list, s=80, alpha=0.8)
ax1.plot(np.unique(gad_means), np.poly1d(np.polyfit(gad_means, gad_stds, 1))(np.unique(gad_means)))
ax1.set_title("Gad", fontsize=16)
ax2.scatter(glut_means, glut_stds, c=mask_volume_list, s=80, alpha=0.8)
ax2.plot(np.unique(glut_means), np.poly1d(np.polyfit(glut_means, glut_stds,1))(np.unique(glut_means)))
ax2.yaxis.tick_right()
ax2.set_title("Glut", fontsize=16)

cbar_ax = fig.add_axes([0.5, 0.13, 0.02, 0.4])
fig.colorbar(c, cax=cbar_ax, orientation="vertical")
fig.text(0.51, 0, "Mean", ha="center", fontsize=16)
fig.text(0.05, 0.5, "Standard Deviation", rotation="vertical", fontsize=16)
fig.text(0.7, 0, "*Color indicates relative region size", fontsize=16)
fig.suptitle("Mean vs. Standard Deviation for MECE Regions", fontsize=20)

#%% Create mean vs variance/means ratio scatter plot
# get the variance/mean ratios
gad_ratio = np.divide(gad_vars, gad_means)
glut_ratio = np.divide(glut_vars, glut_means)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
c = ax1.scatter(gad_means, gad_ratio, c=mask_volume_list, s=80, alpha=0.8)
ax1.set_title("Gad", fontsize=16)
ax1.hlines(1, 0, 10)
ax2.scatter(glut_means, glut_ratio, c=mask_volume_list, s=80, alpha=0.8)
ax2.hlines(1, 0, 10)
ax2.yaxis.tick_right()
ax2.set_title("Glut", fontsize=16)

cbar_ax = fig.add_axes([0.5, 0.13, 0.02, 0.4])
fig.colorbar(c, cax=cbar_ax, orientation="vertical")
fig.text(0.05, 0.5, "Variance/Mean", rotation="vertical", fontsize=16)
fig.text(0.51, 0, "Mean", ha="center", fontsize=16)
fig.text(0.7, 0, "*Color indicates relative region size", fontsize=16)
fig.suptitle("Ratio of Variance/Mean", fontsize=20)

#%% Create var vs sd scatter plots
gad_ratio = np.divide(gad_vars, gad_means)
glut_ratio = np.divide(glut_vars, glut_means)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
c = ax1.scatter(np.linspace(0,10,126), gad_ratio, c=mask_volume_list, s=80, alpha=0.8)
ax1.set_title("Gad", fontsize=16)
ax1.hlines(1, 0, 10)
ax2.scatter(np.linspace(0,10,126), glut_ratio, c=mask_volume_list, s=80, alpha=0.8)
ax2.hlines(1, 0, 10)
ax2.yaxis.tick_right()
ax2.set_title("Glut", fontsize=16)

cbar_ax = fig.add_axes([0.5, 0.13, 0.02, 0.4])
fig.colorbar(c, cax=cbar_ax, orientation="vertical")
fig.text(0.05, 0.5, "Variance/Mean", rotation="vertical", fontsize=16)
fig.text(0.51, 0, "Mean", ha="center", fontsize=16)
fig.text(0.7, 0, "*Color indicates relative region size", fontsize=16)
fig.suptitle("Ratio of Variance/Mean", fontsize=20)