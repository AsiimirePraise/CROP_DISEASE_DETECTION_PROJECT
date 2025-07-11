 // Navigation function
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Remove active class from all nav links
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            // Show selected section
            document.getElementById(sectionId).style.display = 'block';
            
            // Add active class to clicked nav link
            event.target.classList.add('active');
        }
        
        // Chart initialization
        document.addEventListener('DOMContentLoaded', function() {
            // Disease Trend Chart
            const trendCtx = document.getElementById('trendChart').getContext('2d');
            new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                    datasets: [{
                        label: 'Disease Detections',
                        data: [65, 59, 80, 81, 56, 55, 89],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
            
            // Disease Distribution Chart
            const diseaseCtx = document.getElementById('diseaseChart').getContext('2d');
            new Chart(diseaseCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Leaf Blight', 'Rust', 'Powdery Mildew', 'Bacterial Spot'],
                    datasets: [{
                        data: [35, 25, 20, 20],
                        backgroundColor: ['#e74c3c', '#f39c12', '#3498db', '#27ae60']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            
            // Regional Activity Chart
            const regionCtx = document.getElementById('regionChart').getContext('2d');
            new Chart(regionCtx, {
                type: 'bar',
                data: {
                    labels: ['Central', 'Eastern', 'Western', 'Northern'],
                    datasets: [{
                        label: 'Cases',
                        data: [45, 32, 28, 19],
                        backgroundColor: '#3498db'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
            
            // Monthly Chart
            const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
            new Chart(monthlyCtx, {
                type: 'bar',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Detections',
                        data: [120, 150, 180, 200, 160, 190],
                        backgroundColor: '#27ae60'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
            
            // User Activity Chart
            const userCtx = document.getElementById('userChart').getContext('2d');
            new Chart(userCtx, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Active Users',
                        data: [85, 92, 78, 89],
                        borderColor: '#f39c12',
                        backgroundColor: 'rgba(243, 156, 18, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        });
        
        // Diagnosis function
        function diagnoseCrop() {
            const fileInput = document.getElementById('imageUpload');
            const cropType = document.getElementById('cropType').value;
            const resultDiv = document.getElementById('diagnosisResult');
            
            if (!fileInput.files[0]) {
                alert('Please upload an image first');
                return;
            }
            
            if (!cropType) {
                alert('Please select a crop type');
                return;
            }
            
            // Simulate diagnosis process
            resultDiv.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Processing...</span>
                    </div>
                    <p class="mt-2">Analyzing image...</p>
                </div>
            `;
            
            setTimeout(() => {
                resultDiv.innerHTML = `
                    <h5><i class="fas fa-check-circle text-success"></i> Diagnosis Complete</h5>
                    <hr>
                    <p><strong>Disease:</strong> Leaf Blight</p>
                    <p><strong>Confidence:</strong> 94%</p>
                    <p><strong>Severity:</strong> <span class="disease-severity severity-high">High</span></p>
                    <p><strong>Recommendation:</strong> Apply fungicide treatment immediately</p>
                    <button class="btn btn-custom btn-sm mt-2">
                        <i class="fas fa-save"></i> Save Diagnosis
                    </button>
                `;
            }, 2000);
        }