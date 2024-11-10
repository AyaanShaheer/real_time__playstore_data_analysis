#!/usr/bin/env python
# coding: utf-8

# # Task 2: Grouped Bar Chart for Top 10 App Categories by Installs
# 
# ### Objective
# This task aims to visualize the **average rating** and **total review count** for the top 10 app categories, ranked by the number of installs. The analysis will only consider apps that meet specific criteria, and the chart will generate only between **10 AM and 5 PM**.

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.ticker as ticker


# In[13]:


#loading dataset
play_store_data = pd.read_csv('Play Store Data.csv')


# In[14]:


#1: Data cleaning and Initial Filtering
play_store_data['Size'] = play_store_data['Size'].replace('Varies with device', 'NaN')
play_store_data['Size'] = play_store_data['Size'].str.replace('M', '')
play_store_data['Size'] = pd.to_numeric(play_store_data['Size'], errors='coerce')

#filtering based on conditions : avg rating >= 4.0, size >= 10mb, last update - jan
filtered_data = play_store_data[
    (play_store_data['Rating'] >= 4.0) &              # Average Rating >= 4.0
    (play_store_data['Size'] >= 10) &                 # Size >= 10 MB
    (play_store_data['Last Updated'].str.contains('January'))  # Last updated in January
]


# In[15]:


#2: Identifying Top 10 Categories by Installs

# Makeing a copy of the filtered data to avoid the SettingWithCopyWarning
filtered_data = filtered_data.copy()

# Ensuring all values in the 'Installs' column are strings, then remove commas and plus signs
filtered_data['Installs'] = filtered_data['Installs'].astype(str).str.replace('[+,]', '', regex=True).astype(float)

# Grouping by Category to get top 10 categories by installs
# calculate the average rating and sum of reviews for each category
top_categories = (filtered_data.groupby('Category')
                  .agg({'Installs': 'sum', 'Rating': 'mean', 'Reviews': 'sum'})
                  .sort_values(by='Installs', ascending=False)
                  .head(10))

# Reset the index for easier access to columns in further steps
top_categories.reset_index(inplace=True)

# Displaying the resulting top_categories DataFrame to confirm
print(top_categories)


# In[17]:


current_hour = datetime.now().hour
if 10 <= current_hour < 17:
    # Create figure and axes with a larger size
    fig, ax1 = plt.subplots(figsize=(15, 8))
    
    # Create a second y-axis
    ax2 = ax1.twinx()
    
    # Set bar width and positions
    bar_width = 0.35
    positions = np.arange(len(top_categories))
    
    # Plot Average Rating bars on first y-axis
    rating_bars = ax1.bar(positions - bar_width/2, 
                         top_categories['Rating'],
                         width=bar_width,
                         label='Average Rating',
                         color='#2E86C1',
                         alpha=0.8)
    
    # Plot Review Count bars on second y-axis
    review_bars = ax2.bar(positions + bar_width/2,
                         top_categories['Reviews'],
                         width=bar_width,
                         label='Total Review Count',
                         color='#E74C3C',
                         alpha=0.8)
    
    # Formatting the first y-axis (Rating)
    ax1.set_ylabel('Average Rating', fontsize=12, color='#2E86C1')
    ax1.tick_params(axis='y', labelcolor='#2E86C1')
    ax1.set_ylim(3.5, 5.0)  # Set range for ratings
    
    # Formatting the second y-axis (Reviews)
    ax2.set_ylabel('Total Review Count', fontsize=12, color='#E74C3C')
    ax2.tick_params(axis='y', labelcolor='#E74C3C')
    
    # Format review count numbers with K/M suffix
    def format_count(x, p):
        if x >= 1e6:
            return f'{x/1e6:.1f}M'
        elif x >= 1e3:
            return f'{x/1e3:.1f}K'
        return f'{x:.0f}'
    
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(format_count))
    
    # Set title and adjust its position
    plt.title('Average Rating and Total Review Count\nfor Top 10 App Categories by Installs',
              pad=20, fontsize=14, fontweight='bold')
    
    # Format x-axis
    plt.xticks(positions, top_categories['Category'], rotation=45, ha='right')
    
    # Add gridlines to the review count axis
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    # Add legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1.15))
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 1.15))
    
    # Add value labels on bars
    def add_labels(bars, ax):
        for bar in bars:
            height = bar.get_height()
            if ax == ax1:  # Rating values
                label = f'{height:.2f}'
            else:  # Review count values
                label = format_count(height, None)
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   label, ha='center', va='bottom', rotation=0,
                   fontsize=9)
    
    add_labels(rating_bars, ax1)
    add_labels(review_bars, ax2)
    
    # Adjust layout
    plt.tight_layout()
    
    # Show plot
    plt.show()
else:
    print("This graph can only be generated between 10 AM and 5 PM.")


# In[ ]:




