# =================================================
# CUSTOMER SEGMENTATION SYSTEM - IMPROVED VERSION
# =================================================
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import warnings
warnings.filterwarnings('ignore')

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Customer Segmentation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================================
# ENHANCED CSS
# =================================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #3a679c 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #ff1493, #ff6b9d);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.4);
    }
    
    /* Prediction card */
    .prediction-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        margin: 20px 0;
        text-align: center;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        margin: 10px 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #667eea;
    }
    
    /* Input fields */
    .stNumberInput input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =================================================
# USER DATABASE MANAGEMENT
# =================================================
USER_DB = "users.csv"

def initialize_user_db():
    """Initialize user database if it doesn't exist"""
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=["username", "password"]).to_csv(USER_DB, index=False)

def load_users():
    """Load users from CSV"""
    try:
        return pd.read_csv(USER_DB)
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    """Save new user to database"""
    try:
        df = load_users()
        if username in df['username'].values:
            return False, "Username already exists!"
        new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv(USER_DB, index=False)
        return True, "Account created successfully!"
    except Exception as e:
        return False, f"Error saving user: {e}"

def verify_user(username, password):
    """Verify user credentials"""
    try:
        users = load_users()
        user_match = users[users['username'] == username]
        if not user_match.empty:
            stored_password = user_match.iloc[0]['password']
            return stored_password == password
        return False
    except Exception as e:
        st.error(f"Error verifying user: {e}")
        return False

