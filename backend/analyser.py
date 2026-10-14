import pandas as pd

def analyze_csv(file_path):
    """Aalyses and give a describtion of the given csv file"""
    df = pd.read_csv(file_path)
    total_cells= int(df.shape[0] * df.shape[1])
    
    missing_cells=int(df.isna().sum().sum())
    duplicated_rows=int(df.duplicated().sum())
    
    if total_cells>0:
        missing_percentage=round((missing_cells/total_cells)*100,2)
    else:
        missing_percentage=0
    
    if len(df)>0:
        duplicate_percentage=round((duplicated_rows/len(df))*100,2) 
    else:
        duplicate_percentage=0
    
    quality_score=round(100-(missing_percentage+duplicate_percentage),2)        
    
    quality_score=max(0,(min(100,quality_score)))
    analysis= {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_names": list(df.columns),
        "data_types": {
            column: str(df[column].dtype)
            for column in df.columns
        },
        "missing_by_column": {
        column: int(df[column].isna().sum())
        for column in df.columns},
        "missing_percentage": missing_percentage,
        "duplicate_percentage": duplicate_percentage,
        "quality_score": quality_score,
    }
    
    return analysis