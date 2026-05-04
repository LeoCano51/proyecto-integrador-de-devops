import pandas as pd
import numpy as np

# -----------------------------
# 1. EXTRACT
# -----------------------------

input_file = "synthetic_projects_dataset_DO.csv"

df = pd.read_csv(input_file)

# estandarizar nombres de columnas
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print('nombres estandarizados')

# -----------------------------
# 2. TRANSFORM
# -----------------------------

# convertir tipos numéricos 

numeric_cols = [
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
    "risks_prevented"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# eliminar duplicados 

df = df.drop_duplicates(subset="project_id")

print('adios dups')

# limpiar valores negativos donde no deberían existir 

cols_no_negative = [
    "forecast_cost",
    "estimated_sell_price",
    "change_order_cost",
    "change_order_sell_price",
    "final_cost",
    "final_sell_price",
    "estimated_duration_days",
    "final_duration_days",
]

for col in cols_no_negative:
    df.loc[df[col] < 0, col] = np.nan

print('negativos ilogicos eliminados')

#  consistencia lógica 

# duración final = duración estimada + retrasos
df["duration_check"] = (
    df["estimated_duration_days"] + df["delays_days"]
)

# si hay inconsistencias, corregimos
mask = df["duration_check"] != df["final_duration_days"]

df.loc[mask, "final_duration_days"] = df.loc[mask, "duration_check"]

df.drop(columns=["duration_check"], inplace=True)

print('logica verificada')

#  normalizar texto 

text_cols = [
    "line_of_business",
    "region",
    "country_code",
    "tier"
]

for col in text_cols:
    df[col] = df[col].str.strip().str.upper()

print('textos normalizados')

#  evitar inconsistencias en riesgos 

df["risks_prevented"] = df[
    ["risks_prevented", "risks_registered"]
].min(axis=1)

print('inconsistencias en riesgos verificadas')

# -----------------------------
# 3. FEATURE ENGINEERING
# -----------------------------

# margen estimado
df["estimated_margin"] = (
    df["estimated_sell_price"] - df["forecast_cost"]
)

# margen final
df["final_margin"] = (
    df["final_sell_price"] - df["final_cost"]
)

# margen %
df["final_margin_pct"] = (
    df["final_margin"] / df["final_sell_price"]
)

# impacto de change orders
df["change_order_profit"] = (
    df["change_order_sell_price"] - df["change_order_cost"]
)

# retraso %
df["delay_ratio"] = (
    df["delays_days"] / df["estimated_duration_days"]
)

# eficiencia en mitigación de riesgos
df["risk_mitigation_rate"] = (
    df["risks_prevented"] / df["risks_registered"]
).fillna(0)

print('feature ing. terminada')

# -----------------------------
# 4. DATA QUALITY FLAGS
# -----------------------------

df["high_delay_flag"] = df["delay_ratio"] > 0.2
df["low_margin_flag"] = df["final_margin_pct"] < 0.1
df["risk_management_issue"] = df["risk_mitigation_rate"] < 0.5

print('quality flags ok')

# -----------------------------
# 5. LOAD
# -----------------------------

# guardar dataset limpio
df.to_csv("projects_clean.csv", index=False)

# formato analítico recomendado
df.to_parquet("projects_clean.parquet", index=False)

print("ETL completado")
print("\n\nRegistros finales:", len(df))