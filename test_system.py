"""
Testing Script for Customer Segmentation System
Run this to verify all components are working correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import pandas as pd
        print("✅ Pandas imported successfully")
        
        import numpy as np
        print("✅ NumPy imported successfully")
        
        import seaborn as sns
        print("✅ Seaborn imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
        
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        print("✅ Scikit-learn imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def test_dataset():
    """Test if dataset exists and is valid"""
    print("\n📊 Testing dataset...")
    try:
        import pandas as pd
        
        if not os.path.exists('customer_segmentation.csv'):
            print("⚠️  Dataset not found: customer_segmentation.csv")
            print("💡 Run: python generate_sample_data.py")
            return False
        
        df = pd.read_csv('customer_segmentation.csv')
        print(f"✅ Dataset loaded successfully")
        print(f"   - Rows: {len(df)}")
        print(f"   - Columns: {len(df.columns)}")
        
        required_columns = ['Year_Birth', 'Income', 'MntWines', 'MntFruits', 
                          'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts',
                          'MntGoldProds', 'NumWebPurchases', 'NumStorePurchases',
                          'NumWebVisitsMonth', 'Recency']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        
        print("✅ All required columns present")
        return True
        
    except Exception as e:
        print(f"❌ Dataset error: {e}")
        return False

def test_model_training():
    """Test if model can be trained"""
    print("\n🤖 Testing model training...")
    try:
        import pandas as pd
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        
        # Load data
        df = pd.read_csv('customer_segmentation.csv')
        df.dropna(inplace=True)
        df["Age"] = 2026 - df["Year_Birth"]
        df["Total_Spending"] = df[["MntWines", "MntFruits", "MntMeatProducts",
                                   "MntFishProducts", "MntSweetProducts", 
                                   "MntGoldProds"]].sum(axis=1)
        
        features = ["Age", "Income", "Total_Spending",
                   "NumWebPurchases", "NumStorePurchases",
                   "NumWebVisitsMonth", "Recency"]
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[features])
        model = KMeans(n_clusters=6, random_state=42)
        clusters = model.fit_predict(X_scaled)
        
        print("✅ Model trained successfully")
        print(f"   - Features used: {len(features)}")
        print(f"   - Clusters created: {len(set(clusters))}")
        print(f"   - Samples processed: {len(clusters)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model training error: {e}")
        return False

def test_user_database():
    """Test user database functionality"""
    print("\n👤 Testing user database...")
    try:
        import pandas as pd
        
        # Create test database if it doesn't exist
        if not os.path.exists('users.csv'):
            pd.DataFrame(columns=["username", "password"]).to_csv('users.csv', index=False)
            print("✅ User database created")
        else:
            users = pd.read_csv('users.csv')
            print(f"✅ User database exists ({len(users)} users)")
        
        return True
        
    except Exception as e:
        print(f"❌ User database error: {e}")
        return False

def test_app_file():
    """Test if main app file exists"""
    print("\n📱 Testing application file...")
    
    if not os.path.exists('app3_improved.py'):
        print("❌ Application file not found: app3_improved.py")
        return False
    
    print("✅ Application file exists")
    
    # Check file size
    file_size = os.path.getsize('app3_improved.py')
    print(f"   - File size: {file_size:,} bytes")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🎯 CUSTOMER SEGMENTATION SYSTEM - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Dataset", test_dataset),
        ("Model Training", test_model_training),
        ("User Database", test_user_database),
        ("Application File", test_app_file)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to run the app!")
        print("\n🚀 Run the app with:")
        print("   streamlit run app3_improved.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("💡 Check the error messages for guidance.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
