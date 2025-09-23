// metrics.js - handles the toggle for metrics view (per message/per 100 words)

document.addEventListener('DOMContentLoaded', function() {
    const toggleSwitch = document.getElementById('toggle-metric-view');
    const perMsg = document.getElementById('metrics-per-message');
    const per100 = document.getElementById('metrics-per-100words');
    const labelLeft = document.getElementById('toggle-label-left');
    const labelRight = document.getElementById('toggle-label-right');
    // Use localStorage to persist toggle state
    function updateToggleUI() {
      if (!toggleSwitch.checked) {
        perMsg.style.display = '';
        per100.style.display = 'none';
        labelLeft.style.color = '#25D366';
        labelRight.style.color = '#888';
        localStorage.setItem('metricsToggle', 'perMessage');
      } else {
        perMsg.style.display = 'none';
        per100.style.display = '';
        labelLeft.style.color = '#888';
        labelRight.style.color = '#25D366';
        localStorage.setItem('metricsToggle', 'per100');
      }
    }
    // On load, restore toggle state
    const savedToggle = localStorage.getItem('metricsToggle');
    if (savedToggle === 'per100') {
      toggleSwitch.checked = true;
    } else {
      toggleSwitch.checked = false;
    }
    updateToggleUI();
    toggleSwitch.addEventListener('change', updateToggleUI);
});
