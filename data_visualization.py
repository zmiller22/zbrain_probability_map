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
sns.distributions._has_statsmodels = False
import zbrain_analysis_functions as my_func
import time

# Set up paths
gad_data = "gad_vox_vals.txt"
glut_data = "glut_vox_vals.txt"

mean_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Gad1b-GFP-combined.tif"
mean_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/zbrain_images/Vglut2a-GFP-combined.tif"

indiv_gad_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/Gad1b_individual_zbrain_stacks"
indiv_glut_path = "/mnt/c/Users/TracingPC1/Documents/zbrain_analysis/vglutGFP_individual_zbrain_stacks"


#%% Read individual image stacks into lists

gad_img_list = my_func.read_img_dir(indiv_gad_path, as_float=False)
glut_img_list = my_func.read_img_dir(indiv_glut_path, as_float=False)



#%% Create the plotting data
#TODO optimize this so it will use less memory, currently the dataframe uses 8 gigs of ram

# Get a simple random sample of 10e6 voxels
sampled_data = my_func.sample_file_lines(gad_data, 1000000)
gad_vox_df = my_func.df_from_file_sample(sampled_data)

# Get the mean and std of the 10e6 sampled voxels
gad_vox_std_df = gad_vox_df.std(axis=1)
gad_vox_mean_df = gad_vox_df.mean(axis=1)

# Get a simple random sample of 20 of voxels from the 10e6 sampled voxels
gad_vox_hists_df = pd.DataFrame.sample(gad_vox_df, n=20).T
vox_names = list(gad_vox_hists_df.columns.values)

#%% Create Plots for the gad images

# Plot the kde of the density curves with a rug plot for the 20 sampled voxels to show the 
# distribution of shape. If all the voxels values are 0, plot a vertical line at 0 
fig1, ax1 = plt.subplots(5, 4, figsize=(20,20))
fig1.suptitle("Individual Gad Voxel Distributions", fontsize=28)

counter=0
for r in range(5):
    
    for c in range(4):
        if sum(gad_vox_hists_df.iloc[:,counter].values) == 0:
            sns.distplot(gad_vox_hists_df.iloc[:,counter], kde=False, rug=True, hist=False, ax=ax1[r, c], axlabel=False)
            ax1[r,c].axvline(0, 0, 1)
            ax1[r,c].set_xlabel(vox_names[counter])
        else:
            sns.kdeplot(gad_vox_hists_df.iloc[:,counter], shade=True, legend=False, ax=ax1[r, c])
            sns.rugplot(gad_vox_hists_df.iloc[:,counter], ax=ax1[r,c])
            ax1[r,c].set_xlabel(vox_names[counter])
        counter+=1
        
fig1.text(0.5, 0.04, 'Voxel Value', ha='center', fontsize=20)
fig1.text(0.04, 0.5, 'Frequency', va='center', rotation='vertical', fontsize=20)
        
# Plot a box plot with the overlayed swarm plot for each of the sampled voxels to show the
# distribution of scale
fig2 = plt.figure(figsize=(15,15))
fig2.suptitle("Individual Gad Voxel Distributions", fontsize=20)
ax = sns.boxplot(data=gad_vox_hists_df, orient="h", color="w")
sns.swarmplot(data=gad_vox_hists_df, orient="h", palette="dark", ax=ax)
ax.set(xlabel="Voxel Value", ylabel="Voxel Number")

# Plot the sds for 10e6 sampled voxels
fig3 = plt.figure(figsize =(15,15))
fig3.suptitle("Gad Voxel Standard Deviations Distribution(Sample of 10e6)", fontsize=20)
ax = sns.distplot(gad_vox_std_df, hist=False)
ax.set(xlabel="Voxel Standard Deviation", ylabel="Frequency")

# Plot the means for 10e6 sampled voxels
fig4 = plt.figure(figsize =(15,15))
fig4.suptitle("Gad Voxel Means Distribution (Sample of 10e6)", fontsize=20)
ax = sns.distplot(gad_vox_mean_df, hist=False)
ax.set(xlabel="Voxel Mean", ylabel="Frequency")

# Plot the histogram of the voxel values for each image
fig5 = plt.figure(figsize =(15,15)) 
fig5.suptitle("Glut voxel value distributions for each image (Sample of 10e6)", fontsize=20)
for col in gad_vox_df:
    data = gad_vox_df[col].values
    ax = sns.distplot(data, kde=False, hist_kws={"fc":(np.random.uniform(0,1),np.random.uniform(0,1),np.random.uniform(0,1),0.4), "lw":1, "edgecolor":(0,0,0,1)})
    
