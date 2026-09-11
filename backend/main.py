print("CSV Cleaner backend satrting")
from analyser import analyze_csv
# import cleaner as cln
from fastapi import FastAPI,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import tempfile
import pandas as pd
from cleaner import clean_data, get_cleaning_summary
import os

# file_path="C:\Codes\csv_cleaner\data\machine-readable-business-employment-data-mar-2026-quarter.csv"
# res=analyse_csv(file_path)
# print(res)

# output_file = "C:\Codes\csv_cleaner\data\clean.csv"
# Load CSV
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



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "CSV Cleaner API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        return {
            "error": "Only CSV files are allowed"
        }

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    ) as temp_file:

        temp_file.write(contents)
        temp_file_path = temp_file.name

    result = analyze_csv(temp_file_path)

    return {
      "filename":file.filename, 
        **result
    }

@app.post("/file-info")
async def file_info(file: UploadFile = File(...)):

    contents = await file.read()

    return {
        "filename": file.filename,
        "size": len(contents),
        "is_csv":file.filename.endswith(".csv")
    }
    
@app.post("/clean")
async def clean(file: UploadFile=File(...)):
    
    if not file.filename.endswith(".csv"):
        return {
            "erorr":"Only CSV file are allowed"
        }
    contents =await file.read()
    
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    ) as temp_file:
        temp_file.write(contents)
        input_path=temp_file.name
        
    original_df=pd.read_csv(input_path)
    cleaned_df=clean_data(original_df)
    
    summary=get_cleaning_summary(original_df,cleaned_df)
    
    output_path=tempfile.NamedTemporaryFile(delete=False,suffix="cleaned.csv").name
    
    cleaned_df.to_csv(output_path,index=False)
    
    return{
        "filename":file.filename,
        "summary":summary,
        "download_path":output_path
    }
    
@app.get("/download")

def download_file(path: str):
    if not os.path.exists(path):
        return{
            "error":"File not found"
        }
    return FileResponse(
        path,
        media_type="text/csv",
        filename="cleaned.csv"
    )