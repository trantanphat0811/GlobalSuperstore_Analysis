import pandas as pd
import sqlite3

DB = r"C:\DA\global-superstore-analysis\data\superstore.db"
conn = sqlite3.connect(DB)

# ── Query 1: Profit Margin theo Category ─────────────────────
q1 = """
SELECT category, sub_category,
       ROUND(SUM(sales), 0)                      AS total_sales,
       ROUND(SUM(profit), 0)                     AS total_profit,
       ROUND(SUM(profit)/SUM(sales)*100, 1)      AS margin_pct,
       ROUND(AVG(discount)*100, 1)               AS avg_discount_pct
FROM orders
GROUP BY category, sub_category
ORDER BY margin_pct ASC
"""
print("=" * 60)
print("QUERY 1 - Profit Margin (thap nhat -> cao nhat)")
print("=" * 60)
print(pd.read_sql(q1, conn).to_string(index=False))

# ── Query 2: Discount Impact ──────────────────────────────────
q2 = """
SELECT
    CASE
        WHEN discount = 0     THEN '0%  No discount'
        WHEN discount <= 0.10 THEN '1-10%'
        WHEN discount <= 0.20 THEN '11-20%'
        WHEN discount <= 0.30 THEN '21-30%'
        WHEN discount <= 0.40 THEN '31-40%'
        ELSE                       '>40%'
    END                                          AS discount_range,
    COUNT(*)                                     AS orders,
    ROUND(SUM(profit), 0)                       AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 1)        AS margin_pct
FROM orders
GROUP BY discount_range
ORDER BY discount
"""
print("\n" + "=" * 60)
print("QUERY 2 - Discount Impact (KEY INSIGHT)")
print("=" * 60)
print(pd.read_sql(q2, conn).to_string(index=False))

# ── Query 3: Top 10 Countries ─────────────────────────────────
q3 = """
SELECT country,
       ROUND(SUM(sales), 0)                AS total_sales,
       ROUND(SUM(profit), 0)               AS total_profit,
       ROUND(SUM(profit)/SUM(sales)*100,1) AS margin_pct
FROM orders
GROUP BY country
ORDER BY total_profit DESC
LIMIT 10
"""
print("\n" + "=" * 60)
print("QUERY 3 - Top 10 Countries by Profit")
print("=" * 60)
print(pd.read_sql(q3, conn).to_string(index=False))

# ── Query 4: Customer Segment ─────────────────────────────────
q4 = """
SELECT segment,
       COUNT(DISTINCT customer_id)              AS customers,
       ROUND(SUM(sales), 0)                    AS total_sales,
       ROUND(SUM(profit), 0)                   AS total_profit,
       ROUND(SUM(profit)/SUM(sales)*100, 1)    AS margin_pct
FROM orders
GROUP BY segment
ORDER BY total_sales DESC
"""
print("\n" + "=" * 60)
print("QUERY 4 - Customer Segment Performance")
print("=" * 60)
print(pd.read_sql(q4, conn).to_string(index=False))

# ── Query 5: Yearly Summary ───────────────────────────────────
q5 = """
SELECT year,
       ROUND(SUM(sales), 0)             AS total_sales,
       ROUND(SUM(profit), 0)            AS total_profit,
       COUNT(DISTINCT order_id)         AS total_orders,
       ROUND(SUM(profit)/SUM(sales)*100,1) AS margin_pct
FROM orders
GROUP BY year
ORDER BY year
"""
print("\n" + "=" * 60)
print("QUERY 5 - Yearly Summary")
print("=" * 60)
print(pd.read_sql(q5, conn).to_string(index=False))

conn.close()
print("\nHOAN THANH! Tat ca queries da chay thanh cong.")