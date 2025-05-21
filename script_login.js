// Simple login form handling
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Here you would normally handle authentication
    // For demo purposes, we'll simply redirect back to the main page
    window.location.href = 'index.html';
});
