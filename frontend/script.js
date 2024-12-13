const serverUrl = "http://127.0.0.1:8000"; // Update if your backend is hosted elsewhere

// Image Upload Elements
const imageInput = document.getElementById("imageInput");
const uploadButton = document.getElementById("uploadButton");
const loadingImage = document.getElementById("loadingImage");
const imagePreviewContainer = document.getElementById("imagePreviewContainer");
const imagePreview = document.getElementById("imagePreview");
const imageDescription = document.getElementById("imageDescription");
const audioPlayerContainer = document.getElementById("audioPlayerContainer");
const audioPlayback = document.getElementById("audioPlayback");

// Today's Diary Elements
const fetchTodayDiaryButton = document.getElementById("fetchTodayDiaryButton");
const loadingTodayDiary = document.getElementById("loadingTodayDiary");
const todayDiaryContent = document.getElementById("todayDiaryContent");

// Previous Diaries Elements
const fetchDiaryButton = document.getElementById("fetchDiaryButton");
const diaryDate = document.getElementById("diaryDate");
const loadingDiary = document.getElementById("loadingDiary");
const diaryContent = document.getElementById("diaryContent");

// All Diaries Elements
const fetchAllDiariesButton = document.getElementById("fetchAllDiariesButton");
const prevPageButton = document.getElementById("prevPageButton");
const nextPageButton = document.getElementById("nextPageButton");
const loadingAllDiaries = document.getElementById("loadingAllDiaries");
const allDiariesContent = document.getElementById("allDiariesContent");

// Camera Elements
const cameraStream = document.getElementById("cameraStream");
const startCameraButton = document.getElementById("startCameraButton");
const captureButton = document.getElementById("captureButton");
const canvasPreview = document.getElementById("canvasPreview");
const capturedImage = document.getElementById("capturedImage");
const processCapturedImageButton = document.getElementById("processCapturedImageButton");

let currentPage = 1;
const pageSize = 10;
let videoStream = null;

// Handle Image Preview
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
    } else {
        imagePreview.src = "";
        imagePreview.classList.add("hidden");
    }
});

// Start Camera
startCameraButton.addEventListener("click", async () => {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraStream.srcObject = videoStream;
        cameraStream.classList.remove("hidden");
        captureButton.classList.remove("hidden");
        startCameraButton.classList.add("hidden");
    } catch (error) {
        console.error("Error accessing the camera:", error);
        alert("Unable to access the camera. Please ensure it is connected and permissions are granted.");
    }
});

// Capture Image
captureButton.addEventListener("click", () => {
    const context = canvasPreview.getContext("2d");
    canvasPreview.width = cameraStream.videoWidth;
    canvasPreview.height = cameraStream.videoHeight;
    context.drawImage(cameraStream, 0, 0, canvasPreview.width, canvasPreview.height);

    const imageDataURL = canvasPreview.toDataURL("image/png");
    capturedImage.src = imageDataURL;
    capturedImage.classList.remove("hidden");
    processCapturedImageButton.classList.remove("hidden");

    // Stop the camera
    videoStream.getTracks().forEach(track => track.stop());
    cameraStream.classList.add("hidden");
    captureButton.classList.add("hidden");
    startCameraButton.classList.remove("hidden");
});

