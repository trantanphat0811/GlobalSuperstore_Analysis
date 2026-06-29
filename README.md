# 🛒 Global Superstore Sales Analysis

Phân tích toàn diện hoạt động kinh doanh bán lẻ toàn cầu
sử dụng SQL · Python · Power BI


![Python](https://img.shields.io/badge/Python-3.10-blue)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![SQL](https://img.shields.io/badge/SQL-SQLite-green)

---

## 📌 Dataset
- *Nguồn:* Kaggle — Global Superstore
- *Quy mô:* 51,290 orders · 147 quốc gia · 2011–2014
- *File:* Global_Superstore2.xlsx (3 sheets)

---

## 🎯 5 Key Insights

1. *Technology dẫn đầu doanh thu* — $4.7M, margin 14%
   — gấp 2x Furniture về hiệu quả lợi nhuận

2. *Discount > 40% = 100% thua lỗ* — mọi đơn hàng
   có discount >= 0.4 đều ghi nhận Profit âm

3. *Tables & Bookcases đang thua lỗ* — margin lần
   lượt -8.5% và -3.2% do discount trung bình 29%

4. *Q4 luôn là peak* — 4/4 năm đều có doanh thu
   tháng 10-12 cao hơn trung bình 40%

5. *Champions = 22% khách hàng → 68% doanh thu*
   — Pareto 80/20 được xác nhận qua RFM analysis

---

## 🛠️ Tech Stack

| Phase | Tool | Mục đích |
|---|---|---|
| Phase 1 | SQL (SQLite) | Data cleaning, Business queries |
| Phase 2 | Python (Pandas, Seaborn, Prophet) | EDA, RFM, Forecast |
| Phase 3 | Power BI | Interactive Dashboard |

---

## 📁 Cấu trúc Project

global-superstore-analysis/
├── data/
│   ├── Global_Superstore2.xlsx
│   ├── superstore.db
│   ├── rfm_segments.csv
│   └── forecast_result.csv
├── 01_SQL/
│   ├── 01_import_to_sqlite.py
│   └── 02_business_queries.py
├── 02_Python/
│   ├── 01_EDA.py
│   ├── 02_Discount_Analysis.py
│   ├── 03_RFM_Segmentation.py
│   ├── 04_Geo_Analysis.py
│   └── 05_Forecast.py
├── 03_PowerBI/
│   ├── GlobalSuperstore_Dashboard.pbix
│   └── screenshots/
└── README.md

---

## 📊 Power BI Dashboard

| Trang | Nội dung |
|---|---|
| 1. Executive | KPI tổng quan, Revenue trend, Sub-Category |
| 2. Region | Map 147 quốc gia, Top countries |
| 3. Product | Category, Discount impact, Margin |
| 4. Forecast | Actual vs Forecast 2015 |
| 5. Customers | RFM Segments, Top customers |

---

## 🚀 Hướng dẫn chạy

# 1. Clone repo
git clone https://github.com/trantanphat0811/global-superstore-analysis

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Chạy theo thứ tự
python 01_SQL/01_import_to_sqlite.py
python 02_Python/01_EDA.py
python 02_Python/02_Discount_Analysis.py
python 02_Python/03_RFM_Segmentation.py
python 02_Python/04_Geo_Analysis.py
python 02_Python/05_Forecast.py

# 4. Mở Power BI
# → Import file .pbix từ thư mục 03_PowerBI/

---

## 👤 Tác giả
*Trần Tấn Phát*
- GitHub: [trantanphat0811](https://github.com/trantanphat0811)
- Email: trantanphat08112004@gmail.com