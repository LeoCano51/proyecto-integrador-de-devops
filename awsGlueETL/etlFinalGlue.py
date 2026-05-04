import pandas as pd
import numpy as np
import boto3
import io
import pymysql
import sys
import subprocess

subprocess.check_call([
    sys.executable, "-m", "pip", "install", "pymysql", "-t", "/tmp"
])

sys.path.insert(0, "/tmp")

import pymysql

# -----------------------------
# CONFIG
# -----------------------------

S3_BUCKET = "sapsimdata"
S3_KEY = "synthetic_projects_dataset_DO.csv"

RDS_HOST = "devopsdbinstance.chg6o2suqnpf.us-east-2.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "superdupercontraseniaBD"
RDS_DB = "etl_db"

# -----------------------------
# 1. EXTRACT
# -----------------------------
s3 = boto3.client("s3")
obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)

df = pd.read_csv(io.BytesIO(obj["Body"].read()))

# estandarizar nombres
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -----------------------------
# 2. TRANSFORM
# -----------------------------
numeric_cols = [
    "forecast_cost","estimated_sell_price","change_order_cost",
    "change_order_sell_price","final_cost","final_sell_price",
    "estimated_duration_days","delays_days","final_duration_days",
    "risks_registered","risks_prevented"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates(subset="project_id")

cols_no_negative = [
    "forecast_cost","estimated_sell_price","change_order_cost",
    "change_order_sell_price","final_cost","final_sell_price",
    "estimated_duration_days","final_duration_days",
]

for col in cols_no_negative:
    df.loc[df[col] < 0, col] = np.nan

# consistencia duración
df["duration_check"] = df["estimated_duration_days"] + df["delays_days"]
mask = df["duration_check"] != df["final_duration_days"]
df.loc[mask, "final_duration_days"] = df.loc[mask, "duration_check"]
df.drop(columns=["duration_check"], inplace=True)

# normalizar texto
text_cols = ["line_of_business","region","country_code","tier"]
for col in text_cols:
    df[col] = df[col].str.strip().str.upper()

# riesgos consistentes
df["risks_prevented"] = df[["risks_prevented","risks_registered"]].min(axis=1)

# -----------------------------
# 3. FEATURE ENGINEERING
# -----------------------------
df["estimated_margin"] = df["estimated_sell_price"] - df["forecast_cost"]
df["final_margin"] = df["final_sell_price"] - df["final_cost"]
df["final_margin_pct"] = df["final_margin"] / df["final_sell_price"]
df["change_order_profit"] = df["change_order_sell_price"] - df["change_order_cost"]
df["delay_ratio"] = df["delays_days"] / df["estimated_duration_days"]
df["risk_mitigation_rate"] = (
    df["risks_prevented"] / df["risks_registered"]
).fillna(0)

# -----------------------------
# 4. FLAGS
# -----------------------------
df["high_delay_flag"] = df["delay_ratio"] > 0.2
df["low_margin_flag"] = df["final_margin_pct"] < 0.1
df["risk_management_issue"] = df["risk_mitigation_rate"] < 0.5

# -----------------------------
# 5. LOAD
# -----------------------------

# columnas EXACTAS de la tabla SQL
columns_sql = [
    "project_id",
    "forecast_cost",
    "estimated_sell_price",
    "change_order_cost",
    "change_order_sell_price",
    "final_cost",
    "final_sell_price",
    "estimated_duration_days",
    "delays_days",
    "final_duration_days",
    "risks_registered",
    "risks_prevented",
    "estimated_margin",
    "final_margin",
    "final_margin_pct",
    "change_order_profit",
    "delay_ratio",
    "risk_mitigation_rate",
    "high_delay_flag",
    "low_margin_flag",
    "risk_management_issue"
]

df_insert = df[columns_sql]

# conexión RDS
conn = pymysql.connect(
    host=RDS_HOST,
    user=RDS_USER,
    password=RDS_PASSWORD,
    database=RDS_DB
)

cursor = conn.cursor()

# query dinámica segura
placeholders = ",".join(["%s"] * len(columns_sql))
insert_query = f"""
INSERT INTO projects_clean ({",".join(columns_sql)})
VALUES ({placeholders})
"""

# inserción fila por fila (simple)
for _, row in df_insert.iterrows():
    cursor.execute(insert_query, tuple(row))

conn.commit()
conn.close()

print("ETL COMPLETADO")
print("Registros cargados:", len(df_insert))