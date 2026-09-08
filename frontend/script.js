const fileInput = document.getElementById("csvfile");
const analyzeButton = document.getElementById("analyzebtn");

const statusText = document.getElementById("status");

const filenameElement= document.getElementById("filename")
const rowsElement = document.getElementById("rows");
const columnsElement = document.getElementById("columns");
const missingElement = document.getElementById("missing");
const duplicatesElement = document.getElementById("duplicates");

analyzeButton.addEventListener("click", analyzeCSV);

async function analyzeCSV() {
    const file = fileInput.files[0];

    if (!file) {
        statusText.textContent = "Please select a CSV file.";
        return;
    }
    statusText.textContent = "Analyzing...";
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
            method: "Post",
            body: formData
        }
    );

    const data = await response.json();
    console.log(data);

    filenameElement.textContent= data.filename;
    rowsElement.textContent = data.rows;
    columnsElement.textContent = data.columns;
    missingElement.textContent = data.missing_values;
    duplicatesElement.textContent = data.duplicate_rows;

    statusText.textContent = "Analysis complete!";
}