# =================================================
# SESSION STATE INITIALIZATION
# =================================================
def initialize_session_state():
    """Initialize all session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "show_prediction" not in st.session_state:
        st.session_state.show_prediction = False

# =================================================
# DATA LOADING AND PREPROCESSING
# =================================================
@st.cache_data
def load_and_preprocess_data():
    """Load and preprocess customer data"""
    try:
        # Try to load the dataset
        df = pd.read_csv("customer_segmentation.csv")
        
        # Handle missing values
        df.dropna(inplace=True)
        
        # Feature engineering
        df["Age"] = 2026 - df["Year_Birth"]
        
        # Calculate total spending
        spending_columns = ["MntWines", "MntFruits", "MntMeatProducts",
                          "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
        df["Total_Spending"] = df[spending_columns].sum(axis=1)
        
        return df, None
    except FileNotFoundError:
        error_msg = "❌ Dataset file 'customer_segmentation.csv' not found! Please ensure the file is in the same directory as the app."
        return None, error_msg
    except Exception as e:
        error_msg = f"❌ Error loading data: {str(e)}"
        return None, error_msg

# =================================================
# MODEL TRAINING
# =================================================
@st.cache_resource
def train_clustering_model(df):
    """Train K-Means clustering model"""
    try:
        # Define features for clustering
        features = ["Age", "Income", "Total_Spending",
                   "NumWebPurchases", "NumStorePurchases",
                   "NumWebVisitsMonth", "Recency"]
        
        # Check if all required features exist
        missing_features = [f for f in features if f not in df.columns]
        if missing_features:
            return None, None, None, None, f"Missing features in dataset: {missing_features}"
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[features])
        
        # Train K-Means model
        model = KMeans(n_clusters=6, random_state=42, n_init=10)
        clusters = model.fit_predict(X_scaled)
        
        return model, scaler, features, clusters, None
    except Exception as e:
        return None, None, None, None, f"Error training model: {str(e)}"

# =================================================
# LOGIN PAGE
# =================================================
def login_page():
    """Display login and signup page"""
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🎯 Customer Segmentation System</h1>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white; font-size: 18px;'>Analyze and segment customers using AI-powered clustering</p>", 
                   unsafe_allow_html=True)
        
        # Create tabs for login and signup
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        # LOGIN TAB
        with tab1:
            st.markdown("### Welcome Back!")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if not username or not password:
                        st.error("⚠️ Please fill in all fields!")
                    elif verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.success(f"✅ Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
        
        # SIGNUP TAB
        with tab2:
            st.markdown("### Create New Account")
            with st.form("signup_form"):
                new_username = st.text_input("Choose Username", placeholder="Enter a unique username")
                new_password = st.text_input("Create Password", type="password", placeholder="Enter a strong password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
                submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit:
                    if not new_username or not new_password or not confirm_password:
                        st.error("⚠️ Please fill in all fields!")
                    elif len(new_username) < 3:
                        st.error("⚠️ Username must be at least 3 characters long!")
                    elif len(new_password) < 6:
                        st.error("⚠️ Password must be at least 6 characters long!")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match!")
                    else:
                        success, message = save_user(new_username, new_password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.current_user = new_username
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

# =================================================
# CLUSTER INSIGHTS
# =================================================
def get_cluster_insights(cluster_id, cluster_summary):
    """Get business insights for each cluster"""
    insights = {
        0: "💎 **Premium Customers**: High income and spending, frequent purchasers",
        1: "🎯 **Regular Shoppers**: Moderate income, consistent purchase behavior",
        2: "🌟 **Potential Growth**: Young customers with growing spending potential",
        3: "💼 **High-Value Online**: Strong online presence with good spending",
        4: "🏪 **Store Loyalists**: Prefer in-store shopping, regular visitors",
        5: "💰 **Budget Conscious**: Lower spending, price-sensitive segment"
    }
    return insights.get(cluster_id, "📊 General Customer Segment")

# =================================================
# MAIN DASHBOARD
# =================================================
def dashboard_page():
    """Main dashboard with clustering functionality"""
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Customer Segmentation Dashboard")
        st.markdown(f"Welcome, **{st.session_state.current_user}**! 👋")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.show_prediction = False
            st.rerun()
    
    st.markdown("---")
    
    # Load data
    with st.spinner("🔄 Loading customer data..."):
        df, error = load_and_preprocess_data()
    
    if error:
        st.error(error)
        st.info("💡 **Tip**: Make sure 'customer_segmentation.csv' is in the same folder as this app.")
        st.stop()
    
    # Train model
    with st.spinner("🤖 Training clustering model..."):
        model, scaler, features, clusters, error = train_clustering_model(df)
    
    if error:
        st.error(error)
        st.stop()
    
    # Add cluster labels to dataframe
    df["Cluster"] = clusters
    
    # Calculate cluster summary
    cluster_summary = df.groupby("Cluster")[features].mean().round(2)
    cluster_counts = df["Cluster"].value_counts().sort_index()
    
    # Display dataset overview
    with st.expander("📋 Dataset Overview", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", len(df))
        with col2:
            st.metric("Total Clusters", df["Cluster"].nunique())
        with col3:
            st.metric("Avg. Income", f"${df['Income'].mean():,.0f}")
        with col4:
            st.metric("Avg. Spending", f"${df['Total_Spending'].mean():,.0f}")
        
        st.dataframe(df.head(10), use_container_width=True)
    
    # =================================================
    # CUSTOMER INPUT SECTION
    # =================================================
    st.markdown("## 🔮 Predict Customer Segment")
    st.markdown("Enter customer details to predict their cluster segment:")
    
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 👤 Demographics")
            age = st.number_input("Age", min_value=18, max_value=100, value=35, step=1)
            income = st.number_input("Annual Income ($)", min_value=0, max_value=200000, value=50000, step=1000)
        
        with col2:
            st.markdown("### 🛒 Purchase Behavior")
            spending = st.number_input("Total Spending ($)", min_value=0, max_value=5000, value=500, step=50)
            web_purchases = st.number_input("Web Purchases", min_value=0, max_value=30, value=5, step=1)
            store_purchases = st.number_input("Store Purchases", min_value=0, max_value=30, value=5, step=1)
        
        with col3:
            st.markdown("### 📈 Engagement")
            web_visits = st.number_input("Web Visits/Month", min_value=0, max_value=30, value=5, step=1)
            recency = st.number_input("Days Since Last Purchase", min_value=0, max_value=365, value=30, step=1)
        
        submit_prediction = st.form_submit_button("🎯 Predict Cluster", use_container_width=True)
    
    # =================================================
    # PREDICTION RESULTS
    # =================================================
    if submit_prediction:
        try:
            # Prepare input data
            input_data = pd.DataFrame([[age, income, spending, web_purchases, 
                                      store_purchases, web_visits, recency]], 
                                     columns=features)
            
            # Scale and predict
            input_scaled = scaler.transform(input_data)
            predicted_cluster = model.predict(input_scaled)[0]
            
            # Display prediction
            st.markdown("---")
            st.markdown(f"""
            <div class="prediction-card">
                <h1>🎯 Predicted Cluster: <span style='color: #667eea;'>{predicted_cluster}</span></h1>
                <p style='font-size: 18px; color: #666; margin-top: 10px;'>
                    {get_cluster_insights(predicted_cluster, cluster_summary)}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show cluster characteristics
            st.markdown("### 📊 Cluster Characteristics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Average Values in This Cluster:")
                cluster_data = cluster_summary.loc[predicted_cluster]
                for feature in features[:4]:
                    value = cluster_data[feature]
                    if feature in ["Income", "Total_Spending"]:
                        st.write(f"**{feature}**: ${value:,.0f}")
                    else:
                        st.write(f"**{feature}**: {value:.1f}")
            
            with col2:
                st.markdown("#### Customer Count per Cluster:")
                fig, ax = plt.subplots(figsize=(8, 5))
                colors = ['#667eea' if i == predicted_cluster else '#cccccc' 
                         for i in range(len(cluster_counts))]
                cluster_counts.plot(kind='bar', ax=ax, color=colors)
                ax.set_xlabel("Cluster")
                ax.set_ylabel("Number of Customers")
                ax.set_title("Cluster Distribution")
                plt.xticks(rotation=0)
                st.pyplot(fig)
                plt.close()
            
            # =================================================
            # COMPARISON VISUALIZATIONS
            # =================================================
            st.markdown("---")
            st.markdown("## 📊 Your Profile vs Dataset")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.histplot(df["Age"], kde=True, ax=ax, color='#667eea', alpha=0.6)
                ax.axvline(age, color='#ff1493', linestyle='--', linewidth=2, label=f'Your Age: {age}')
                ax.set_xlabel("Age", fontsize=12)
                ax.set_ylabel("Frequency", fontsize=12)
                ax.set_title("Age Distribution", fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            with col2:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.histplot(df["Income"], kde=True, ax=ax, color='#667eea', alpha=0.6)
                ax.axvline(income, color='#ff1493', linestyle='--', linewidth=2, label=f'Your Income: ${income:,}')
                ax.set_xlabel("Income ($)", fontsize=12)
                ax.set_ylabel("Frequency", fontsize=12)
                ax.set_title("Income Distribution", fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            with col3:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.histplot(df["Total_Spending"], kde=True, ax=ax, color='#667eea', alpha=0.6)
                ax.axvline(spending, color='#ff1493', linestyle='--', linewidth=2, 
                          label=f'Your Spending: ${spending}')
                ax.set_xlabel("Total Spending ($)", fontsize=12)
                ax.set_ylabel("Frequency", fontsize=12)
                ax.set_title("Spending Distribution", fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            # =================================================
            # CLUSTER SUMMARY TABLE
            # =================================================
            st.markdown("---")
            st.markdown("## 📋 All Clusters Summary")
            
            summary_display = cluster_summary.copy()
            summary_display["Customer Count"] = cluster_counts.values
            
            # Format the dataframe
            st.dataframe(
                summary_display.style
                .format({
                    "Income": "${:,.0f}",
                    "Total_Spending": "${:,.0f}",
                    "Age": "{:.1f}",
                    "NumWebPurchases": "{:.1f}",
                    "NumStorePurchases": "{:.1f}",
                    "NumWebVisitsMonth": "{:.1f}",
                    "Recency": "{:.1f}",
                    "Customer Count": "{:,.0f}"
                })
                .background_gradient(cmap="RdPu", subset=["Income", "Total_Spending"])
                .highlight_max(axis=0, color='lightgreen')
                .highlight_min(axis=0, color='lightcoral'),
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")
            st.info("Please check your input values and try again.")

# =================================================
# MAIN APP LOGIC
# =================================================
def main():
    """Main application logic"""
    # Initialize
    initialize_user_db()
    initialize_session_state()
    
    # Route to appropriate page
    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page()

# =================================================
# RUN APPLICATION
# =================================================
if __name__ == "__main__":
    main()
