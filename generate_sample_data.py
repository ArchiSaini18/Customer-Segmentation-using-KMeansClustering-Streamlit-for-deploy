"""
Sample Dataset Generator for Customer Segmentation
Run this file if you don't have the customer_segmentation.csv file
"""

import pandas as pd
import numpy as np

def generate_sample_dataset(n_samples=1000):
    """Generate a sample customer segmentation dataset"""
    
    np.random.seed(42)
    
    # Generate data for different customer segments
    data = {
        'Year_Birth': np.random.randint(1940, 2005, n_samples),
        'Income': np.random.randint(20000, 150000, n_samples),
        'MntWines': np.random.randint(0, 1000, n_samples),
        'MntFruits': np.random.randint(0, 200, n_samples),
        'MntMeatProducts': np.random.randint(0, 1500, n_samples),
        'MntFishProducts': np.random.randint(0, 300, n_samples),
        'MntSweetProducts': np.random.randint(0, 200, n_samples),
        'MntGoldProds': np.random.randint(0, 300, n_samples),
        'NumWebPurchases': np.random.randint(0, 25, n_samples),
        'NumStorePurchases': np.random.randint(0, 20, n_samples),
        'NumWebVisitsMonth': np.random.randint(0, 20, n_samples),
        'Recency': np.random.randint(0, 100, n_samples)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some correlations to make it more realistic
    # Higher income customers tend to spend more
    high_income_mask = df['Income'] > 80000
    df.loc[high_income_mask, 'MntWines'] = df.loc[high_income_mask, 'MntWines'] * 1.5
    df.loc[high_income_mask, 'MntMeatProducts'] = df.loc[high_income_mask, 'MntMeatProducts'] * 1.5
    
    # Younger customers (born after 1980) tend to shop more online
    young_mask = df['Year_Birth'] > 1980
    df.loc[young_mask, 'NumWebPurchases'] = df.loc[young_mask, 'NumWebPurchases'] * 1.3
    df.loc[young_mask, 'NumWebVisitsMonth'] = df.loc[young_mask, 'NumWebVisitsMonth'] * 1.5
    
    # Save to CSV
    df.to_csv('customer_segmentation.csv', index=False)
    print(f"✅ Sample dataset created successfully!")
    print(f"📊 Total samples: {n_samples}")
    print(f"📁 Saved as: customer_segmentation.csv")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nDataset info:")
    print(df.info())

if __name__ == "__main__":
    generate_sample_dataset(1000)
