"""
Global Superstore - Phase 1 | Step 1
Doc Sheet1 tu xlsx -> tao SQLite database
File: 01_SQL/01_import_to_sqlite.py
"""

import pandas as pd
import sqlite3
import os

# ── Duong dan ─────────────────────────────────────────────────────────────────
EXCEL_FILE = r"C:\DA\global-superstore-analysis\data\Global_Superstore2.xlsx"
DB_FILE    = r"C:\DA\global-superstore-analysis\data\superstore.db"

print("=" * 60)
print("GLOBAL SUPERSTORE - IMPORT EXCEL TO SQLITE")
print("=" * 60)

# Kiem tra file
if not os.path.exists(EXCEL_FILE):
    print(f"LOI: Khong tim thay file:\n  {EXCEL_FILE}")
    exit(1)

# ── BUOC 1: Doc Sheet1 ────────────────────────────────────────────────────────
print("\n[1/5] Doc Sheet1 tu Excel...")

xl = pd.ExcelFile(EXCEL_FILE)
print(f"      Sheets: {xl.sheet_names}")

# Doc sheet dau tien bat ke ten gi
first_sheet = xl.sheet_names[0]
print(f"      Dang doc sheet: '{first_sheet}'")

df = pd.read_excel(EXCEL_FILE, sheet_name=first_sheet)
print(f"      Shape: {df.shape[0]:,} rows x {df.shape[1]} cols")
print(f"      Columns: {list(df.columns)}")

# ── BUOC 2: Lam sach ten cot ─────────────────────────────────────────────────
print("\n[2/5] Lam sach ten cot...")

df.columns = (
    df.columns.str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("/", "_")
    .str.lower()
)
print(f"      Ten cot moi: {list(df.columns)}")

# ── BUOC 3: Xu ly ngay thang ──────────────────────────────────────────────────
print("\n[3/5] Xu ly ngay thang...")

date_cols = [c for c in df.columns if "date" in c]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")
    print(f"      Converted: {col}")

# Tao cot phu
order_col = next((c for c in df.columns if "order" in c and "date" in c), None)
ship_col  = next((c for c in df.columns if "ship"  in c and "date" in c), None)

if order_col and ship_col:
    df["delivery_days"] = (df[ship_col] - df[order_col]).dt.days
    df["year"]          = df[order_col].dt.year
    df["month"]         = df[order_col].dt.month
    df["quarter"]       = df[order_col].dt.quarter
    print(f"      Tao them: delivery_days | year | month | quarter")
    print(f"      delivery_days: min={int(df['delivery_days'].min())} | max={int(df['delivery_days'].max())}")

# ── BUOC 4: Kiem tra NULL ─────────────────────────────────────────────────────
print("\n[4/5] Kiem tra NULL values...")

nulls = df.isnull().sum()
nulls = nulls[nulls > 0]
if len(nulls) > 0:
    for col, cnt in nulls.items():
        print(f"      - {col}: {cnt:,} nulls ({cnt/len(df)*100:.1f}%)")
else:
    print("      Khong co NULL values")

# ── BUOC 5: Luu vao SQLite ────────────────────────────────────────────────────
print(f"\n[5/5] Luu vao SQLite...")

conn = sqlite3.connect(DB_FILE)

# Bang chinh: orders
df.to_sql("orders", conn, if_exists="replace", index=False)
n = pd.read_sql("SELECT COUNT(*) AS n FROM orders", conn).iloc[0, 0]
print(f"      Bang 'orders' : {n:,} rows OK")

# Tao bang returns tu orders (cac don hang returned)
# Trong dataset nay, thong tin return nam trong cot 'returned' hoac co the khong co
# -> Tao bang returns don gian tu order_id
returned_col = next((c for c in df.columns if "return" in c), None)
if returned_col:
    returns = df[df[returned_col].notna()][["order_id"] if "order_id" in df.columns else df.columns[:2].tolist()]
    returns.to_sql("returns", conn, if_exists="replace", index=False)
    print(f"      Bang 'returns': {len(returns):,} rows OK")
else:
    # Tao bang returns rong
    returns = pd.DataFrame(columns=["returned", "order_id", "market"])
    returns.to_sql("returns", conn, if_exists="replace", index=False)
    print(f"      Bang 'returns': tao rong (khong co cot returned trong data)")

# Tao bang people tu region
region_col = next((c for c in df.columns if "region" in c), None)
if region_col:
    people = df[[region_col]].drop_duplicates().reset_index(drop=True)
    people.columns = ["region"]
    people["person"] = "Unknown"
    people.to_sql("people", conn, if_exists="replace", index=False)
    print(f"      Bang 'people' : {len(people):,} rows OK (tao tu danh sach region)")

# ── Kiem tra nhanh bang SQL ────────────────────────────────────────────────────
print("\n── KIEM TRA NHANH ───────────────────────────────────────────")

sales_col  = next((c for c in df.columns if c == "sales"),  None)
profit_col = next((c for c in df.columns if c == "profit"), None)
cat_col    = next((c for c in df.columns if "categ" in c and "sub" not in c), None)

if sales_col and profit_col and cat_col:
    q = f"""
    SELECT {cat_col}            AS category,
           ROUND(SUM({sales_col}),  0) AS total_sales,
           ROUND(SUM({profit_col}), 0) AS total_profit,
           ROUND(SUM({profit_col})/SUM({sales_col})*100, 1) AS margin_pct
    FROM orders
    GROUP BY {cat_col}
    ORDER BY total_sales DESC
    """
    print("\nRevenue by Category:")
    print(pd.read_sql(q, conn).to_string(index=False))

if order_col:
    q2 = f"SELECT MIN({order_col}) AS from_date, MAX({order_col}) AS to_date FROM orders"
    print("\nTime range:")
    print(pd.read_sql(q2, conn).to_string(index=False))

country_col = next((c for c in df.columns if "country" in c), None)
if country_col:
    n_country = pd.read_sql(
        f"SELECT COUNT(DISTINCT {country_col}) AS n FROM orders", conn
    ).iloc[0, 0]
    print(f"\nSo quoc gia: {n_country}")

conn.close()

size_mb = os.path.getsize(DB_FILE) / 1024 / 1024
print(f"\n Database : {DB_FILE}")
print(f" Size     : {size_mb:.1f} MB")
print("\n" + "=" * 60)
print("HOAN THANH! Buoc tiep theo: chay 01_SQL/02_cleaning.sql")
print("=" * 60)