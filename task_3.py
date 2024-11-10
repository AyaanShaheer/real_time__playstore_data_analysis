#!/usr/bin/env python
# coding: utf-8

# # Task 3: Bubble Chart Analysis for Games Category
# 
# ### Objective
# This task aims to analyze the relationship between **app size** and **average rating** for apps in the "Games" category using a **bubble chart**. The chart will only include apps that meet specific criteria, and it will only display between **12 PM and 4 PM**.

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns


# In[3]:


play_store_data = pd.read_csv('Play Store Data.csv')

# Displaying first few rows and basic information
print("Dataset Info:")
print(play_store_data.info())
print("\nFirst few rows:")
display(play_store_data.head())


# In[4]:


# Cell 3: Data cleaning functions
def clean_size(size_str):
    try:
        if 'M' in str(size_str):
            return float(str(size_str).replace('M', ''))
        elif 'k' in str(size_str).lower():
            return float(str(size_str).replace('k', '')) / 1024
        elif size_str == 'Varies with device':
            return np.nan
        else:
            return float(size_str)
    except:
        return np.nan


# In[5]:


# Cell 4: Clean and prepare the data
# Clean Size column
play_store_data['Size'] = play_store_data['Size'].apply(clean_size)

# Clean Installs column
play_store_data['Installs'] = play_store_data['Installs'].str.replace('[+,]', '', regex=True)
play_store_data['Installs'] = pd.to_numeric(play_store_data['Installs'], errors='coerce')

# Filter the data
filtered_data = play_store_data[
    (play_store_data['Rating'].notna()) &
    (play_store_data['Rating'] > 3.5) &
    (play_store_data['Category'] == 'GAME') &
    (play_store_data['Installs'] > 50000) &
    (play_store_data['Size'].notna())
].copy()

# Display filtered data info
print("Filtered Dataset Info:")
print(filtered_data.info())
print("\nFiltered data summary:")
display(filtered_data.describe())


# In[6]:


# Get current time
current_time = datetime.now()
current_hour = current_time.hour

# Check if current time is between 12 PM and 4 PM
if 12 <= current_hour < 16:
    # Set the style to a built-in matplotlib style
    plt.style.use('tableau-colorblind10')
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Calculate bubble sizes
    bubble_sizes = np.cbrt(filtered_data['Installs']) * 2
    
    # Create custom colormap
    colors = plt.cm.RdYlBu_r
    
    # Create scatter plot
    scatter = ax.scatter(
        filtered_data['Size'],
        filtered_data['Rating'],
        s=bubble_sizes,
        alpha=0.6,
        c=np.log10(filtered_data['Installs']),
        cmap=colors,
        edgecolors='white',
        linewidth=0.5
    )
    
    # Rest of your visualization code remains the same
    cbar = plt.colorbar(scatter)
    cbar.set_label('Number of Installs (log scale)', size=12, labelpad=10)
    tick_labels = [f'{10**n:,.0f}' for n in cbar.get_ticks()]
    cbar.set_ticklabels(tick_labels)
    
    plt.title("App Size vs. Rating Distribution for Games\nAnalysis of Popular Apps (50k+ installs)", 
              pad=20, fontsize=16, fontweight='bold')
    
    ax.text(0.5, -0.1, 
            "Bubble size and color intensity represent number of installations",
            ha='center', va='center', transform=ax.transAxes, 
            fontsize=12, style='italic')
    plt.xlabel("App Size (MB)", fontsize=14, labelpad=10)
    plt.ylabel("Average Rating", fontsize=14, labelpad=10)
    
    size_padding = (filtered_data['Size'].max() - filtered_data['Size'].min()) * 0.05
    plt.xlim(filtered_data['Size'].min() - size_padding,
             filtered_data['Size'].max() + size_padding)
    plt.ylim(3.45, 5.05)
    
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    
    install_values = [100000, 1000000, 10000000]
    legend_elements = [
        plt.scatter([], [], 
                   s=np.cbrt(size) * 2,
                   c='gray',
                   alpha=0.6,
                   label=f'{size:,} installs')
        for size in install_values
    ]
    
    ax.legend(handles=legend_elements,
             title="Installation Count Reference",
             title_fontsize=12,
             fontsize=10,
             loc="upper right",
             bbox_to_anchor=(1.15, 1))
    
    max_installs_idx = filtered_data['Installs'].idxmax()
    max_rating_idx = filtered_data['Rating'].idxmax()
    for idx, label in [(max_installs_idx, 'Most Installed'),
                       (max_rating_idx, 'Highest Rated')]:
        ax.annotate(label,
                   xy=(filtered_data.loc[idx, 'Size'],
                       filtered_data.loc[idx, 'Rating']),
                   xytext=(10, 10),
                   textcoords='offset points',
                   fontsize=10,
                   bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7),
                   arrowprops=dict(arrowstyle='->'))
    
    plt.tight_layout()
    plt.show()
else:
    print("This visualization is only available between 12 PM and 4 PM.")


# In[ ]:




