import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

# Connect database
db = sqlite3.connect('comments.db')

# Read all comments
df = pd.read_sql_query("SELECT * from comments", db)

# Converting comments to feature vectors using CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['comment'])

# Creating K-means clustering model
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

# Assigning comments to clusters
df['cluster'] = kmeans.labels_

print(df)