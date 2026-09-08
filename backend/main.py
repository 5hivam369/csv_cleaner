print("CSV Cleaner backend satrting")
from analyser import analyze_csv
# import cleaner as cln
from fastapi import FastAPI,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile

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