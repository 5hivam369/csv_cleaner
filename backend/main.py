print("CSV Cleaner backend satrting")
from analyser import analyze_csv
# import cleaner as cln
from fastapi import FastAPI,UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import tempfile
import pandas as pd
from cleaner import clean_data, get_cleaning_summary, get_before_after_report
import os
import json

def validate_csv_file(file:UploadFile):
    #checks filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )
    
    #check file extenstion
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a CSV file."
        )
    
    # Check whether file is empty
    content = file.file.read()
    file.file.seek(0)

    if not content or not content.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV file is empty."
        )  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/preview")
async def preview_csv(file: UploadFile=File(...)):
    
    #validate uploaded CSV
    validate_csv_file(file)
    
    #read only the first 10 rows
    df =pd.read_csv(file.file, nrows=10)
    
    #convert data into JSON-friendly format
    preview_data=json.loads(
        df.to_json(orient="records")
    )
    
    return{
        "columns": df.columns.tolist(),
        "rows": preview_data,
        "preview_count": len(preview_data)
    }

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
    validate_csv_file(file)
    
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
async def clean(
    file: UploadFile = File(...),
    numeric_strategy: str = Form("median"),
    text_strategy: str = Form("unknown"),
    remove_duplicate_rows: bool = Form(True)
):
    validate_csv_file(file)

    if not file.filename.lower().endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    contents = await file.read()

    input_path = None

    try:
        # Create temporary input file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        ) as temp_file:
            temp_file.write(contents)
            input_path = temp_file.name

        # Read original CSV
        original_df = pd.read_csv(input_path)

        # Clean CSV using selected settings
        cleaned_df = clean_data(
            original_df,
            numeric_strategy=numeric_strategy,
            text_strategy=text_strategy,
            remove_duplicate_rows=remove_duplicate_rows
        )

        # Generate before-and-after summary
        summary = get_before_after_report(
            original_df,
            cleaned_df
        )

        # Record cleaning settings
        settings = {
            "numeric_strategy": numeric_strategy,
            "text_strategy": text_strategy,
            "remove_duplicate_rows": remove_duplicate_rows
        }

        # Generate quality report
        report = {
            "filename": file.filename,
            "summary": summary,
            "settings": settings
        }

        # Convert cleaned DataFrame directly into CSV text
        cleaned_csv = cleaned_df.to_csv(index=False)

        return {
            "filename": file.filename,
            "summary": summary,
            "settings": settings,
            "cleaned_csv": cleaned_csv,
            "quality_report": report
        }

    except ValueError as exc:
        return {"error": str(exc)}

    finally:
        if input_path and os.path.exists(input_path):
            os.remove(input_path)

    
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

@app.get("/download_report")
def download_report(path: str):
    if not os.path.exists(path):
        return{"error":"Report file not found"}
    
    return FileResponse(
        path,
        media_type="application/json",
        filename="data_quality_report.json"
    )