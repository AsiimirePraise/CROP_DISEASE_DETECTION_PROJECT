// Sidebar functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidebar
    initializeSidebar();
    
    // Add mobile toggle button
    addMobileToggle();
    
    // Handle menu item clicks
    handleMenuClicks();
});

function initializeSidebar() {
    // Set active menu item based on current page
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu-item');
    
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
    // Create mobile toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'sidebar-toggle';
    toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
    toggleBtn.onclick = toggleSidebar;
    document.body.appendChild(toggleBtn);
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
    
    // Close sidebar when clicking outside on mobile
    if (sidebar.classList.contains('active')) {
        document.addEventListener('click', closeSidebarOnOutsideClick);
    }
}

function closeSidebarOnOutsideClick(event) {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    
    if (!sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
        sidebar.classList.remove('active');
        document.removeEventListener('click', closeSidebarOnOutsideClick);
    }
}

function handleMenuClicks() {
    const menuItems = document.querySelectorAll('.menu-item:not(.logout)');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Don't prevent default for logout link
            if (!this.classList.contains('logout')) {
                e.preventDefault();
                
                // Remove active class from all items
                menuItems.forEach(i => i.classList.remove('active'));
                
                // Add active class to clicked item
                this.classList.add('active');
                
                // Close sidebar on mobile after selection
                if (window.innerWidth <= 768) {
                    document.getElementById('sidebar').classList.remove('active');
                }
            }
        });
    });
}

// Show Common Diseases section
function showCommonDiseases() {
    hideAllSections();
    showSection('common-diseases');
    
    const mainContent = document.querySelector('.main-content .container');
    
    // Create common diseases content
    const diseasesContent = `
        <div id="common-diseases" class="content-section active">
            <h3><i class="fas fa-bug"></i> Common Crop Diseases</h3>
            
            <div class="disease-card">
                <h5>Leaf Spot</h5>
                <p><strong>Symptoms:</strong> Small, dark spots on leaves that may have yellow halos</p>
                <p><strong>Causes:</strong> Fungal infection, often due to high humidity</p>
                <p><strong>Treatment:</strong> Remove infected leaves, apply fungicide, improve air circulation</p>
            </div>
            
            <div class="disease-card">
                <h5>Powdery Mildew</h5>
                <p><strong>Symptoms:</strong> White, powdery coating on leaves and stems</p>
                <p><strong>Causes:</strong> Fungal infection in warm, humid conditions</p>
                <p><strong>Treatment:</strong> Neem oil, baking soda spray, ensure good air circulation</p>
            </div>
            
            <div class="disease-card">
                <h5>Blight</h5>
                <p><strong>Symptoms:</strong> Large brown or black patches on leaves, stems, or fruits</p>
                <p><strong>Causes:</strong> Bacterial or fungal infection</p>
                <p><strong>Treatment:</strong> Remove infected parts, copper-based fungicides, crop rotation</p>
            </div>
            
            <div class="disease-card">
                <h5>Root Rot</h5>
                <p><strong>Symptoms:</strong> Yellowing leaves, wilting, stunted growth</p>
                <p><strong>Causes:</strong> Overwatering, poor drainage, fungal infection</p>
                <p><strong>Treatment:</strong> Improve drainage, reduce watering, fungicide treatment</p>
            </div>
            
            <div class="disease-card">
                <h5>Aphid Infestation</h5>
                <p><strong>Symptoms:</strong> Small green/black insects on leaves, sticky honeydew</p>
                <p><strong>Causes:</strong> Pest infestation</p>
                <p><strong>Treatment:</strong> Insecticidal soap, neem oil, beneficial insects</p>
            </div>
            
            <div class="disease-card">
                <h5>Mosaic Virus</h5>
                <p><strong>Symptoms:</strong> Mottled yellow and green patterns on leaves</p>
                <p><strong>Causes:</strong> Viral infection spread by insects</p>
                <p><strong>Treatment:</strong> Remove infected plants, control insect vectors</p>
            </div>
        </div>
    `;
    
    mainContent.innerHTML = diseasesContent;
}

// Show Recent Pictures section
function showRecentPictures() {
    hideAllSections();
    showSection('recent-pictures');
    
    const mainContent = document.querySelector('.main-content .container');
    
    // Create recent pictures content
    const recentContent = `
        <div id="recent-pictures" class="content-section active">
            <h3><i class="fas fa-images"></i> Recent Pictures</h3>
            
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> 
                Your recently uploaded images will appear here. Click on any image to view details.
            </div>
            
            <div class="image-grid">
                <div class="text-center p-4" style="grid-column: 1 / -1;">
                    <i class="fas fa-image fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No recent images found.</p>
                    <p class="text-muted">Upload an image to get started!</p>
                </div>
            </div>
        </div>
    `;
    
    mainContent.innerHTML = recentContent;
}

// Show upload section (original form)
function showUploadSection() {
    hideAllSections();
    location.reload(); // Reload to show original form
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

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.remove('active');
    }
});

// Add click handler for upload menu item
document.addEventListener('DOMContentLoaded', function() {
    const uploadMenuItem = document.querySelector('.menu-item:first-child .menu-link');
    if (uploadMenuItem) {
        uploadMenuItem.addEventListener('click', function(e) {
            e.preventDefault();
            showUploadSection();
        });
    }
});

// Enhanced image preview with recent images storage
function addToRecentImages(imageSrc) {
    let recentImages = JSON.parse(sessionStorage.getItem('recentImages') || '[]');
    
    const newImage = {
        src: imageSrc,
        timestamp: new Date().toISOString(),
        id: Date.now()
    };
    
    recentImages.unshift(newImage);
    
    // Keep only last 10 images
    if (recentImages.length > 10) {
        recentImages = recentImages.slice(0, 10);
    }
    
    sessionStorage.setItem('recentImages', JSON.stringify(recentImages));
}

// Update recent pictures display
function updateRecentPicturesDisplay() {
    const recentImages = JSON.parse(sessionStorage.getItem('recentImages') || '[]');
    const imageGrid = document.querySelector('.image-grid');
    
    if (imageGrid && recentImages.length > 0) {
        imageGrid.innerHTML = recentImages.map(img => `
            <div class="recent-image-container">
                <img src="${img.src}" alt="Recent Upload" class="recent-image img-fluid" 
                     style="max-width: 150px; max-height: 150px; object-fit: cover;">
                <small class="text-muted d-block text-center mt-1">
                    ${new Date(img.timestamp).toLocaleDateString()}
                </small>
            </div>
        `).join('');
    }
}

// Override the original image preview to add to recent images
document.addEventListener('DOMContentLoaded', function() {
    const originalInput = document.getElementById('crop_image');
    if (originalInput) {
        originalInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('preview');
                    const previewImg = document.getElementById('previewImg');
                    previewImg.src = e.target.result;
                    preview.style.display = 'block';
                    
                    // Add to recent images
                    addToRecentImages(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    }
});