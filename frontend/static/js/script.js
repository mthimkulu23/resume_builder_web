// frontend/static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const resumeForm = document.getElementById('resumeForm');
    const messageDiv = document.getElementById('message');

    // Function to display validation messages
    function showMessage(msg, type = 'error') {
        messageDiv.textContent = msg;
        messageDiv.className = 'message-area'; // Reset classes
        if (type === 'error') {
            messageDiv.classList.add('error-message');
        } else if (type === 'success') {
            messageDiv.classList.add('success-message');
        }
        messageDiv.style.display = 'block';
    }

    // Function to clear messages and validation styles
    function clearValidation() {
        messageDiv.style.display = 'none';
        const invalidInputs = resumeForm.querySelectorAll('.invalid');
        invalidInputs.forEach(input => {
            input.classList.remove('invalid');
        });
    }

    // Basic validation function
    function validateForm() {
        clearValidation(); // Clear previous messages and styles

        let isValid = true;

        // Required text/textarea fields
        const requiredFields = ['name', 'email', 'summary', 'skills', 'education', 'experience', 'reference'];
        requiredFields.forEach(fieldId => {
            const input = document.getElementById(fieldId);
            if (!input.value.trim()) {
                input.classList.add('invalid');
                isValid = false;
            }
        });

        // Email format validation
        const emailInput = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailInput && !emailRegex.test(emailInput.value.trim())) {
            emailInput.classList.add('invalid');
            isValid = false;
        }

        if (!isValid) {
            showMessage('Please fill in all required fields and ensure formats are correct.', 'error');
        }

        return isValid;
    }

    // Add event listener for form submission
    if (resumeForm) {
        resumeForm.addEventListener('submit', (event) => {
            if (!validateForm()) {
                event.preventDefault(); // Stop form submission if validation fails
            }
        });

        // Add input event listeners to clear validation on typing
        const formInputs = resumeForm.querySelectorAll('input, textarea');
        formInputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.classList.contains('invalid')) {
                    input.classList.remove('invalid');
                    // Optionally re-validate all or clear message if no more invalid fields
                    if (resumeForm.querySelectorAll('.invalid').length === 0) {
                        clearValidation();
                    }
                }
            });
        });
    }
});