for col in gad_vox_df:
    data = gad_vox_df[col].values
    ax = sns.distplot(data, kde=False, hist_kws={"fc":(np.random.uniform(0,1),np.random.uniform(0,1),np.random.uniform(0,1),0), "alpha":None, "lw":1, "edgecolor":(0,0,0,1)})
ax.set(xlabel="Voxel Value", ylabel="Count")

#%% Create the plotting data

# Get samples for individual voxels
sampled_data = my_func.sample_file_lines(glut_data, 1000000)
glut_vox_df = my_func.df_from_file_sample(sampled_data)

# Get the mean and std of the 10e6 sampled voxels
glut_vox_std_df = glut_vox_df.std(axis=1)
glut_vox_mean_df = glut_vox_df.mean(axis=1)

# Get a simple random sample of 20 of voxels from the 10e6 sampled voxels
glut_vox_hists_df = pd.DataFrame.sample(glut_vox_df, n=20).T
vox_names = list(glut_vox_hists_df.columns.values)

#%% Create plots

# Plot the kde of the density curves with a rug plot for the 20 sampled voxels to show the 
# distribution of shape. If all the voxels values are 0, plot a vertical line at 0 
fig6, ax6 = plt.subplots(5,4, figsize=(20,20))
fig6.suptitle("Individual Glut Voxel Distributions", fontsize=28)

counter=0
for r in range(5):
    
    for c in range(4):
        if sum(glut_vox_hists_df.iloc[:,counter].values) == 0:
            sns.distplot(glut_vox_hists_df.iloc[:,counter], kde=False, rug=True, hist=False, ax=ax6[r, c], axlabel=False)
            ax6[r,c].axvline(0, 0, 1)
            ax6[r,c].set_xlabel(vox_names[counter])
        else:
            sns.kdeplot(glut_vox_hists_df.iloc[:,counter], shade=True, legend=False, ax=ax6[r, c])
            sns.rugplot(glut_vox_hists_df.iloc[:,counter], ax=ax6[r,c])
            ax6[r,c].set_xlabel(vox_names[counter])
        counter+=1

fig6.text(0.5, 0.04, 'Voxel Value', ha='center', fontsize=20)
fig6.text(0.04, 0.5, 'Frequency', va='center', rotation='vertical', fontsize=20)

# Plot a box plot with the overlayed swarm plot for each of the sampled voxels to show the
# distribution of scale
fig7 = plt.figure(figsize=(15,15))
fig7.suptitle("Individual Glut Voxel Distributions", fontsize=20)
ax = sns.boxplot(data=glut_vox_hists_df, orient="h", color="w")
sns.swarmplot(data=glut_vox_hists_df, orient="h", palette="dark", ax=ax)
ax.set(xlabel="Voxel Value", ylabel="Voxel Number")


# Plot the sds
fig8 = plt.figure(figsize =(15,15))
fig8.suptitle("Glut Voxel Standard Deviations Distribution (Sample of 10e6)", fontsize=20)
ax = sns.distplot(glut_vox_std_df, hist=False)
ax.set(xlabel="Voxel Standard Deviation", ylabel="Frequency")

# Plot the means
fig9 = plt.figure(figsize =(15,15))
fig9.suptitle("Glut Voxel Means Distribution (Sample of 10e6)", fontsize=20)
ax = sns.distplot(glut_vox_mean_df, hist=False)
ax.set(xlabel="Voxel Mean", ylabel="Frequency")

# Plot the histogram of the voxel values for each image
fig10 = plt.figure(figsize =(15,15)) 
fig10.suptitle("Glut voxel value distributions for each image (Sample of 10e6)", fontsize=20)
for col in glut_vox_df:
    data = glut_vox_df[col].values
    ax = sns.distplot(data, kde=False, hist_kws={"fc":(np.random.uniform(0,1),np.random.uniform(0,1),np.random.uniform(0,1),0.4), "lw":1, "edgecolor":(0,0,0,1)})
    
for col in glut_vox_df:
    data = glut_vox_df[col].values
    ax = sns.distplot(data, kde=False, hist_kws={"fc":(np.random.uniform(0,1),np.random.uniform(0,1),np.random.uniform(0,1),0), "alpha":None, "lw":1, "edgecolor":(0,0,0,1)})
ax.set(xlabel="Voxel Value", ylabel="Count")