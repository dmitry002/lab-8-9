import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

folder = os.path.dirname(os.path.abspath(__file__))
file_name = ""
for f in os.listdir(folder):
    if f.startswith("comptage") and "2018" in f:
        file_name = os.path.join(folder, f)

if file_name == "":
    print("Помилка: файл comptage_velo_2018.csv не знайдено у папці", folder)
    exit()

print("Файл:", file_name)

df = pd.read_csv(file_name, sep=None, engine='python', encoding='latin1')
df = df.loc[:, ~df.columns.str.contains('Unnamed')]
date_col = df.columns[0]
df[date_col] = pd.to_datetime(df[date_col], format='mixed', dayfirst=True)
df = df.set_index(date_col)
df = df.select_dtypes(include='number')

print(df.head())
print(df.info())
print(df.describe())

total = df.sum().sum()
print("\nЗагальна кількість велосипедистів за 2018 рік:", int(total))

print("\nКількість велосипедистів на кожній велодоріжці:")
print(df.sum().sort_values(ascending=False))

monthly = df.groupby(df.index.month).sum()
monthly.index.name = 'Month'
print("\nКількість велосипедистів за місяцями:")
print(monthly)

paths = df.columns[:3]
for p in paths:
    print("\nВелодоріжка:", p)
    print("Найпопулярніший місяць:", monthly[p].idxmax())
    print("Кількість велосипедистів:", int(monthly[p].max()))

path = df.columns[0]
print("\nДинаміка використання велодоріжки", path)
print(monthly[path])

monthly[path].plot(kind='line', marker='o')
plt.title('Кількість велосипедистів на велодоріжці ' + path + ' за 2018 рік')
plt.xlabel('Місяць')
plt.ylabel('Кількість велосипедистів')
plt.xticks(range(1, 13))
plt.show()