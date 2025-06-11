// frontend/static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const resumeForm = document.getElementById('resumeForm');
    const messageDiv = document.getElementById('message'); // Assuming this is your messageArea now
    const submitButton = resumeForm.querySelector('button[type="submit"]');

    // Function to display validation messages
    function showMessage(msg, type = 'error') {
        messageDiv.textContent = msg;
        messageDiv.className = 'message-area'; // Reset classes
        if (type === 'error') {
            messageDiv.classList.add('error-message');
        } else if (type === 'success') {
            messageDiv.classList.add('success-message');
        } else if (type === 'info') { // Add info-message for loading states etc.
            messageDiv.classList.add('info-message');
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

    // Client-side validation function
    function validateForm() {
        clearValidation(); // Clear previous messages and styles

        let isValid = true;

        // Required text/textarea fields based on 'required' attribute in HTML
        const requiredInputs = resumeForm.querySelectorAll('[required]');
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('invalid');
                isValid = false;
            }
        });

        // Specific email format validation
        const emailInput = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailInput && emailInput.value.trim() && !emailRegex.test(emailInput.value.trim())) {
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
            // Only validate. If valid, the form proceeds to the action specified in HTML.
            if (!validateForm()) {
                event.preventDefault(); // Stop form submission if validation fails
            }
        });

        // Add input event listeners for real-time validation feedback
        const formInputs = resumeForm.querySelectorAll('input, textarea');
        formInputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.classList.contains('invalid')) {
                    if (input.checkValidity()) {
                         input.classList.remove('invalid');
                    }
                    if (resumeForm.querySelectorAll('.invalid').length === 0) {
                        clearValidation();
                    }
                }
            });

            input.addEventListener('blur', () => {
                if (!input.checkValidity() && input.value.trim()) {
                    input.classList.add('invalid');
                } else if (!input.value.trim() && input.hasAttribute('required')) {
                     input.classList.add('invalid');
                } else {
                    input.classList.remove('invalid');
                }
                 if (resumeForm.querySelectorAll('.invalid').length === 0) {
                    clearValidation();
                }
            });
        });
    }
});