const fileInput = document.getElementById("csvfile");
const analyzeButton = document.getElementById("analyzebtn");

const statusText = document.getElementById("status");

const filenameElement = document.getElementById("filename")
const rowsElement = document.getElementById("rows");
const columnsElement = document.getElementById("columns");
const missingElement = document.getElementById("missing");
const duplicatesElement = document.getElementById("duplicates");
const cleanButton = document.getElementById("cleanBtn");

const downloadButton = document.getElementById("downloadBtn");

const originalRowsElement = document.getElementById("originalRows");
const cleanedRowsElement = document.getElementById("cleanedRows");
const duplicatesRemovedElement = document.getElementById("duplicatesRemoved");
const missingChangedElement = document.getElementById("missingChanged");


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

    filenameElement.textContent = data.filename;
    rowsElement.textContent = data.rows;
    columnsElement.textContent = data.columns;
    missingElement.textContent = data.missing_values;
    duplicatesElement.textContent = data.duplicate_rows;

    statusText.textContent = "Analysis complete!";
}

cleanButton.addEventListener("click", cleanCSV);

async function cleanCSV() {
    const file = fileInput.files[0];

    if (!file) {
        statusText.textContent = "Please select a CSV file";
        return;
    }

    statusText.textContent = "Cleaning...";

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        "http://127.0.0.1:8000/clean",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();
    console.log(data);

    const summary = data.summary;

    originalRowsElement.textContent =summary["Original rows"];
    cleanedRowsElement.textContent =summary["Cleaned rows"];
    duplicatesRemovedElement.textContent =summary["Duplicates removed"];
    missingChangedElement.textContent = summary["Missing Values"];

    statusText.textContent = "Cleaning complete!";

    downloadButton.href = "http://127.0.0.1:8000/download?path=" + encodeURIComponent(data.download_path);
    downloadButton.style.display = "inline-block";

}
