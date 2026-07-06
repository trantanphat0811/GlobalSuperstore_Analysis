-- ============================================================
-- GLOBAL SUPERSTORE - BUSINESS QUERIES
-- File: 01_SQL/02_business_queries.sql
-- Chay trong DB Browser for SQLite
-- ============================================================


-- ── QUERY 1: Profit Margin theo Category & Sub-Category ─────
-- Muc tieu: Tim sub-category nao dang thua lo
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 0)                        AS total_sales,
    ROUND(SUM(profit), 0)                       AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1)   AS margin_pct,
    ROUND(AVG(discount) * 100, 1)              AS avg_discount_pct
FROM orders
GROUP BY category, sub_category
ORDER BY margin_pct ASC;


-- ── QUERY 2: Monthly Revenue Trend + MoM Growth ─────────────
-- Muc tieu: Xu huong doanh thu theo thang, tinh tang truong
WITH monthly AS (
    SELECT
        year,
        month,
        ROUND(SUM(sales), 0)  AS monthly_sales,
        ROUND(SUM(profit), 0) AS monthly_profit
    FROM orders
    GROUP BY year, month
)
SELECT
    year,
    month,
    monthly_sales,
    monthly_profit,
    LAG(monthly_sales) OVER (ORDER BY year, month) AS prev_month_sales,
    ROUND(
        (monthly_sales - LAG(monthly_sales) OVER (ORDER BY year, month))
        / LAG(monthly_sales) OVER (ORDER BY year, month) * 100
    , 1) AS mom_growth_pct
FROM monthly
ORDER BY year, month;


-- ── QUERY 3: Top 10 Countries by Revenue & Profit ───────────
-- Muc tieu: Thi truong nao sinh loi nhat / thua lo nhat
SELECT
    country,
    ROUND(SUM(sales), 0)                        AS total_sales,
    ROUND(SUM(profit), 0)                       AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1)   AS margin_pct,
    COUNT(DISTINCT order_id)                    AS total_orders
FROM orders
GROUP BY country
ORDER BY total_profit DESC
LIMIT 10;


-- ── QUERY 4: Discount Impact Analysis ───────────────────────
-- Muc tieu: Discount bao nhieu % thi bat dau thua lo?
SELECT
    CASE
        WHEN discount = 0         THEN '0% (No discount)'
        WHEN discount <= 0.10     THEN '1-10%'
        WHEN discount <= 0.20     THEN '11-20%'
        WHEN discount <= 0.30     THEN '21-30%'
        WHEN discount <= 0.40     THEN '31-40%'
        ELSE                           '> 40%'
    END                                          AS discount_range,
    COUNT(*)                                     AS order_count,
    ROUND(SUM(sales), 0)                        AS total_sales,
    ROUND(SUM(profit), 0)                       AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1)   AS margin_pct,
    ROUND(AVG(profit), 1)                       AS avg_profit_per_order
FROM orders
GROUP BY discount_range
ORDER BY discount;


-- ── QUERY 5: Customer Segment Performance ───────────────────
-- Muc tieu: Consumer vs Corporate vs Home Office
SELECT
    segment,
    COUNT(DISTINCT customer_id)                 AS customer_count,
    COUNT(DISTINCT order_id)                    AS total_orders,
    ROUND(SUM(sales), 0)                        AS total_sales,
    ROUND(SUM(profit), 0)                       AS total_profit,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 0) AS avg_order_value,
    ROUND(SUM(profit) / SUM(sales) * 100, 1)   AS margin_pct
FROM orders
GROUP BY segment
ORDER BY total_sales DESC;


-- ── QUERY 6: Shipping Mode Analysis ─────────────────────────
-- Muc tieu: Ship mode nao hieu qua nhat?
SELECT
    ship_mode,
    COUNT(*)                                     AS order_count,
    ROUND(AVG(delivery_days), 1)               AS avg_delivery_days,
    ROUND(AVG(shipping_cost), 2)               AS avg_shipping_cost,
    ROUND(SUM(profit), 0)                       AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1)   AS margin_pct
FROM orders
GROUP BY ship_mode
ORDER BY avg_delivery_days;


-- ── QUERY 7: Yearly Revenue Summary (export cho Power BI) ────
SELECT
    year,
    ROUND(SUM(sales), 0)    AS total_sales,
    ROUND(SUM(profit), 0)   AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(profit)/SUM(sales)*100, 1) AS margin_pct
FROM orders
GROUP BY year
ORDER BY year;

