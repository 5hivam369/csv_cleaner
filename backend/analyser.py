import pandas as pd

def analyse_csv(file_path):
    """Aalyses and give a describtion of the given csv file"""
    df = pd.read_csv(file_path)
    return {
        'Head':df.head(5),
        'Columns':df.columns,
        'Data Type':df.dtypes,
        'Missing Values':df.isnull().sum(),
        'Duplicates':df.duplicated().sum()
    }