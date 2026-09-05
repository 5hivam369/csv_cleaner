print("CSV Cleaner backend satrting")
import analyser
import cleaner as cln
file_path="C:\Codes\csv_cleaner\data\machine-readable-business-employment-data-mar-2026-quarter.csv"
res=analyser.analyse_csv(file_path)
print(res)

output_file = "C:\Codes\csv_cleaner\data\clean.csv"
# Load CSV
df = cln.load_csv(file_path)
    
print("\nOriginal Data:")
print(df)
    
# Clean data
cleaned_df = cln.clean_data(df)
    
print("\nCleaned Data:")
print(cleaned_df)
    
    # Save cleaned CSV
cleaned_df.to_csv(output_file, index=False)
    
print(f"\nCleaned file saved to: {output_file}")