// Sidebar functionality - Fixed Version
document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidebar
    initializeSidebar();
    
    // Add mobile toggle button
    addMobileToggle();
    
    // Handle menu item clicks
    handleMenuClicks();
    
    // Initialize recent images display
    updateRecentPicturesDisplay();
    
    // Handle image upload and preview
    initializeImageUpload();
});

function initializeSidebar() {
    // Set active menu item - default to Upload Image
    const menuItems = document.querySelectorAll('.menu-item:not(.logout)');
    
    menuItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Default to Upload Image as active
    const uploadItem = document.querySelector('.menu-item:first-child');
    if (uploadItem) {
        uploadItem.classList.add('active');
    }
}

function addMobileToggle() {
    // Check if toggle button already exists
    if (document.querySelector('.sidebar-toggle')) {
        return;
    }
    
    // Create mobile toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'sidebar-toggle';
    toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
    toggleBtn.onclick = toggleSidebar;
    
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
    `;
    
    document.body.appendChild(toggleBtn);
    
    // Show/hide toggle button based on screen size
    handleToggleButtonVisibility();
    window.addEventListener('resize', handleToggleButtonVisibility);
}

function handleToggleButtonVisibility() {
    const toggleBtn = document.querySelector('.sidebar-toggle');
    if (toggleBtn) {
        if (window.innerWidth <= 768) {
            toggleBtn.style.display = 'block';
        } else {
            toggleBtn.style.display = 'none';
            // Close sidebar on desktop
            const sidebar = document.getElementById('sidebar');
            if (sidebar) {
                sidebar.classList.remove('active');
            }
        }
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
        
        // Close sidebar when clicking outside on mobile
        if (sidebar.classList.contains('active')) {
            setTimeout(() => {
                document.addEventListener('click', closeSidebarOnOutsideClick);
            }, 100);
        } else {
            document.removeEventListener('click', closeSidebarOnOutsideClick);
        }
    }
}

function closeSidebarOnOutsideClick(event) {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    
    if (sidebar && toggleBtn) {
        if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
            sidebar.classList.remove('active');
            document.removeEventListener('click', closeSidebarOnOutsideClick);
        }
    }
}

function handleMenuClicks() {
    const menuItems = document.querySelectorAll('.menu-item:not(.logout)');
    
    menuItems.forEach((item, index) => {
        const link = item.querySelector('.menu-link');
        if (link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all items
                menuItems.forEach(i => i.classList.remove('active'));
                
                // Add active class to clicked item
                item.classList.add('active');
                
                // Handle different menu actions
                switch(index) {
                    case 0:
                        showUploadSection();
                        break;
                    case 1:
                        showCommonDiseases();
                        break;
                    case 2:
                        showRecentPictures();
                        break;
                }
                
                // Close sidebar on mobile after selection
                if (window.innerWidth <= 768) {
                    const sidebar = document.getElementById('sidebar');
                    if (sidebar) {
                        sidebar.classList.remove('active');
                    }
                }
            });
        }
    });
}

// Show Upload Section (original form)
function showUploadSection() {
    hideAllSections();
    showSection('upload-section');
}

// Show Common Diseases section
function showCommonDiseases() {
    hideAllSections();
    showSection('common-diseases');
    
    // Load content dynamically
    const section = document.getElementById('common-diseases');
    if (section) {
        section.innerHTML = `
            <div class="card shadow">
                <div class="card-body">
                    <h3 class="card-title"><i class="fas fa-bug"></i> Common Crop Diseases</h3>
                    
                    <div class="disease-card mb-4 p-3 border rounded">
                        <h5 class="text-success">Leaf Spot</h5>
                        <p><strong>Symptoms:</strong> Small, dark spots on leaves that may have yellow halos</p>
                        <p><strong>Causes:</strong> Fungal infection, often due to high humidity</p>
                        <p><strong>Treatment:</strong> Remove infected leaves, apply fungicide, improve air circulation</p>
                    </div>
                    
                    <div class="disease-card mb-4 p-3 border rounded">
                        <h5 class="text-success">Powdery Mildew</h5>
                        <p><strong>Symptoms:</strong> White, powdery coating on leaves and stems</p>
                        <p><strong>Causes:</strong> Fungal infection in warm, humid conditions</p>
                        <p><strong>Treatment:</strong> Neem oil, baking soda spray, ensure good air circulation</p>
                    </div>
                    
                    <div class="disease-card mb-4 p-3 border rounded">
                        <h5 class="text-success">Blight</h5>
                        <p><strong>Symptoms:</strong> Large brown or black patches on leaves, stems, or fruits</p>
                        <p><strong>Causes:</strong> Bacterial or fungal infection</p>
                        <p><strong>Treatment:</strong> Remove infected parts, copper-based fungicides, crop rotation</p>
                    </div>
                    
                    <div class="disease-card mb-4 p-3 border rounded">
                        <h5 class="text-success">Root Rot</h5>
                        <p><strong>Symptoms:</strong> Yellowing leaves, wilting, stunted growth</p>
                        <p><strong>Causes:</strong> Overwatering, poor drainage, fungal infection</p>
                        <p><strong>Treatment:</strong> Improve drainage, reduce watering, fungicide treatment</p>
                    </div>
                    
                    <div class="disease-card mb-4 p-3 border rounded">
                        <h5 class="text-success">Aphid Infestation</h5>
                        <p><strong>Symptoms:</strong> Small green/black insects on leaves, sticky honeydew</p>
                        <p><strong>Causes:</strong> Pest infestation</p>
                        <p><strong>Treatment:</strong> Insecticidal soap, neem oil, beneficial insects</p>
                    </div>
                    
                    <div class="disease-card mb-4 p-3 border rounded">
                        <h5 class="text-success">Mosaic Virus</h5>
                        <p><strong>Symptoms:</strong> Mottled yellow and green patterns on leaves</p>
                        <p><strong>Causes:</strong> Viral infection spread by insects</p>
                        <p><strong>Treatment:</strong> Remove infected plants, control insect vectors</p>
                    </div>
                </div>
            </div>
        `;
    }
}

// Show Recent Pictures section
function showRecentPictures() {
    hideAllSections();
    showSection('recent-pictures');
    updateRecentPicturesDisplay();
}

// Helper functions
function hideAllSections() {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });
}

function showSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
        section.style.display = 'block';
    }
}

function resetForm() {
    // Reset file input
    const fileInput = document.getElementById('crop_image');
    if (fileInput) fileInput.value = '';
    
    // Hide preview image
    const preview = document.getElementById('preview');
    if (preview) preview.style.display = 'none';
    
    // Clear results display
    const resultDiv = document.getElementById('result');
    if (resultDiv) resultDiv.innerHTML = '';
    
    // Optional: Scroll back to upload section
    document.querySelector('.upload-section')?.scrollIntoView({ behavior: 'smooth' });
    
    // Optional: Focus back on file input for accessibility
    fileInput?.focus();
}

// Fixed addToRecentImages function - now accepts diseaseDetails as parameter
function addToRecentImages(imageSrc, diseaseDetails = null) {
    let recentImages = JSON.parse(sessionStorage.getItem('recentImages') || '[]');
    
    // Ensure diseaseDetails has required fields
    if (!diseaseDetails) {
        diseaseDetails = {
            disease: 'Unknown',
            confidence: 0,
            description: 'No diagnosis available',
            treatment: 'Consult an expert'
        };
    }

    const newImage = {
        src: imageSrc,
        timestamp: new Date().toISOString(),
        id: Date.now(),
        diseaseDetails: diseaseDetails
    };
    
    recentImages.unshift(newImage);
    
    // Keep only last 10 images
    if (recentImages.length > 10) {
        recentImages = recentImages.slice(0, 10);
    }
    
    sessionStorage.setItem('recentImages', JSON.stringify(recentImages));
    
    updateRecentPicturesDisplay();
}

function updateRecentPicturesDisplay() {
    console.log("Checking sessionStorage for recent images...");
    console.log(JSON.parse(sessionStorage.getItem('recentImages')));

    const recentImages = JSON.parse(sessionStorage.getItem('recentImages') || '[]');
    const recentPicturesSection = document.getElementById('recent-pictures');
    
    if (recentPicturesSection) {
        if (recentImages.length > 0) {
            recentPicturesSection.innerHTML = `
                <div class="card shadow">
                    <div class="card-body">
                        <h3 class="card-title"><i class="fas fa-images"></i> Recent Pictures</h3>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Click on any image to view details.
                        </div>
                        <div class="image-grid">
                            ${recentImages.map(img => `
                                <div class="recent-image-container" onclick="showImageModal('${img.id}')">
                                    <img src="${img.src}" alt="Recent Upload" class="img-fluid">
                                    <small class="text-muted d-block text-center mt-1">
                                        ${new Date(img.timestamp).toLocaleDateString()}
                                        ${img.diseaseDetails ? `<span class="badge ${getDiseaseBadgeClass(img.diseaseDetails.disease)}">${img.diseaseDetails.disease}</span>` : ''}
                                    </small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        } else {
            recentPicturesSection.innerHTML = `
                <div class="card shadow">
                    <div class="card-body text-center">
                        <h3 class="card-title"><i class="fas fa-images"></i> Recent Pictures</h3>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Your recently uploaded images will appear here.
                        </div>
                        <div class="my-5 py-4">
                            <i class="fas fa-image fa-4x text-muted mb-3"></i>
                            <p class="text-muted">No recent images found.</p>
                            <p class="text-muted">Upload an image to get started!</p>
                        </div>
                    </div>
                </div>
            `;
        }
    }
}

// Modal functions
function showImageModal(imageId) {
    const recentImages = JSON.parse(sessionStorage.getItem('recentImages') || '[]');
    const image = recentImages.find(img => img.id == imageId);
    
    if (image) {
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImage');
        const caption = document.getElementById('modalCaption');
        const diseaseDetails = document.getElementById('diseaseDetails');
        
        if (modal && modalImg && caption) {
            modal.style.display = "block";
            modalImg.src = image.src;
            caption.innerHTML = `Uploaded: ${new Date(image.timestamp).toLocaleString()}`;
            
            if (image.diseaseDetails && diseaseDetails) {
                diseaseDetails.innerHTML = `
                    <div class="disease-info mt-3 p-3 border rounded">
                        <h5>Diagnosis: <span class="${getDiseaseTextClass(image.diseaseDetails.disease)}">${image.diseaseDetails.disease}</span></h5>
                        <p><strong>Confidence:</strong> ${image.diseaseDetails.confidence}%</p>
                        <p><strong>Description:</strong> ${image.diseaseDetails.description}</p>
                        <p><strong>Treatment:</strong> ${image.diseaseDetails.treatment}</p>
                    </div>
                `;
                diseaseDetails.style.display = 'block';
            } else if (diseaseDetails) {
                diseaseDetails.style.display = 'none';
            }
        }
    }
}

function getDiseaseBadgeClass(disease) {
    if (!disease) return 'bg-secondary'; 
    disease = disease.toLowerCase();
    if (disease.includes('healthy')) return 'bg-success';
    if (disease.includes('spot') || disease.includes('blight')) return 'bg-warning text-dark';
    if (disease.includes('mildew') || disease.includes('mold')) return 'bg-info text-dark';
    if (disease.includes('virus') || disease.includes('bacterial')) return 'bg-danger';
    return 'bg-secondary';
}

// Helper function for disease text styling
function getDiseaseTextClass(disease) {
    if (!disease) return 'text-secondary';
    disease = disease.toLowerCase();
    if (disease.includes('healthy')) return 'text-success';
    if (disease.includes('spot') || disease.includes('blight')) return 'text-warning';
    if (disease.includes('mildew') || disease.includes('mold')) return 'text-info';
    if (disease.includes('virus') || disease.includes('bacterial')) return 'text-danger';
    return 'text-secondary';
}

// Fixed form submission handler
function initializeFormSubmission() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get the form data
            const formData = new FormData(this);
            
            // Submit via AJAX
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Store both image and disease details
                    addToRecentImages(data.image_url, {
                        disease: data.diagnosis || 'Unknown',
                        confidence: data.confidence || 0,
                        description: data.description || 'No diagnosis available',
                        treatment: data.treatment || 'Consult an expert'
                    });
                    
                    // Show success message
                    alert('Image uploaded and analyzed successfully!');
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during upload.');
            });
        });
    }
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = "none";
    }
}

// Initialize image upload functionality
function initializeImageUpload() {
    const imageInput = document.getElementById('crop_image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Update preview
                    const preview = document.getElementById('preview');
                    const previewImg = document.getElementById('previewImg');
                    if (preview && previewImg) {
                        previewImg.src = e.target.result;
                        preview.style.display = 'block';
                    }
                    
                  
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Initialize form submission
    initializeFormSubmission();
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('imageModal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

// Handle window resize for sidebar
window.addEventListener('resize', function() {
    handleToggleButtonVisibility();
});