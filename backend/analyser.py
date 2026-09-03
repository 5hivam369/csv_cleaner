import pandas as pd

df = pd.read_csv("C:\Codes\csv_cleaner\data\machine-readable-business-employment-data-mar-2026-quarter.csv")

print("Head:")
print(df.head(5))
print("\nShape:",df.shape)
print("\nColumns:")
print(df.columns)
print("\nData type:")
print(df.dtypes)
print("\nNull values:")
print(df.isnull().sum())
print("\nDuplicates:",df.duplicated().sum())