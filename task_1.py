#!/usr/bin/env python
# coding: utf-8

# # Task 1: Word Cloud of 5-Star Reviews for Health & Fitness Apps
# This notebook generates a word cloud for the most frequent keywords in 5-star reviews, excluding common stopwords and app names, focusing on apps in the "Health & Fitness" category.
# 

# In[1]:


import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import nltk


# In[2]:


#Downloading NLTK stopwords
nltk.download('stopwords')


# In[3]:


#loading dataset
play_store_data = pd.read_csv('Play Store Data.csv')
user_reviews = pd.read_csv('User Reviews.csv')


# In[4]:


#1: Unique app names in health and fitness category
health_apps = play_store_data[play_store_data['Category'] == 'HEALTH_AND_FITNESS']['App'].unique()

filtered_reviews = user_reviews[(user_reviews['App'].isin(health_apps)) & (user_reviews['Sentiment_Polarity'] == 1.0)]


# In[5]:


#2: Combining all reviews into a single text and cleaning it
#merge all 5-star review texts into a string
text = " ".join(review for review in filtered_reviews['Translated_Review'].dropna())

#removing app names from text for bias avoidance
for app_name in health_apps:
    text = re.sub(r'\b' + re.escape(app_name) + r'\b', '', text)
    


# In[6]:


#3: defining stopwords to exclude common words
stop_words = set(stopwords.words('english'))


# In[7]:


#4: Generating word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stop_words, collocations=False).generate(text)


# In[8]:


#5: Displaying word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Frequent Keywords in 5-Star Health & Fitness App Reviews")
plt.show()


# In[ ]:




