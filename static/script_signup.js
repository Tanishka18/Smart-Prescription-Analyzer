// Password strength indicator
const passwordInput = document.getElementById('password');
const passwordStrength = document.getElementById('passwordStrength');

passwordInput.addEventListener('input', function() {
  const password = this.value;
  let strength = 0;
  
  // Check length
  if (password.length >= 8) {
    strength += 1;
  }
  
  // Check for numbers
  if (/\d/.test(password)) {
    strength += 1;
  }
  
  // Check for special characters
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    strength += 1;
  }
  
  // Check for uppercase and lowercase
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) {
    strength += 1;
  }
  
  // Update strength meter
  passwordStrength.className = 'password-strength-meter';
  if (password.length === 0) {
    passwordStrength.style.width = '0%';
  } else if (strength <= 2) {
    passwordStrength.classList.add('weak');
  } else if (strength === 3) {
    passwordStrength.classList.add('medium');
  } else {
    passwordStrength.classList.add('strong');
  }
});

// Form submission
document.getElementById('signupForm').addEventListener('submit', function(e) {
  e.preventDefault();
  
  // Validate password match
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  
  if (password !== confirmPassword) {
    alert('Passwords do not match!');
    return false;
  }
  
  // Here you would typically send data to your backend
  // For demo purposes, redirect to login page
  window.location.href = 'login.html';
});
