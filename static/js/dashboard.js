
// Dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts if Chart.js is loaded
    if (typeof Chart !== 'undefined') {
        initializeDashboardCharts();
    }
    
    // Auto-refresh alerts every 30 seconds
    setInterval(refreshAlerts, 30000);
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

function initializeDashboardCharts() {
    // Diagnosis trends chart
    const ctx = document.getElementById('diagnosisChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Diagnoses',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: 'rgb(82, 164, 71)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

function refreshAlerts() {
    fetch('/api/alerts/recent/')
        .then(response => response.json())
        .then(data => {
            updateAlertsDisplay(data);
        })
        .catch(error => console.log('Alert refresh failed:', error));
}

function updateAlertsDisplay(alerts) {
    const alertsContainer = document.getElementById('alerts-container');
    if (alertsContainer && alerts.length > 0) {
        // Update alerts display
        alertsContainer.innerHTML = alerts.map(alert => `
            <div class="alert alert-warning alert-dismissible fade show" role="alert">
                ${alert.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `).join('');
    }
}
