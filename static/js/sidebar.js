document.addEventListener("DOMContentLoaded", () => {
  // Initialize sidebar
  initializeSidebar()

  // Add mobile toggle button
  addMobileToggle()

  // Handle menu item clicks
  handleMenuClicks()

  // Handle image upload and preview
  initializeImageUpload()

  // Initialize form submission
  initializeFormSubmission()

  // Close modal when clicking outside
  window.addEventListener("click", (event) => {
    const modal = document.getElementById("imageModal")
    const recoModal = document.getElementById("recommendationsModal")
    if (modal && event.target === modal) {
      closeModal("imageModal")
    }
    if (recoModal && event.target === recoModal) {
      closeModal("recommendationsModal")
    }
  })

  // Handle window resize for sidebar
  window.addEventListener("resize", () => {
    handleToggleButtonVisibility()
  })
})

function initializeSidebar() {
  // Set active menu item - default to Upload Image
  const menuItems = document.querySelectorAll(".sidebar-menu .menu-item:not(.logout)")
  menuItems.forEach((item) => {
    item.classList.remove("active")
  })

  // Default to Upload Image as active
  const uploadItem = document.querySelector(".sidebar-menu .menu-item:first-child")
  if (uploadItem) {
    uploadItem.classList.add("active")
  }

  // Ensure only upload section is visible initially
  showUploadSection()
}

function addMobileToggle() {
  // Check if toggle button already exists
  if (document.querySelector(".sidebar-toggle")) {
    return
  }

  // Create mobile toggle button
  const toggleBtn = document.createElement("button")
  toggleBtn.className = "sidebar-toggle"
  toggleBtn.innerHTML = '<i class="fas fa-bars"></i>'
  toggleBtn.onclick = toggleSidebar

  // Add styles for the toggle button
  toggleBtn.style.cssText = `
        position: fixed;
        top: 70px;
        left: 15px;
        z-index: 1001;
        background: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 12px;
        font-size: 16px;
        cursor: pointer;
        display: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    `

  document.body.appendChild(toggleBtn)

  // Show/hide toggle button based on screen size
  handleToggleButtonVisibility()
  window.addEventListener("resize", handleToggleButtonVisibility)
}

function handleToggleButtonVisibility() {
  const toggleBtn = document.querySelector(".sidebar-toggle")
  if (toggleBtn) {
    if (window.innerWidth <= 768) {
      toggleBtn.style.display = "block"
    } else {
      toggleBtn.style.display = "none"
      // Close sidebar on desktop if it's open
      const sidebar = document.getElementById("sidebar")
      if (sidebar) {
        sidebar.classList.remove("active")
      }
    }
  }
}

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar")
  if (sidebar) {
    sidebar.classList.toggle("active")

    // Close sidebar on mobile after selection
    if (sidebar.classList.contains("active")) {
      setTimeout(() => {
        document.addEventListener("click", closeSidebarOnOutsideClick)
      }, 100)
    } else {
      document.removeEventListener("click", closeSidebarOnOutsideClick)
    }
  }
}

function closeSidebarOnOutsideClick(event) {
  const sidebar = document.getElementById("sidebar")
  const toggleBtn = document.querySelector(".sidebar-toggle")

  if (sidebar && toggleBtn) {
    if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
      sidebar.classList.remove("active")
      document.removeEventListener("click", closeSidebarOnOutsideClick)
    }
  }
}

function handleMenuClicks() {
  const menuItems = document.querySelectorAll(".sidebar-menu .menu-item:not(.logout)")

  menuItems.forEach((item, index) => {
    const link = item.querySelector(".menu-link")
    if (link) {
      link.addEventListener("click", (e) => {
        e.preventDefault()

        // Remove active class from all items
        menuItems.forEach((i) => i.classList.remove("active"))

        // Add active class to clicked item
        item.classList.add("active")

        // Handle different menu actions
        switch (index) {
          case 0:
            showUploadSection()
            break
          case 1:
            showCommonDiseases()
            break
          case 2:
            showRecentPictures()
            break
        }

        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
          const sidebar = document.getElementById("sidebar")
          if (sidebar) {
            sidebar.classList.remove("active")
          }
        }
      })
    }
  })
}

// Helper functions for section visibility
function hideAllSections() {
  const sections = document.querySelectorAll(".content-section")
  sections.forEach((section) => {
    section.style.display = "none"
  })
}

function showSection(sectionId) {
  hideAllSections()
  const section = document.getElementById(sectionId)
  if (section) {
    section.style.display = "block"
  }
}