// Process Image Function (Common for Uploaded and Captured)
async function processImage(file) {
    // Show loader
    loadingImage.classList.remove("hidden");
    imageDescription.textContent = "";
    audioPlayerContainer.classList.add("hidden");

    // Prepare form data
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${serverUrl}/process_image/`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to process the image.");
        }

        const data = await response.json();

        // Display description
        imageDescription.textContent = data.description;

        // Display audio
        if (data.audio_url) {
            audioPlayback.src = data.audio_url;
            audioPlayerContainer.classList.remove("hidden");
        }
    } catch (error) {
        console.error("Error processing image:", error);
        imageDescription.textContent = "An error occurred while processing the image.";
    } finally {
        // Hide loader
        loadingImage.classList.add("hidden");
    }
}

// Upload Button
uploadButton.addEventListener("click", async () => {
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image to upload.");
        return;
    }
    await processImage(file);
});

// Process Captured Image Button
processCapturedImageButton.addEventListener("click", async () => {
    const response = await fetch(capturedImage.src);
    const blob = await response.blob();
    const file = new File([blob], "captured-image.png", { type: "image/png" });
    await processImage(file);
});

// Fetch Today's Diary
fetchTodayDiaryButton.addEventListener("click", async () => {
    // Show loader
    loadingTodayDiary.classList.remove("hidden");
    todayDiaryContent.textContent = "";

    try {
        const response = await fetch(`${serverUrl}/daily_summary/`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch today's diary.");
        }

        const data = await response.json();

        if (data.message) {
            todayDiaryContent.textContent = data.message;
        } else {
            todayDiaryContent.innerHTML = `
                <p><strong>Summary:</strong> ${data.summary}</p>
                <audio controls src="${data.podcast_url}" class="mt-4"></audio>
            `;
        }
    } catch (error) {
        console.error("Error fetching today's diary:", error);
        todayDiaryContent.textContent = "An error occurred while fetching today's diary.";
    } finally {
        loadingTodayDiary.classList.add("hidden");
    }
});

// Fetch Diary for a Specific Date
fetchDiaryButton.addEventListener("click", async () => {
    const selectedDate = diaryDate.value;
    if (!selectedDate) {
        alert("Please select a date.");
        return;
    }

    // Show loader
    loadingDiary.classList.remove("hidden");
    diaryContent.textContent = "";

    try {
        const response = await fetch(`${serverUrl}/daily_summary/?date=${selectedDate}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch diary.");
        }

        const data = await response.json();

        if (data.message) {
            diaryContent.textContent = data.message;
        } else {
            diaryContent.innerHTML = `
                <p><strong>Summary:</strong> ${data.summary}</p>
                <audio controls src="${data.podcast_url}" class="mt-4"></audio>
            `;
        }
    } catch (error) {
        console.error("Error fetching diary:", error);
        diaryContent.textContent = "An error occurred while fetching the diary.";
    } finally {
        loadingDiary.classList.add("hidden");
    }
});

// Fetch All Diaries with Pagination
fetchAllDiariesButton.addEventListener("click", () => {
    currentPage = 1;
    fetchAllDiaries(currentPage);
});

prevPageButton.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        fetchAllDiaries(currentPage);
    }
});

nextPageButton.addEventListener("click", () => {
    currentPage++;
    fetchAllDiaries(currentPage);
});

async function fetchAllDiaries(page) {
    // Show loader
    loadingAllDiaries.classList.remove("hidden");
    allDiariesContent.innerHTML = "";

    try {
        const response = await fetch(`${serverUrl}/fetch_all_diaries/?page=${page}&page_size=${pageSize}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch all diaries.");
        }

        const data = await response.json();

        if (data.diaries.length === 0) {
            allDiariesContent.textContent = "No diary entries found.";
            return;
        }

        data.diaries.forEach(diary => {
            const diaryCard = document.createElement("div");
            diaryCard.className = "bg-gray-100 p-4 rounded shadow";

            diaryCard.innerHTML = `
                <p><strong>Date:</strong> ${diary.date}</p>
                <p><strong>Summary:</strong> ${diary.summary}</p>
                ${diary.podcast_url ? `<audio controls src="${diary.podcast_url}" class="mt-2"></audio>` : ""}
            `;

            allDiariesContent.appendChild(diaryCard);
        });

        // Update button states
        prevPageButton.disabled = page <= 1;
        nextPageButton.disabled = data.diaries.length < pageSize;
    } catch (error) {
        console.error("Error fetching all diaries:", error);
        allDiariesContent.textContent = "An error occurred while fetching the diaries.";
    } finally {
        loadingAllDiaries.classList.add("hidden");
    }
}
