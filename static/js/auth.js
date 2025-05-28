/**
 * Authentication JavaScript
 * Handles sign in, sign up functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Sign In Form
    const signInForm = document.getElementById('signInForm');
    if (signInForm) {
        signInForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const rememberMe = document.getElementById('rememberMe').checked;
            
            // Form validation
            if (!email || !password) {
                showError('Please enter both email and password');
                return;
            }
            
            // Call sign in API
            signIn(email, password, rememberMe);
        });
    }
    
    // Sign Up Form
    const signUpForm = document.getElementById('signUpForm');
    if (signUpForm) {
        // Password validation on keyup
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        
        if (passwordInput && confirmPasswordInput) {
            // Check password strength
            passwordInput.addEventListener('keyup', function() {
                validatePasswordStrength(this.value);
            });
            
            // Check password match
            confirmPasswordInput.addEventListener('keyup', function() {
                if (passwordInput.value !== this.value) {
                    this.setCustomValidity('Passwords do not match');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        signUpForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const fullName = document.getElementById('fullName').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const agreeTerms = document.getElementById('agreeTerms').checked;
            
            // Form validation
            if (!fullName || !email || !password) {
                showError('Please fill in all required fields');
                return;
            }
            
            if (password !== confirmPassword) {
                showError('Passwords do not match');
                return;
            }
            
            if (!agreeTerms) {
                showError('You must agree to the Terms of Service and Privacy Policy');
                return;
            }
            
            // Call sign up API
            signUp(fullName, email, password);
        });
    }
});

/**
 * Sign in function to authenticate user
 */
function signIn(email, password, rememberMe) {
    showLoading();
    
    // Get registered users from localStorage
    let registeredUsers = JSON.parse(localStorage.getItem('registered_users') || '[]');
    
    // Check if the user exists in the registered users
    let foundUser = registeredUsers.find(user => user.email === email);
    
    // Check the demo user credentials as well
    let isDemoUser = (email === 'demo@example.com' && password === 'Password123!');
    
    setTimeout(() => {
        if (foundUser && foundUser.password === password) {
            // Success - registered user login
            localStorage.setItem('auth_token', foundUser.token || 'user_token_12345');
            localStorage.setItem('user_name', foundUser.fullName);
            if (rememberMe) {
                localStorage.setItem('remember_auth', 'true');
            }
            
            // Redirect to original destination or home
            redirectAfterLogin();
        } else if (isDemoUser) {
            // Success - demo user login
            localStorage.setItem('auth_token', 'demo_token_12345');
            localStorage.setItem('user_name', 'Demo User');
            if (rememberMe) {
                localStorage.setItem('remember_auth', 'true');
            }
            
            // Redirect to original destination or home
            redirectAfterLogin();
        } else {
            // Error
            hideLoading();
            if (foundUser) {
                showError('Invalid password');
            } else {
                showError('Email not registered or invalid credentials');
            }
        }
    }, 1000);
}

/**
 * Sign up function to register new user
 */
function signUp(fullName, email, password) {
    showLoading();
    
    // Get existing registered users or initialize empty array
    let registeredUsers = JSON.parse(localStorage.getItem('registered_users') || '[]');
    
    // Check if email already exists
    let existingUser = registeredUsers.find(user => user.email === email);
    
    setTimeout(() => {
        if (email === 'admin@example.com' || existingUser) {
            // Error - email already registered
            hideLoading();
            showError('Email already registered');
        } else {
            // Generate a token
            const token = generateToken(email);
            
            // Create new user object
            const newUser = {
                email: email,
                password: password,
                fullName: fullName,
                token: token,
                registrationDate: new Date().toISOString()
            };
            
            // Add to registered users
            registeredUsers.push(newUser);
            
            // Save to localStorage
            localStorage.setItem('registered_users', JSON.stringify(registeredUsers));
            
            // Store current user info
            localStorage.setItem('auth_token', token);
            localStorage.setItem('user_name', fullName);
            
            // Redirect to original destination or home
            redirectAfterLogin();
        }
    }, 1000);
}

/**
 * Generate a simple token for authentication
 */
function generateToken(email) {
    const timestamp = new Date().getTime();
    const random = Math.floor(Math.random() * 1000000);
    return btoa(`${email}:${timestamp}:${random}`);
}

/**
 * Validate password strength
 */
function validatePasswordStrength(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    const passwordInput = document.getElementById('password');
    
    if (password.length < minLength) {
        passwordInput.setCustomValidity('Password must be at least 8 characters long');
    } else if (!hasUpperCase) {
        passwordInput.setCustomValidity('Password must contain at least one uppercase letter');
    } else if (!hasLowerCase) {
        passwordInput.setCustomValidity('Password must contain at least one lowercase letter');
    } else if (!hasNumbers) {
        passwordInput.setCustomValidity('Password must contain at least one number');
    } else if (!hasSpecialChar) {
        passwordInput.setCustomValidity('Password must contain at least one special character');
    } else {
        passwordInput.setCustomValidity('');
    }
}

/**
 * Show error message
 */
function showError(message) {
    // Create error alert
    const errorAlert = document.createElement('div');
    errorAlert.className = 'alert alert-danger mt-3';
    errorAlert.role = 'alert';
    errorAlert.innerHTML = `
        <strong>Error:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Find the form to append the error to
    const form = document.querySelector('.modern-form');
    if (form) {
        // Add the error alert before the form
        form.parentNode.insertBefore(errorAlert, form);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            errorAlert.remove();
        }, 5000);
    }
}

/**
 * Show loading overlay
 */
function showLoading() {
    // Create loading overlay
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.id = 'authLoadingOverlay';
    loadingOverlay.innerHTML = `
        <div class="loading-content">
            <div class="loading">
                <div></div>
                <div></div>
                <div></div>
            </div>
            <h3 class="loading-title">Processing</h3>
            <p class="loading-subtitle">Please wait...</p>
        </div>
    `;
    
    // Add to body
    document.body.appendChild(loadingOverlay);
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const loadingOverlay = document.getElementById('authLoadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.remove();
    }
}

/**
 * Redirect to saved URL after login or to home page
 */
function redirectAfterLogin() {
    // Get the redirect URL if any
    const redirectUrl = localStorage.getItem('redirect_after_login');
    
    // Clear the redirect URL from storage
    localStorage.removeItem('redirect_after_login');
    
    // Redirect to the saved URL or home page
    if (redirectUrl) {
        window.location.href = redirectUrl;
    } else {
        window.location.href = '/';
    }
} 