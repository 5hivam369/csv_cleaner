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

def get_missing_value_report(df):
    """Tells how many missing values each column has."""
    return df.isna().sum().to_dict()

def handle_missing_values(
    df,
    numeric_strategy="median",
    text_strategy="unknown"
):
    """Handle missing values using the selected strategies."""

    df = df.copy()

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    text_columns = df.select_dtypes(
        include="object"
    ).columns

    # Validate the selected strategies
    if numeric_strategy not in ["median", "mean", "zero", "drop"]:
        raise ValueError("Invalid numerical cleaning strategy")

    if text_strategy not in ["unknown", "mode", "drop"]:
        raise ValueError("Invalid text cleaning strategy")

    # Drop rows missing numerical values, if requested
    if numeric_strategy == "drop" and len(numerical_columns) > 0:
        df = df.dropna(subset=list(numerical_columns))

    # Drop rows missing text values, if requested
    if text_strategy == "drop" and len(text_columns) > 0:
        df = df.dropna(subset=list(text_columns))

    # Handle numerical columns
    if numeric_strategy != "drop":
        for column in numerical_columns:
            if df[column].isna().all():
                print(
                    f"Column '{column}' contains only missing values."
                )
                continue

            if numeric_strategy == "median":
                fill_value = df[column].median()

            elif numeric_strategy == "mean":
                fill_value = df[column].mean()

            else:  # zero
                fill_value = 0

            df[column] = df[column].fillna(fill_value)

    # Handle text columns
    if text_strategy != "drop":
        for column in text_columns:
            if text_strategy == "unknown":
                df[column] = df[column].fillna("Unknown")

            elif text_strategy == "mode":
                modes = df[column].mode()

                if not modes.empty:
                    df[column] = df[column].fillna(modes.iloc[0])
                else:
                    df[column] = df[column].fillna("Unknown")

    return df


def clean_data(
    df,
    numeric_strategy="median",
    text_strategy="unknown",
    remove_duplicate_rows=True
):
    """Run the complete cleaning pipeline with user options."""

    df = df.copy()

    df = clean_column_names(df)

    if remove_duplicate_rows:
        df = remove_duplicates(df)

    df = handle_missing_values(
        df,
        numeric_strategy=numeric_strategy,
        text_strategy=text_strategy
    )

    return df

def get_cleaning_summary(original_df, cleaned_df):
    
    return{
        'Original rows':len(original_df),
        'Cleaned rows':len(cleaned_df),
        'Duplicates removed':int(original_df.duplicated().sum()),
        'Missing Values Before':original_df.isna().sum().sum(),
        'Mising Values After':cleaned_df.isna().sum().sum(),
        'Missing Values Fixed':original_df.isna().sum().sum()-cleaned_df.isna().sum().sum()
        }
    
def get_datatype_report(df):
    """Returns data type of each columns"""
    
    return{
        column:str(df[column].dtype)
        for column in df.columns
        
    }
    
def get_column_stats(df):
    """Returns basic statisctics fro each column."""
    stats={}
    
    for column in df.columns:
        if df[column].dtype =="int64" or df[column].dtype == "float64":
            
             if df[column].isna().all():
                stats[column]={
                'type':"numerical",
                "count":0,
                "mean":None,
                "median":None,
                "min":None,
                "max":None,
                "standard_deviation":None
                }
            
             else:
                stats[column]={
                'type':"numerical",
                "count":int(df[column].count()),
                "mean":float(df[column].mean()),
                "median":float(df[column].median()),
                "min":float(df[column].min()),
                "max":float(df[column].max()),
                "standard_deviation":float(df[column].std())
                }
        else:
            stats[column]={
                "type":"text",
                "count":int(df[column].count()),
                "unique_values":int(df[column].nunique()),
                "most_common":(
                                df[column].mode().iloc[0]
                               if not df[column].mode().empty
                                else None
                            )
            }
    return stats

def validate_dates(df,column):
    """Validate dates in a column."""
    dates=pd.to_datetime(df[column],errors="coerce")
    
    invalid_dates=dates.isna().sum()
    
    valid_dates=len(dates)-invalid_dates
    
    return{
        "valid_dates":int(valid_dates),
        "invalid_dates":int(invalid_dates)
    }

def get_before_after_report(original_df, cleaned_df):
    """Compare the dataset before and after cleaning."""

    column_names_changed = 0

    for original, cleaned in zip(
        original_df.columns,
        cleaned_df.columns
        ):
        if original != cleaned:
            column_names_changed += 1

    report = {
         "before": {
            "Rows": int(len(original_df)),
            "Columns": int(len(original_df.columns)),
            "Duplicate Rows": int(original_df.duplicated().sum()),
            "Missing Values": int(original_df.isna().sum().sum())
        },

        "after": {
            "Rows": int(len(cleaned_df)),
            "Columns": int(len(cleaned_df.columns)),
            "Duplicate Rows": int(cleaned_df.duplicated().sum()),
            "Missing Values": int(cleaned_df.isna().sum().sum())
        },

        "changes": {
            "Duplicates removed": int(
                len(original_df) - len(cleaned_df)
            ),

            "Missing Values Fixed": int(
                original_df.isna().sum().sum()
                - cleaned_df.isna().sum().sum()
            ),

            "Column names changed": int(column_names_changed)
        }
    }

    return report