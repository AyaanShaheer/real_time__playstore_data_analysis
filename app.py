import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned data
play_store_data = pd.read_csv('Play Store Data.csv')
user_reviews = pd.read_csv('User Reviews.csv')

# Set up the Streamlit app layout
st.title("Google Play Store Data Analytics Dashboard")
st.sidebar.header("Filter Options")

# Filter by Category
category_filter = st.sidebar.multiselect(
    "Select App Category:",
    options=play_store_data['Category'].unique(),
    default=play_store_data['Category'].unique()
)

# Apply the filter to the data
filtered_data = play_store_data[play_store_data['Category'].isin(category_filter)]

# Visualization 1: Distribution of Ratings
st.subheader("Distribution of App Ratings")
fig, ax = plt.subplots()
sns.histplot(filtered_data['Rating'].dropna(), bins=20, kde=True, ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Visualization 2: Top Categories by Number of Apps
st.subheader("Top 10 Categories by Number of Apps")
top_categories = filtered_data['Category'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_categories.index, y=top_categories.values, palette="viridis", ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Number of Apps")
st.pyplot(fig)

# Visualization 3: Average Rating by Category
st.subheader("Average Rating by Category")
avg_rating_by_category = filtered_data.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
sns.barplot(x=avg_rating_by_category.index, y=avg_rating_by_category.values, palette="coolwarm", ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Average Rating")
st.pyplot(fig)

# Sentiment Analysis
st.subheader("Sentiment Distribution in User Reviews")
sentiment_counts = user_reviews['Sentiment'].value_counts()
fig, ax = plt.subplots()
sentiment_counts.plot(kind='pie', autopct='%1.1f%%', colors=["#66c2a5", "#fc8d62", "#8da0cb"], ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

st.write("### Note")
st.write("This dashboard provides insights on Google Play Store app data, including ratings and sentiment analysis.")

