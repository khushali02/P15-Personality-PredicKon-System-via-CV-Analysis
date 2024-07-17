document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const errorMessage = document.getElementById('error-message');
    
    if (password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match.";
    } else {
        errorMessage.textContent = "";
        // Proceed with form submission or further processing
        alert("Account created successfully!");
    }
});
