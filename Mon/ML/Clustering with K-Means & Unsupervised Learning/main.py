# 📦 Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 📥 Load Dataset
df = pd.read_csv("Mall_Customers.csv")
print("First 5 rows:\n", df.head())

# 🔍 Check for Missing Values
print("\nMissing values:\n", df.isnull().sum())
print("\nData Types:\n", df.dtypes)

# 📊 EDA - Histograms & Boxplots
plt.figure(figsize=(14,5))

plt.subplot(1,2,1)
sns.histplot(df['Age'], bins=20, kde=True)
plt.title("Age Distribution")

plt.subplot(1,2,2)
sns.histplot(df['Annual Income (k$)'], bins=20, kde=True)
plt.title("Annual Income Distribution")
plt.tight_layout()
plt.show()

# Boxplots
plt.figure(figsize=(10,4))
sns.boxplot(data=df[['Age', 'Annual Income (k$)']])
plt.title("Boxplots of Age and Annual Income")
plt.show()

# 🎯 Feature Selection for Easy-Level Clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# 🚀 K-Means Clustering (k = 3)
kmeans_easy = KMeans(n_clusters=3, random_state=42)
df['Cluster_Easy'] = kmeans_easy.fit_predict(X)

# 🎨 Cluster Visualization
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster_Easy', palette='Set1')
plt.title("Customer Segments (k=3)")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.legend()
plt.show()

# --------------------- INTERMEDIATE LEVEL ---------------------

# 🧼 Preprocessing: Scaling
features = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# 🔍 Elbow Method to Find Optimal k
wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    wcss.append(km.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1, 11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("WCSS")
plt.grid(True)
plt.show()

# 💡 Apply KMeans with Optimal k (e.g., k=5)
k_optimal = 5
kmeans_final = KMeans(n_clusters=k_optimal, random_state=42)
df['Cluster_Final'] = kmeans_final.fit_predict(X_scaled)

# 📊 Cluster Profiling
cluster_profile = df.groupby('Cluster_Final')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
print("\nCluster Profile:\n", cluster_profile)

# 📌 Visualize Final Clusters in 2D
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster_Final', palette='tab10')
plt.title("Final Customer Segments")
plt.show()
