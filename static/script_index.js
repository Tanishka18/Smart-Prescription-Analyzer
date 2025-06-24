console.log("✅ script_index.js loaded");
// File input and display functionality
const fileInput = document.getElementById("imageInput");
const dropArea = document.getElementById("dropArea");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

// Update upload area to show selected file
function updateUploadDisplay(file) {
  if (file) {
    // Update the upload area content to show file name
    dropArea.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14,2 14,8 20,8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10,9 9,9 8,9"></polyline>
      </svg>
      <h3 style="color: #4f46e5;">File Selected!</h3>
      <p style="font-weight: 600; color: #374151;">${file.name}</p>
      <p class="file-info">Size: ${(file.size / 1024 / 1024).toFixed(2)} MB</p>
      <p style="font-size: 0.875rem; color: #6b7280;">Click to choose a different file</p>
    `;
    
    // Show the clear button
    clearBtn.classList.remove("hidden");
    analyzeBtn.textContent = "Analyze Prescription";
  } else {
    // Reset to original state
    dropArea.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="17 8 12 3 7 8"></polyline>
        <line x1="12" y1="3" x2="12" y2="15"></line>
      </svg>
      <h3>Drag and drop your prescription image here</h3>
      <p>or click to browse files</p>
      <p class="file-info">Supported formats: JPG, PNG, PDF - Max size: 10MB</p>
    `;
    
    // Hide the clear button
    clearBtn.classList.add("hidden");
    analyzeBtn.textContent = "Analyze Prescription";
  }
}

// File input change event
fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  updateUploadDisplay(file);
});

// Clear button functionality
clearBtn.addEventListener("click", () => {
  fileInput.value = "";
  updateUploadDisplay(null);
  document.getElementById("results").classList.add("hidden");
  document.getElementById("loading").classList.add("hidden");
});

// Drag and drop functionality
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.borderColor = "#4f46e5";
  dropArea.style.backgroundColor = "#f8fafc";
});

dropArea.addEventListener("dragleave", (e) => {
  e.preventDefault();
  dropArea.style.borderColor = "#d1d5db";
  dropArea.style.backgroundColor = "transparent";
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.style.borderColor = "#d1d5db";
  dropArea.style.backgroundColor = "transparent";
  
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    // Check if file type is supported
    if (file.type.startsWith('image/') || file.type === 'application/pdf') {
      fileInput.files = files;
      updateUploadDisplay(file);
    } else {
      alert("Please upload an image file (JPG, PNG) or PDF.");
    }
  }
});

// Analyze button functionality
analyzeBtn.addEventListener("click", () => {
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload a prescription image.");
    return;
  }

  // Show loading animation
  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("results").classList.add("hidden");

  const formData = new FormData();
  formData.append("prescription", file);

  fetch("/analyze", {
    method: "POST",
    body: formData
  })
  .then(response => response.text()) // We get rendered HTML
  .then(html => {
    document.open();
    document.write(html);
    document.close();
  })
  .catch(error => {
    console.error("Error analyzing prescription:", error);
    alert("An error occurred during analysis.");
    document.getElementById("loading").classList.add("hidden");
  });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Contact form submission
document.getElementById('contactForm').addEventListener('submit', function(e) {
  e.preventDefault();
  // Add your form submission logic here
  alert('Thank you for your message! We will get back to you soon.');
  this.reset();
});