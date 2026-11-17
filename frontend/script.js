const fileInput = document.getElementById("csvfile");
const API_BASE_URL = "http://127.0.0.1:8000";
console.log("File input:", fileInput);
console.log("Selected files:", fileInput?.files);

const analyzeButton = document.getElementById("analyzebtn");

const analyse_statusText = document.getElementById("analyse_status");
const clean_statusText = document.getElementById("clean_status");
const preview_statusText = document.getElementById("preview_status");

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
const columnNamesChangedElement = document.getElementById("columnNamesChanged");

const uploadBox = document.getElementById("uploadBox");
const selectedFile = document.getElementById("selectedFile")

const columnTableBody = document.getElementById("columnTableBody");

const chartCanvas = document.getElementById("missingChart");
let missingChart = null;

const qualityScoreElement = document.getElementById("qualityScore");
const missingPercentageElement = document.getElementById("missingPercentage");
const duplicatePercentageElement = document.getElementById("duplicatePercentage");

const numericStrategyElement = document.getElementById("numericStrategy");
const textStrategyElement = document.getElementById("textStrategy");
const removeDuplicatesElement = document.getElementById("removeDuplicates");

const appliedNumericStrategy = document.getElementById("appliedNumericStrategy");
const appliedTextStrategy = document.getElementById("appliedTextStrategy");
const appliedDuplicateSetting = document.getElementById("appliedDuplicateSetting");
const downloadreportbtn = document.getElementById("downloadReportBtn");

const previewButton = document.getElementById("previewBtn");
const previewInfo = document.getElementById("previewInfo");
const previewTableHead = document.getElementById("previewTableHead");
const previewTableBody = document.getElementById("previewTableBody");

analyzeButton.addEventListener("click", analyzeCSV);

async function analyzeCSV() {
    const file = fileInput.files[0];

    if (!file) {
        statusText.textContent = "Please select a CSV file.";
        return;
    }
    analyse_statusText.textContent = "Analyzing...";
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `${API_BASE_URL}/analyze`,
        {
            method: "Post",
            body: formData
        }
    );

    const data = await response.json();
    if (!response.ok) {
        analyse_statusText.textContent = data.detail || "Something went wrong.";
        return;
    }
    console.log(data);

    filenameElement.textContent = data.filename;
    rowsElement.textContent = data.rows;
    columnsElement.textContent = data.columns;
    missingElement.textContent = data.missing_values;
    duplicatesElement.textContent = data.duplicate_rows;

    qualityScoreElement.textContent = data.quality_score;
    missingPercentageElement.textContent = data.missing_percentage + "%";
    duplicatePercentageElement.textContent = data.duplicate_percentage + "%";

    columnTableBody.replaceChildren();
    for (const columnName of data.column_names) {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.textContent = columnName;

        const typeCell = document.createElement("td");
        typeCell.textContent = data.data_types[columnName];

        row.append(nameCell, typeCell);
        columnTableBody.appendChild(row);
    }
    // Count missing values in each column
    const missingLabels = [];
    const missingCounts = [];

    for (const columnName of data.column_names) {
        const missingCount = data.missing_by_column?.[columnName];

        missingLabels.push(columnName);
        missingCounts.push(Number(missingCount ?? 0));
    }

    // Replace the previous chart, if one exists
    if (missingChart) {
        missingChart.destroy();
    }

    missingChart = new Chart(chartCanvas, {
        type: "bar",

        data: {
            labels: missingLabels,
            datasets: [{
                label: "Missing Values",
                data: missingCounts,
                backgroundColor: "#3b82f6",
                borderRadius: 5
            }]
        },

        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },

            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    analyse_statusText.textContent = "Analysis complete!";
}

previewButton.addEventListener("click", previewCSV);

