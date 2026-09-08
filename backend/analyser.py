import pandas as pd

def analyze_csv(file_path):
    """Aalyses and give a describtion of the given csv file"""
    df = pd.read_csv(file_path)
    analysis= {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_names": list(df.columns),
        "data_types": {
            column: str(df[column].dtype)
            for column in df.columns
        }
    }
    
    return analysis