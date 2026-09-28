// main.js - Client-side interactions for Hospital Management System

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // CONFIRMATION DIALOG FOR DESTRUCTIVE ACTIONS
    // -------------------------------------------------------------
    const confirmForms = document.querySelectorAll('form.confirm-action');
    confirmForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const message = form.getAttribute('data-confirm-message') || 'Are you sure you want to perform this action?';
            if (!window.confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // -------------------------------------------------------------
    // AUTO-DISMISS FLASH ALERTS AFTER 6 SECONDS
    // -------------------------------------------------------------
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                if (bsAlert) {
                    bsAlert.close();
                }
            } catch (err) {
                // Ignore if bootstrap is not fully initialized
            }
        }, 6000);
    });
});