function showUploadSection() {
  showSection("upload-section")
  resetForm() // Ensure form is clean when navigating back
}

function showCommonDiseases() {
  showSection("common-diseases")
  // Load content dynamically (as per your original script)
  const section = document.getElementById("common-diseases")
  if (section) {
    section.innerHTML = `
            <div class="card shadow-lg border-0">
                <div class="card-body p-5">
                    <h3 class="card-title text-center mb-4 display-6"><i class="fas fa-bug me-3"></i> Common Crop Diseases</h3>
                    <div class="alert alert-info text-center mb-4">
                        <i class="fas fa-info-circle me-2"></i> Here are some common crop diseases and their general characteristics.
                    </div>
                    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                        <div class="col">
                            <div class="card h-100 shadow-sm border-success">
                                <div class="card-body">
                                    <h5 class="card-title text-success"><i class="fas fa-leaf me-2"></i>Leaf Spot</h5>
                                    <p class="card-text"><strong>Symptoms:</strong> Small, dark spots on leaves that may have yellow halos.</p>
                                    <p class="card-text"><strong>Causes:</strong> Fungal infection, often due to high humidity.</p>
                                    <p class="card-text"><strong>Treatment:</strong> Remove infected leaves, apply fungicide, improve air circulation.</p>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card h-100 shadow-sm border-success">
                                <div class="card-body">
                                    <h5 class="card-title text-success"><i class="fas fa-cloud me-2"></i>Powdery Mildew</h5>
                                    <p class="card-text"><strong>Symptoms:</strong> White, powdery coating on leaves and stems.</p>
                                    <p class="card-text"><strong>Causes:</strong> Fungal infection in warm, humid conditions.</p>
                                    <p class="card-text"><strong>Treatment:</strong> Neem oil, baking soda spray, ensure good air circulation.</p>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card h-100 shadow-sm border-success">
                                <div class="card-body">
                                    <h5 class="card-title text-success"><i class="fas fa-fire me-2"></i>Blight</h5>
                                    <p class="card-text"><strong>Symptoms:</strong> Large brown or black patches on leaves, stems, or fruits.</p>
                                    <p class="card-text"><strong>Causes:</strong> Bacterial or fungal infection.</p>
                                    <p class="card-text"><strong>Treatment:</strong> Remove infected parts, copper-based fungicides, crop rotation.</p>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card h-100 shadow-sm border-success">
                                <div class="card-body">
                                    <h5 class="card-title text-success"><i class="fas fa-water me-2"></i>Root Rot</h5>
                                    <p class="card-text"><strong>Symptoms:</strong> Yellowing leaves, wilting, stunted growth.</p>
                                    <p class="card-text"><strong>Causes:</strong> Overwatering, poor drainage, fungal infection.</p>
                                    <p class="card-text"><strong>Treatment:</strong> Improve drainage, reduce watering, fungicide treatment.</p>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card h-100 shadow-sm border-success">
                                <div class="card-body">
                                    <h5 class="card-title text-success"><i class="fas fa-bug me-2"></i>Aphid Infestation</h5>
                                    <p class="card-text"><strong>Symptoms:</strong> Small green/black insects on leaves, sticky honeydew.</p>
                                    <p class="card-text"><strong>Causes:</strong> Pest infestation.</p>
                                    <p class="card-text"><strong>Treatment:</strong> Insecticidal soap, neem oil, beneficial insects.</p>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card h-100 shadow-sm border-success">
                                <div class="card-body">
                                    <h5 class="card-title text-success"><i class="fas fa-virus me-2"></i>Mosaic Virus</h5>
                                    <p class="card-text"><strong>Symptoms:</strong> Mottled yellow and green patterns on leaves.</p>
                                    <p class="card-text"><strong>Causes:</strong> Viral infection spread by insects.</p>
                                    <p class="card-text"><strong>Treatment:</strong> Remove infected plants, control insect vectors.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
  }
}

function showRecentPictures() {
  showSection("recent-pictures")
  updateRecentPicturesDisplay() // Call this to refresh the display
}

function resetForm() {
  const form = document.getElementById("cropForm")
  if (form) {
    form.reset() // Resets all form fields
  }
  const preview = document.getElementById("preview")
  if (preview) {
    preview.style.display = "none"
    document.getElementById("previewImg").src = ""
  }
  const resultMessage = document.getElementById("result-message")
  if (resultMessage) {
    resultMessage.innerHTML = ""
    resultMessage.style.display = "none"
  }
  const predictionResults = document.getElementById("prediction-results")
  if (predictionResults) {
    predictionResults.style.display = "none"
  }
}

function resetAndShowUpload() {
  resetForm()
  showUploadSection()
  // Also ensure the sidebar item is active
  const menuItems = document.querySelectorAll(".sidebar-menu .menu-item:not(.logout)")
  menuItems.forEach((item) => item.classList.remove("active"))
  const uploadItem = document.querySelector(".sidebar-menu .menu-item:first-child")
  if (uploadItem) {
    uploadItem.classList.add("active")
  }
}

// Fixed addToRecentImages function - now accepts diseaseDetails as parameter
async function addToRecentImages(imageSrc, diseaseDetails = null) {
  let recentImages = JSON.parse(sessionStorage.getItem("recentImages") || "[]")

  // Ensure diseaseDetails has required fields
  if (!diseaseDetails) {
    diseaseDetails = {
      predicted_class_name: "Unknown",
      confidence: 0,
      crop: "Unknown",
      disease: "Unknown",
      affected_parts: ["Unknown"],
      primary_affected: "Unknown",
      description: "No diagnosis available",
      symptoms: "Unable to determine symptoms",
      severity: "Unknown",
    }
  }
  const newImage = {
    src: imageSrc,
    timestamp: new Date().toISOString(),
    id: Date.now(), // Unique ID for each image
    diseaseDetails: diseaseDetails,
  }

  recentImages.unshift(newImage)

  // Keep only last 10 images
  if (recentImages.length > 10) {
    recentImages = recentImages.slice(0, 10)
  }

  sessionStorage.setItem("recentImages", JSON.stringify(recentImages))
  // updateRecentPicturesDisplay(); // This will be called when the section is shown

    try {
    await fetch('/store-diagnosis/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        imageSrc,
        diseaseDetails: diseaseDetails || {
          // Default values as before
        }
      })
    });
  } catch (error) {
    console.error('Failed to save diagnosis:', error);
  }
}

/**
 * Safely extracts and formats the display name for a disease, including crop.
 * @param {string | undefined | null} fullPredictedName The full predicted class name (e.g., "Apple___Apple_scab").
 * @returns {string} The cleaned display name (e.g., "Apple - Apple Scab" or "Healthy").
 */
function getDisplayDiseaseName(fullPredictedName) {
  if (!fullPredictedName) {
    return "Unknown"
  }
  const parts = fullPredictedName.split("___")
  if (parts.length === 2) {
    const crop = parts[0].replace(/_/g, " ")
    const disease = parts[1].replace(/_/g, " ")
    return `${crop} - ${disease}`
  }
  // If no "___" or not two parts, just clean the whole string
  return fullPredictedName.replace(/_/g, " ")
}

function updateRecentPicturesDisplay() {
  const recentImages = JSON.parse(sessionStorage.getItem("recentImages") || "[]")
  const recentPicturesSection = document.getElementById("recent-pictures")

  // --- DEBUGGING LOG ---
  console.log("Recent Images from sessionStorage:", recentImages)
  // --- END DEBUGGING LOG ---

  if (recentPicturesSection) {
    if (recentImages.length > 0) {
      recentPicturesSection.innerHTML = `
              <div class="card shadow-lg border-0">
                  <div class="card-body p-5">
                      <h3 class="card-title text-center mb-4 display-6"><i class="fas fa-images me-3"></i> Recent Pictures</h3>
                      <div class="alert alert-info text-center mb-4">
                          <i class="fas fa-info-circle me-2"></i> Click on any image to view detailed prediction results.
                      </div>
                      <div class="image-grid">
                          ${recentImages
                            .map(
                              (img) => `
                              <div class="recent-image-container" onclick="showImageModal('${img.id}')">
                                  <img src="${img.src}" alt="Recent Upload" class="img-fluid">
                                  <small class="text-muted d-block text-center mt-1">
                                      ${new Date(img.timestamp).toLocaleDateString()}
                                      <span class="badge ${getDiseaseBadgeClass(img.diseaseDetails?.predicted_class_name || "Unknown")}">
                                          ${getDisplayDiseaseName(img.diseaseDetails?.predicted_class_name)}
                                      </span>
                                  </small>
                              </div>
                          `,
                            )
                            .join("")}
                      </div>
                  </div>
              </div>
          `
    } else {
      recentPicturesSection.innerHTML = `
              <div class="card shadow-lg border-0">
                  <div class="card-body text-center p-5">
                      <h3 class="card-title text-center mb-4 display-6"><i class="fas fa-images me-3"></i> Recent Pictures</h3>
                      <div class="alert alert-info mb-4">
                          <i class="fas fa-info-circle me-2"></i> Your recently uploaded images will appear here.
                      </div>
                      <div class="my-5 py-4">
                          <i class="fas fa-image fa-5x text-muted mb-4"></i>
                          <p class="text-muted fs-5">No recent images found.</p>
                          <p class="text-muted fs-6">Upload an image to get started!</p>
                      </div>
                  </div>
              </div>
          `
    }
  }
}

// Modal functions
function showImageModal(imageId) {
  const recentImages = JSON.parse(sessionStorage.getItem("recentImages") || "[]")
  const image = recentImages.find((img) => img.id == imageId)

  if (image) {
    const modalElement = document.getElementById("imageModal")
    const modalImg = document.getElementById("modalImage")
    const caption = document.getElementById("modalCaption")
    const diseaseDetailsDiv = document.getElementById("diseaseDetails")

    if (modalImg && caption && diseaseDetailsDiv) {
      modalImg.src = image.src
      caption.innerHTML = `Uploaded: ${new Date(image.timestamp).toLocaleString()}`

      const details = image.diseaseDetails
      const severityColor = getSeverityColor(details.severity)
      const cleanPredictedName = getDisplayDiseaseName(details.predicted_class_name) // Use the helper here too

      diseaseDetailsDiv.innerHTML = `
                <h4 class="text-success mb-3">Prediction Details</h4>
                <p><strong>Predicted Class:</strong> ${cleanPredictedName}</p>
                <p><strong>Confidence:</strong> ${details.confidence}%</p>
                <p><strong>Crop:</strong> ${details.crop}</p>
                <p><strong>Disease:</strong> ${details.disease}</p>
                <p><strong>Severity:</strong> <span style="color: ${severityColor}; font-weight: bold;">${details.severity}</span></p>
                <p><strong>Primary Affected Part:</strong> ${details.primary_affected}</p>
                <p><strong>Affected Parts:</strong>
                    <div class="affected-parts-tags mt-2">
                        ${details.affected_parts.map((part) => `<span class="badge bg-warning">${part}</span>`).join("")}
                    </div>
                </p>
                <h4 class="text-success mt-4 mb-3">Description & Symptoms</h4>
                <p><strong>Description:</strong> ${details.description}</p>
                <p><strong>Symptoms:</strong> ${details.symptoms}</p>
            `
      // Using Bootstrap's modal method to show
      const bsModal = window.bootstrap.Modal.getOrCreateInstance(modalElement)
      bsModal.show()
    }
  }
}

function getDiseaseBadgeClass(disease) {
  if (!disease) return "bg-secondary"
  disease = disease.toLowerCase()
  if (disease.includes("healthy")) return "bg-success"
  if (disease.includes("spot") || disease.includes("blight") || disease.includes("rust")) return "bg-warning text-dark"
  if (disease.includes("mildew") || disease.includes("mold") || disease.includes("mites")) return "bg-info text-dark"
  if (disease.includes("virus") || disease.includes("bacterial")) return "bg-danger"
  return "bg-secondary"
}

function getSeverityColor(severity) {
  const colors = {
    None: "#28a745", // Green
    Low: "#ffc107", // Yellow
    Moderate: "#fd7e14", // Orange
    High: "#dc3545", // Red
    "Very High": "#6f42c1", // Purple
  }
  return colors[severity] || "#6c757d" // Default gray
}

function closeModal(modalId) {
  const modalElement = document.getElementById(modalId)
  if (modalElement) {
    const bsModal = window.bootstrap.Modal.getOrCreateInstance(modalElement)
    bsModal.hide()
  }
}

// Initialize image upload functionality
function initializeImageUpload() {
  const imageInput = document.getElementById("crop_image")
  if (imageInput) {
    imageInput.addEventListener("change", (e) => {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          // Update preview
          const preview = document.getElementById("preview")
          const previewImg = document.getElementById("previewImg")
          if (preview && previewImg) {
            previewImg.src = e.target.result
            preview.style.display = "block"
          }
        }
        reader.readAsDataURL(file)
      }
    })
  }
}

// Fixed form submission handler
function initializeFormSubmission() {
  const cropForm = document.getElementById("cropForm")
  if (cropForm) {
    cropForm.addEventListener("submit", function (e) {
      e.preventDefault()

      const formData = new FormData(this)
      const resultMessageDiv = document.getElementById("result-message")
      const predictionResultsDiv = document.getElementById("prediction-results")
      const predictionCardContent = document.getElementById("prediction-card-content")

      // Show loading message
      resultMessageDiv.innerHTML =
        '<div class="alert alert-info loading"><i class="fas fa-spinner fa-spin me-2"></i> Analyzing image...</div>'
      resultMessageDiv.style.display = "block"
      predictionResultsDiv.style.display = "none" // Hide previous results

      fetch(window.location.href, {
        // POST to the same URL
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          resultMessageDiv.style.display = "none" // Hide loading message

          if (data.success) {
            // Add to recent images
            const diseaseInfo = data.disease_info
            const diseaseDetailsToStore = {
              ...diseaseInfo, // Copy all properties from diseaseInfo
              predicted_class_name: data.predicted_class_name, // Explicitly add the full predicted class name
            }
            addToRecentImages(data.image_url, diseaseDetailsToStore)

            // Populate prediction results card
            const recommendations = data.recommendations

            const severityColor = getSeverityColor(diseaseInfo.severity)
            const cleanPredictedName = getDisplayDiseaseName(data.predicted_class_name)

            predictionCardContent.innerHTML = `
                        <div class="prediction-image-container mb-4">
                            <img src="${data.image_url}" alt="Uploaded Crop" class="img-fluid">
                        </div>
                        <div class="prediction-header-gradient">
                            <h3>${cleanPredictedName}</h3>
                            <p><strong>Confidence:</strong> ${data.confidence}%</p>
                        </div>

                        <div class="info-grid">
                            <div class="info-box" style="border-left-color: #007bff;">
                                <h4>🌾 Crop Type</h4>
                                <p>${diseaseInfo.crop}</p>
                            </div>
                            <div class="info-box" style="border-left-color: #28a745;">
                                <h4>🔬 Disease</h4>
                                <p>${diseaseInfo.disease}</p>
                            </div>
                            <div class="info-box" style="border-left-color: ${severityColor};">
                                <h4>⚠ Severity Level</h4>
                                <p style="color: ${severityColor};">${diseaseInfo.severity}</p>
                            </div>
                            <div class="info-box" style="border-left-color: #dc3545;">
                                <h4>🎯 Primary Affected Part</h4>
                                <p>${diseaseInfo.primary_affected}</p>
                            </div>
                        </div>

                        <div class="description-box">
                            <h4>🔍 All Affected Plant Parts</h4>
                            <div class="affected-parts-tags">
                                ${diseaseInfo.affected_parts.map((part) => `<span class="badge bg-warning">${part}</span>`).join("")}
                            </div>
                        </div>

                        <div class="description-box">
                            <h4>📋 Description</h4>
                            <p>${diseaseInfo.description}</p>
                        </div>

                        <div class="symptoms-box">
                            <h4>🔍 Symptoms to Look For</h4>
                            <p>${diseaseInfo.symptoms}</p>
                        </div>

                        <div class="confidence-bar-container">
                            <h4>📊 Prediction Confidence</h4>
                            <div class="progress">
                                <div class="progress-bar" role="progressbar" style="width: ${data.confidence}%;" aria-valuenow="${data.confidence}" aria-valuemin="0" aria-valuemax="100">${data.confidence}%</div>
                            </div>
                        </div>
                    `

            // Populate recommendations modal
            const modalDiseaseName = document.getElementById("modalDiseaseName")
            const recommendationsList = document.getElementById("recommendationsList")
            if (modalDiseaseName && recommendationsList) {
              modalDiseaseName.textContent = cleanPredictedName
              recommendationsList.innerHTML = recommendations
                .map((rec) => `<li class="list-group-item">${rec}</li>`)
                .join("")
            }

            showSection("prediction-results") // Show the results section
          } else {
            resultMessageDiv.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-triangle me-2"></i> Error: ${data.error}</div>`
            resultMessageDiv.style.display = "block"
          }
        })
        .catch((error) => {
          resultMessageDiv.style.display = "none" // Hide loading message
          console.error("Error:", error)
          resultMessageDiv.innerHTML = `<div class="alert alert-danger"><i class="fas fa-times-circle me-2"></i> Error: ${error.message}</div>`
          resultMessageDiv.style.display = "block"
        })
    })
  }
}
