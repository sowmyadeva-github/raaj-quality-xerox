document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector('input[type="file"]');
    const fileName = document.getElementById("selected-file");
    const uploadBox = document.querySelector(".upload-inner");

    if (!fileInput || !fileName || !uploadBox) return;

    function updateFileName(file) {
        if (file) {
            fileName.textContent = "Selected: " + file.name;
            uploadBox.classList.add("file-selected");
        } else {
            fileName.textContent = "No file selected yet";
            uploadBox.classList.remove("file-selected");
        }
    }

    fileInput.addEventListener("change", function () {
        updateFileName(this.files[0]);
    });

    uploadBox.addEventListener("dragover", function (e) {
        e.preventDefault();
        uploadBox.classList.add("drag-active");
    });

    uploadBox.addEventListener("dragleave", function () {
        uploadBox.classList.remove("drag-active");
    });

    uploadBox.addEventListener("drop", function (e) {
        e.preventDefault();
        uploadBox.classList.remove("drag-active");

        const file = e.dataTransfer.files[0];

        if (file) {
            fileInput.files = e.dataTransfer.files;
            updateFileName(file);
        }
    });
});