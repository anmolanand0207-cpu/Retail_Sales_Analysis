-- sales_analysis.sql
-- Run these queries against data/sales_data.db (SQLite) or your SQL engine after loading the table 'sales'.

-- Top 10 products by revenue
SELECT "Product Name", SUM(Revenue) AS Revenue
FROM sales
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 10;

-- Monthly revenue trend
SELECT strftime('%Y-%m', "Order Date") AS Month, SUM(Revenue) AS Revenue
FROM sales
GROUP BY Month
ORDER BY Month;

-- Revenue by Region
SELECT Region, SUM(Revenue) AS Revenue
FROM sales
GROUP BY Region
ORDER BY Revenue DESC;
