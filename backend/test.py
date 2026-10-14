from analyser import analyze_csv
import cleaner as cln

file_path="C:\Codes\csv_cleaner\data\sample_day10.csv"
df=cln.load_csv(file_path)
# res=analyze_csv(file_path)
# print(res)

# output_file = "C:\Codes\csv_cleaner\data\clean.csv"
# #Load CSV
# df = cln.load_csv(file_path)
    
# print("\nOriginal Data:")
# print(df)
    
# # Clean data
# cleaned_df = cln.clean_data(df)
    
# print("\nCleaned Data:")
# print(cleaned_df)
    
#     # Save cleaned CSV
# cleaned_df.to_csv(output_file, index=False)
    
# print(f"\nCleaned file saved to: {output_file}")

# print("\nSummary:")
# print(cln.get_cleaning_summary(df, cleaned_df))

# print(cln.get_before_after_report(df,cleaned_df))
# Test 1: Your default settings
cleaned_median = cln.clean_data(df)

print("\n--- Default cleaning ---")
print(cln.get_before_after_report(df, cleaned_median))

# Test 2: Fill numerical missing values with mean
cleaned_mean = cln.clean_data(
    df,
    numeric_strategy="mean"
)

print("\n--- Mean strategy ---")
print(cln.get_before_after_report(df, cleaned_mean))

# Test 3: Fill numerical missing values with zero
cleaned_zero = cln.clean_data(
    df,
    numeric_strategy="zero"
)

print("\n--- Zero strategy ---")
print(cln.get_before_after_report(df, cleaned_zero))

# Test 4: Fill text missing values with the most common value
cleaned_mode = cln.clean_data(
    df,
    text_strategy="mode"
)

print("\n--- Text mode strategy ---")
print(cln.get_before_after_report(df, cleaned_mode))

# Test 5: Keep duplicate rows
cleaned_keep_duplicates = cln.clean_data(
    df,
    remove_duplicate_rows=False
)

print("\n--- Duplicates retained ---")
print(cln.get_before_after_report(df, cleaned_keep_duplicates))
    