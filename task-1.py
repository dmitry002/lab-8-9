import pandas as pd
import requests

try:
    df = pd.read_csv("gdp_per_capita.csv")
    print("Файл успішно завантажено")
except FileNotFoundError:
    print("Помилка: файл не знайдено")
    exit()

df = df.rename(columns={"GDP per capita (current US$)": "GDP_per_capita"})

def load_indicator(code, name):
    url = "https://api.worldbank.org/v2/country/all/indicator/" + code + "?date=2019&format=json&per_page=400"
    data = requests.get(url).json()[1]
    rows = []
    for item in data:
        rows.append({"Country": item["country"]["value"], name: item["value"]})
    return pd.DataFrame(rows)

df = df.merge(load_indicator("SP.POP.TOTL", "Population"), on="Country", how="left")
df = df.merge(load_indicator("SP.DYN.LE00.IN", "Life_expectancy"), on="Country", how="left")
df.to_csv("gdp_per_capita_full.csv", index=False)
print("Додано стовпці Population та Life_expectancy")

df = df.iloc[49:]

print("\nПочаткові дані:")
print(df)

print("\nПерші 3 рядки DataFrame:")
print(df.head(3))

print("\nТипи даних:")
print(df.dtypes)

print("\nРозмір DataFrame:")
print(df.shape)

print("\nОписова статистика:")
print(df.describe())

df = df.dropna()
df["Population"] = df["Population"].astype(int)
df["GDP_per_capita"] = df["GDP_per_capita"].round(2)
df["Life_expectancy"] = df["Life_expectancy"].round(1)

print("\nТипи даних після зміни:")
print(df.dtypes)

df["GDP_total_bln"] = (df["GDP_per_capita"] * df["Population"] / 1e9).round(2)

print("\nDataFrame з новим показником:")
print(df)

filtered_df = df[df["GDP_per_capita"] > 20000]
print("\nРезультат фільтрації (GDP_per_capita > 20000):")
print(filtered_df)

sorted_df = df.sort_values(by="GDP_per_capita", ascending=False)
print("\nРезультат сортування:")
print(sorted_df)

df["Income_group"] = pd.cut(
    df["GDP_per_capita"],
    bins=[0, 1100, 4500, 14000, 1000000],
    labels=["Low", "Lower middle", "Upper middle", "High"]
)

grouped_df = df.groupby("Income_group", observed=True).agg(
    GDP_mean=("GDP_per_capita", "mean"),
    GDP_max=("GDP_per_capita", "max"),
    GDP_min=("GDP_per_capita", "min"),
    Life_expectancy_mean=("Life_expectancy", "mean"),
    Countries=("Country", "count")
).round(2).reset_index()

print("\nРезультат групування:")
print(grouped_df)

print("\nКількість унікальних груп доходу:")
print(df["Income_group"].nunique())

print("\nКількість унікальних країн:")
print(df["Country"].nunique())

grouped_df.to_csv("analysis_result.csv", index=False)
print("\nРезультати збережено у файл analysis_result.csv")