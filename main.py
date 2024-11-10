#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[5]:


import pandas as pd

# Load the data
play_store_data = pd.read_csv('Play Store Data.csv')
user_reviews = pd.read_csv('User Reviews.csv')

# Display the first few rows of each file to understand their structure
play_store_data_head = play_store_data.head()
user_reviews_head = user_reviews.head()

play_store_data_info = play_store_data.info()
user_reviews_info = user_reviews.info()

play_store_data_head, user_reviews_head, play_store_data_info, user_reviews_info


# In[10]:


#cleaning data
#converting reviews to numeric 
play_store_data['Reviews'] = pd.to_numeric(play_store_data['Reviews'], errors='coerce')

#removing rows with non numeric values in Installs
play_store_data = play_store_data[play_store_data['Installs'].str.contains('[0-9]', regex=True)]

#cleaning and converting Installs to numeric by removing commas and plus
play_store_data['Installs'] = play_store_data['Installs'].str.replace('[+,]', '', regex=True).astype(float)

#removing dollar and converting price to numeric
play_store_data['Price'] = play_store_data['Price'].str.replace('$', '').astype(float)

print(play_store_data[['Reviews', 'Installs', 'Price']].head())


# In[13]:


#exploratory analysis and visualizations

#1 : distribution of App Ratings
plt.figure(figsize=(10, 5))
sns.histplot(play_store_data['Rating'].dropna(), bins=20, kde=True)
plt.title('Distribution of App Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()


# In[15]:


#2 : Top 10 categories by Number of Apps
top_categories = play_store_data['Category'].value_counts().head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_categories.index, y=top_categories.values, palette="viridis")
plt.title('Top 10 App Categories by Count')
plt.xlabel('Category')
plt.ylabel('Number of Apps')
plt.xticks(rotation=45)
plt.show()


# In[19]:


#3 : Average Rating by category
avg_rating_by_category = play_store_data.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=avg_rating_by_category.index, y=avg_rating_by_category.values, palette="coolwarm")
plt.title('Top 10 Categories by Average Rating')
plt.xlabel('Category')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.show()


# In[23]:


#user reviews sentiment analysis
# sentiment distribution
sentiment_counts = user_reviews['Sentiment'].value_counts()
plt.figure(figsize=(8,4))
sentiment_counts.plot(kind='pie', autopct='%1.1f%%', colors=["#66c2a5", "#fc8d62", "#8da0cb"])
plt.title('Sentiment Distribution in User Reviews')
plt.ylabel('')
plt.show()


# In[24]:


# Average Sentiment Polarity by Category (only for apps with reviews)
merged_data = pd.merge(play_store_data, user_reviews, on='App', how='inner')
avg_polarity_by_category = merged_data.groupby('Category')['Sentiment_Polarity'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=avg_polarity_by_category.index, y=avg_polarity_by_category.values, palette="viridis")
plt.title('Top 10 Categories by Average Sentiment Polarity')
plt.xlabel('Category')
plt.ylabel('Average Sentiment Polarity')
plt.xticks(rotation=45)
plt.show()


# In[ ]:




