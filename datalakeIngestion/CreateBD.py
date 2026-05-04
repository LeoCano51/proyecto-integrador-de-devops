import pandas as pd
import random

# Número de proyectos
n_proyectos = 5000

# Line of Business
line_of_business = ["Energy", "Install", "Service"]

# Country codes (2 por continente)
country_codes = {
    "North America": ["US", "MX"],
    "South America": ["BR", "AR"],
    "Europe": ["DE", "FR"],
    "Africa": ["ZA", "EG"],
    "Asia": ["CN", "JP"],
    "Oceania": ["AU", "NZ"]
}

data = []

def calculate_tier(cost):
    if cost > 10000000:
        return "Tier 1"
    elif cost > 5000000:
        return "Tier 2"
    elif cost > 1000000:
        return "Tier 3"
    elif cost > 250000:
        return "Tier 4"
    else:
        return "Tier 5"

for i in range(n_proyectos):

    project_id = f"PRJ-{i+1:04d}"

    business = random.choice(line_of_business)

    # Elegir continente y país
    region = random.choice(list(country_codes.keys()))
    country = random.choice(country_codes[region])

    # Forecast cost
    forecast_cost = random.randint(50000, 5000000)

    # Estimated sell price
    sell_multiplier = random.uniform(0.6, 1.8)
    estimated_sell_price = forecast_cost * sell_multiplier

    # Change orders cost (0–30%)
    change_order_cost = forecast_cost * random.uniform(0, 0.3)

    # Change orders sell price
    change_orders_sell_price = change_order_cost * random.uniform(1.0, 1.5)

    # Final cost
    final_cost = forecast_cost + change_order_cost

    # Final sell price
    final_sell_price = estimated_sell_price + change_orders_sell_price

    # Duración estimada (15 días a 5 años)
    duration_days = random.randint(15, 1825)

    # Retrasos (0–20%)
    delays = int(duration_days * random.uniform(0, 0.2))

    # Duración final
    final_duration = duration_days + delays

    # Tier basado en final cost
    tier = calculate_tier(final_cost)

    data.append({
        "Project_ID": project_id,
        "Line_of_Business": business,
        "Region": region,
        "Country_Code": country,
        "Forecast_Cost": round(forecast_cost,2),
        "Estimated_Sell_Price": round(estimated_sell_price,2),
        "Change_Order_Cost": round(change_order_cost,2),
        "Change_Order_Sell_Price": round(change_orders_sell_price,2),
        "Final_Cost": round(final_cost,2),
        "Final_Sell_Price": round(final_sell_price,2),
        "Estimated_Duration_Days": duration_days,
        "Delays_Days": delays,
        "Final_Duration_Days": final_duration,
        "Tier": tier
    })

df = pd.DataFrame(data)

# Exportar dataset
df.to_csv("synthetic_projects_dataset.csv", index=False)

print("Dataset generado correctamente")
print(df.head())