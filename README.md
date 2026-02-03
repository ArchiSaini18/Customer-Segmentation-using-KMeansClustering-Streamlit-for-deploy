 🛍️ CUSTOMER SEGMENTATION USING K-MEANS CLUSTERING
=================================================
📌 **PROJECT OVERVIEW**
 -------------------------------------------------
  This project analyzes customer behavior and segments customers into meaningful groups using the K-Means clustering algorithm.
 The system helps businesses understand purchasing patterns, identify high-value and low-value customers, and support data-driven marketing decisions through an interactive
 Streamlit dashboard.

 -------------------------------------------------
🔐 APPLICATION FEATURES
 -------------------------------------------------
 • Secure Streamlit application with Login & Signup authentication
 
 • CSV-based user authentication system
 
 • Interactive and visually enhanced UI with custom CSS

-------------------------------------------------
# 🧹 DATA PREPROCESSING & FEATURE ENGINEERING
 -------------------------------------------------
• Handled missing values

• Engineered new features:

     - Age (calculated from Year_Birth)
     
    - Total_Spending (sum of all product purchases)
    
• Normalized numerical features using StandardScaler
-------------------------------------------------
 🤖 MACHINE LEARNING MODEL
-------------------------------------------------
 • Algorithm: K-Means Clustering
 
 • Number of clusters: 6
 
 • Features used for clustering:
 
     - Age
     
     - Income
     
     - Total_Spending
     
     - NumWebPurchases
     
     - NumStorePurchases
     
     - NumWebVisitsMonth
     
     - Recency

• Elbow Method (WCSS) used to justify optimal cluster count

 -------------------------------------------------
# 📊 CLUSTER ANALYSIS & INSIGHTS
 -------------------------------------------------
• Cluster summaries generated using mean feature values

• Clusters interpreted using:

     - Spending behavior
     
     - Income levels
     
     - Purchase frequency
     
     - Engagement & recency

# • Business-friendly cluster labels:
     - Premium Customers
     
     - Regular Shoppers
     
     - Potential Growth Customers
     
     - High-Value Online Customers
     
     - Store Loyalists
     
     - Budget-Conscious Customers

 -------------------------------------------------
# 🔮 REAL-TIME PREDICTION
 -------------------------------------------------
 • Accepts user input via Streamlit form
 
 • Scales input using trained StandardScaler
 
 • Predicts customer cluster in real time
 
 • Displays:
     - Predicted cluster
     
     - Cluster insights
     
     - Comparison with dataset distributions

 -------------------------------------------------
# 📈 VISUALIZATIONS
 -------------------------------------------------
 • Age, Income, and Spending distributions
 
 • User profile vs dataset comparison
 
 • Cluster distribution bar charts
 
 • Cluster summary tables with gradient styling

 -------------------------------------------------
🛠️ TECHNOLOGIES USED
 -------------------------------------------------
 • Python 3.x
 
 • Streamlit
 
 • Pandas, NumPy
 
 • Scikit-learn
 
 • Matplotlib, Seaborn

 -------------------------------------------------
# 📂 DATASET
 -------------------------------------------------
 • File: customer_segmentation.csv
 
 • Contains demographic, behavioral, and spending data
 
 • Unsupervised learning (no target labels)

 -------------------------------------------------
# 🚀 FUTURE IMPROVEMENTS
 -------------------------------------------------
 • Add marketing campaign response features
 
 • Replace CSV authentication with a database
 
 • Deploy on Streamlit Cloud / AWS
 
 • Implement cluster-based marketing recommendations

 -------------------------------------------------
 **Screenshot**
  -------------------------------------------------
link: https://github.com/ArchiSaini18/Customer-Segmentation-using-KMeansClustering-Streamlit-for-deploy/blob/main/Screenshot%202026-02-03%20222043.png

link: https://github.com/ArchiSaini18/Customer-Segmentation-using-KMeansClustering-Streamlit-for-deploy/blob/main/Screenshot%202026-02-03%20215734.png

link: https://github.com/ArchiSaini18/Customer-Segmentation-using-KMeansClustering-Streamlit-for-deploy/blob/main/Screenshot%202026-02-03%20215744.png

link: https://github.com/ArchiSaini18/Customer-Segmentation-using-KMeansClustering-Streamlit-for-deploy/blob/main/Screenshot%202026-02-03%20215752.png

link: https://github.com/ArchiSaini18/Customer-Segmentation-using-KMeansClustering-Streamlit-for-deploy/blob/main/Screenshot%202026-02-03%20215759.png
  
