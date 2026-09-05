import pandas as pd


def load_csv(file_path):
    """Load a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def clean_column_names(df):
    """Clean and standardize column names."""
    
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    
    return df


def remove_duplicates(df):
    """Remove duplicate rows."""
    
    before = len(df)
    
    df = df.drop_duplicates()
    
    after = len(df)
    
    print(f"Removed {before - after} duplicate rows.")
    
    return df


def handle_missing_values(df):
    """Handle missing values in the dataset."""
    
    # Fill numerical columns with their median
    numerical_columns = df.select_dtypes(include="number").columns
    
    for column in numerical_columns:
        df[column] = df[column].fillna(df[column].median())
    
    # Fill text columns with "Unknown"
    text_columns = df.select_dtypes(include="object").columns
    
    for column in text_columns:
        df[column] = df[column].fillna("Unknown")
    
    return df


def clean_data(df):
    """Run the complete cleaning pipeline."""
    
    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    
    return df