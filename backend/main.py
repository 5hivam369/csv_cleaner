print("CSV Cleaner backend satrting")
import analyser
file_path="C:\Codes\csv_cleaner\data\machine-readable-business-employment-data-mar-2026-quarter.csv"
res=analyser.analyse_csv(file_path)
print(res)