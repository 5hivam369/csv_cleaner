# csv_cleaner
A web based csv cleaning and analysis tool built with **FastAPI, Pyhton, HTML, CSS and Javascript**.

CSV Cleaner helps analyze messy CSV files, identify data quality, clean datasets and download the clean file along with quality report.

## Features
- Upload and analyze CSV files.
- View data information including rows and columns.
- Identify missing values and duplicate rows.
- Clean missing values using configurable strategies.
- Replace missing numerical values with the median.
- Replace missing text values with "Unknown".
- Remove duplicate rows.
- Generate before and after data quality reports.
- Calculate data quality score.
- Visualize data using chart.
- Download cleaned CSV files.
- Responsive UI.

## Tech Stack
 ### Frontend
- HTML5
- CSS3
- Javascript
 ### Backend  
- Python
- FastAPI
- Pandas
- Numpy
 ### Deployement
- Vercel

## How it works
1. Upload CSV file.
2. Analyze the dataset to identify missing values and duplicates.
3. Select the desired cleaning option.
4. Clean the dataset.
5. Review the before and after quality report.
6. Download the cleaned CSV file.

## Run Locally
### 1. Clone the repository

git clone https://github.com/5hivam369/csv_cleaner.git

### 2. Navigate to the project

cd csv_cleaner

### 3. Install backend dependencies

cd backend
pip install -r requirements.txt

### 4. Start the backend

uvicorn main:app --reload

### 5. Open the frontend

Open frontend/index.html in your browser.

Make sure the frontend API configuration points to your local backend.

## Project Structure
csv_cleaner/  
  - backend/  
    - main.py  
    - analyser.py  
    - cleaner.py  
    - requirement.txt  
  - frontend/  
    - index.html  
    - style.css  
    - script.js  
  - README.md  

## What I Learned

- Building REST APIs using FastAPI
- Working with CSV files using Pandas
- Handling missing values and duplicate records
- Connecting a frontend with a backend API
- Handling file uploads and downloads
- Building responsive web interfaces
- Deploying a full-stack application

## Author
Shivam Verma
