# retail_sales_analysis.py
# A runnable Python script for EDA, SQL export, and basic plots.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

repo_root = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(repo_root, 'data', 'cleaned_sales_data.csv')

# If you have the full Superstore dataset, replace the file above with it (same name).
df = pd.read_csv(data_path, parse_dates=['Order Date'])

# Basic cleaning
df = df.dropna(subset=['Order Date', 'Sales'])
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
df['Revenue'] = df['Sales']  # In this dataset 'Sales' is the revenue column
df['Month'] = df['Order Date'].dt.to_period('M')

# Summary stats
total_revenue = df['Revenue'].sum()
print(f"Total Revenue: ${total_revenue:,.2f}")

# Top products
if 'Product Name' in df.columns:
    top_products = df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=False).head(10)
    print("Top products (sample):")
    print(top_products)
else:
    print('Product Name column not found in dataset.')

# Monthly revenue trend
monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Revenue'].sum()
monthly.index = monthly.index.astype(str)
print('\nMonthly revenue (sample):')
print(monthly)

# Save a plot
plots_dir = os.path.join(repo_root, 'images')
os.makedirs(plots_dir, exist_ok=True)
plt.figure(figsize=(8,4))
monthly.plot(kind='line', marker='o', grid=True)
plt.title('Monthly Revenue Trend')
plt.ylabel('Revenue')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'monthly_revenue.png'))
plt.close()

# Create SQLite DB from dataframe for SQL-based exploration
db_path = os.path.join(repo_root, 'data', 'sales_data.db')
conn = sqlite3.connect(db_path)
df.to_sql('sales', conn, if_exists='replace', index=False)

# Example queries (results printed)
q1 = "SELECT `Product Name`, SUM(Revenue) as Revenue FROM sales GROUP BY `Product Name` ORDER BY Revenue DESC LIMIT 10"
try:
    top_prod_sql = pd.read_sql(q1, conn)
    print('\nTop products from SQL:')
    print(top_prod_sql)
except Exception as e:
    print('SQL query failed:', e)

q2 = "SELECT strftime('%Y-%m', `Order Date`) as Month, SUM(Revenue) as Revenue FROM sales GROUP BY Month ORDER BY Month"
try:
    monthly_sql = pd.read_sql(q2, conn)
    print('\nMonthly revenue from SQL:')
    print(monthly_sql)
except Exception as e:
    print('SQL query failed:', e)

conn.close()
print('\nDone. Check the images/ folder for the generated plot and tableau/ for dashboard screenshot.')
