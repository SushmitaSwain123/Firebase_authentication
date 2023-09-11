document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get user-entered values
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Send the registration data to the server (Django view)
    fetch('/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'), // Get CSRF token
        },
        body: `username=${encodeURIComponent(username)}&email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    })
    .then(response => {
        if (response.ok) {
            // Registration was successful, you can redirect the user to the profile page or login page.
            window.location.href = '/profile/';
        } else {
            // Handle registration errors (e.g., duplicate username or email)
            console.error('Registration failed.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the expected format
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