async function previewCSV() {
    const file = fileInput?.files?.[0];

    if (!file) {
        preview_statusText.textContent = "Please select a CSV file.";
        return;
    }

    preview_statusText.textContent = "Loading Preview...";

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch(
            `${API_BASE_URL}/preview`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            statusText.textContent =
                data.detail || "Unable to preview CSV.";
            return;
        }
        // Clear previous preview
        previewTableHead.replaceChildren();
        previewTableBody.replaceChildren();

        // Create table headers
        const headerRow = document.createElement("tr");

        data.columns.forEach(column => {
            const th = document.createElement("th");
            th.textContent = column;
            headerRow.appendChild(th);
        });

        previewTableHead.appendChild(headerRow);

        // Create table rows
        data.rows.forEach(rowData => {

            const row = document.createElement("tr");

            data.columns.forEach(column => {

                const cell = document.createElement("td");

                cell.textContent = rowData[column] ?? "";

                row.appendChild(cell);
            });

            previewTableBody.appendChild(row);
        });

        // Display preview information
        previewInfo.textContent =
            `Showing ${data.preview_count} rows out of the first 10 rows.`;

        preview_statusText.textContent = "Preview loaded successfully!";

    } catch (error) {

        preview_statusText.textContent =
            "Unable to connect to the server. Please try again.";

        console.error(error);
    }

}

cleanButton.addEventListener("click", cleanCSV);

async function cleanCSV() {
    const file = fileInput.files[0];

    if (!file) {
        clean_statusText.textContent = "Please select a CSV file";
        return;
    }

    clean_statusText.textContent = "Cleaning...";

    const formData = new FormData();

    formData.append("file", file);

    formData.append(
        "numeric_strategy",
        numericStrategyElement.value
    );

    formData.append(
        "text_strategy",
        textStrategyElement.value
    );

    formData.append(
        "remove_duplicate_rows",
        removeDuplicatesElement.checked ? "true" : "false"
    );

    const response = await fetch(
        `${API_BASE_URL}/clean`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();
    if (!response.ok) {
        clean_statusText.textContent = data.detail || "Something went wrong.";
        return;
    }
    console.log(data);

    const settings = data.settings;

    const numericLabels = {
        median: "Median",
        mean: "Mean",
        zero: "Zero",
        drop: "Drop rows with missing numerical values"
    };

    const textLabels = {
        unknown: '"Unknown"',
        mode: "Most common value",
        drop: "Drop rows with missing text values"
    };

    appliedNumericStrategy.textContent =
        "Numerical values: " +
        numericLabels[settings.numeric_strategy];

    appliedTextStrategy.textContent =
        "Text values: " +
        textLabels[settings.text_strategy];

    appliedDuplicateSetting.textContent =
        "Duplicate removal: " +
        (settings.remove_duplicate_rows ? "Enabled" : "Disabled");

    const summary = data.summary;

    const before = summary.before;
    const after = summary.after;
    const changes = summary.changes;

    originalRowsElement.textContent = before["Rows"];
    cleanedRowsElement.textContent = after["Rows"];
    duplicatesRemovedElement.textContent = changes["Duplicates removed"];
    missingChangedElement.textContent = changes["Missing Values Fixed"];
    columnNamesChangedElement.textContent = changes["Column names changed"];

    clean_statusText.textContent = "Cleaning complete!";

    // Create downloadable CSV file
    const csvBlob = new Blob(
        [data.cleaned_csv],
        { type: "text/csv;charset=utf-8;" }
    );

    const csvURL = URL.createObjectURL(csvBlob);

    downloadButton.href = csvURL;
    downloadButton.download = "cleaned.csv";
    downloadButton.style.display = "inline-block";


    // Create downloadable JSON quality report
    const reportBlob = new Blob(
        [JSON.stringify(data.quality_report, null, 4)],
        { type: "application/json" }
    );

    const reportURL = URL.createObjectURL(reportBlob);

    downloadreportbtn.href = reportURL;
    downloadreportbtn.download = "data_quality_report.json";
    downloadreportbtn.style.display = "inline-block";

}
uploadBox.addEventListener("click", function () {
    fileInput.click();
});

fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];

    if (file) {
        selectedFile.textContent = file.name;
    }
    else {
        selectedFile.textContent = "No file selected";
    }
});

//drag over box
uploadBox.addEventListener("dragover", function (event) {
    event.preventDefault();
    uploadBox.classList.add("dragover");
});

//Drag leave
uploadBox.addEventListener("dragleave", function () {
    uploadBox.classList.remove("dragover");
});

uploadBox.addEventListener("drop", function (event) {
    event.preventDefault();

    uploadBox.classList.remove("dragover");
    const file = event.dataTransfer.files[0];

    if (!file) { return; }

    if (!file.name.toLowerCase().endsWith(".csv")) {
        selectedFile.textContent = "Please select a CSV file.";
        return;
    }

    fileInput.files = event.dataTransfer.files;

    selectedFile.textContent = file.name;
});