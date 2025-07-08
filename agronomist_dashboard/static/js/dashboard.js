document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle functionality
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
    
    // Treatment recommendation actions
    const treatmentButtons = document.querySelectorAll('.treatment-actions .btn');
    treatmentButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.classList.contains('btn-success') ? 'approve' : 'reject';
            const treatmentItem = this.closest('.treatment-item');
            
            // Here you would typically make an AJAX call to update the treatment status
            console.log(`${action} treatment for:`, treatmentItem.querySelector('h4').textContent);
            
            // For demo purposes, just show an alert
            alert(`Treatment ${action}d successfully!`);
            
            // Remove the item from the list
            treatmentItem.remove();
        });
    });
    
    // Auto-refresh sensor data every 30 seconds
    function refreshSensorData() {
        const sensorCards = document.querySelectorAll('.sensor-card');
        sensorCards.forEach(card => {
            const valueElement = card.querySelector('.sensor-value');
            if (valueElement) {
                // Simulate slight variations in sensor readings
                const currentValue = parseFloat(valueElement.textContent);
                const variation = (Math.random() - 0.5) * 2; // ±1 unit variation
                const newValue = (currentValue + variation).toFixed(1);
                valueElement.textContent = newValue + valueElement.textContent.slice(-2); // Keep the unit
            }
        });
    }
    
    // Refresh sensor data every 30 seconds
    setInterval(refreshSensorData, 30000);
    
    // Animate progress bars on page load
    function animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }
    
    // Run animations
    animateProgressBars();
});
