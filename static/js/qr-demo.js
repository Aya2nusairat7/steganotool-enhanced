/**
 * QR Code Steganography - Demo Script
 * 
 * This script demonstrates how to use the QR code steganography API endpoints
 * from a JavaScript client.
 */

// Generate a standard QR code
function generateQrCode(data, callback) {
    const formData = new FormData();
    formData.append('data', data);
    
    // Optional parameters
    formData.append('error_correction', 'H'); // L, M, Q, H (default is H)
    formData.append('box_size', '10'); // Size of each box in pixels
    formData.append('border', '4'); // Border size
    
    fetch('/api/generate-qr', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Get download URL
            const downloadUrl = data.download_url;
            callback(null, downloadUrl);
        } else {
            callback(new Error(data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        callback(error);
    });
}

// Encrypt a message and hide it in a QR code
function encryptMessageToQr(message, password, style, backgroundFile, callback) {
    const formData = new FormData();
    formData.append('message', message);
    
    // Password handling
    if (password) {
        formData.append('password', password);
    } else {
        formData.append('auto_generate', 'true');
    }
    
    // QR style
    if (style) {
        formData.append('style', style); // "standard", "fancy", or "embedded"
    }
    
    // Background image
    if (backgroundFile) {
        formData.append('background', backgroundFile);
    }
    
    fetch('/api/encrypt-qr', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const result = {
                downloadUrl: data.download_url,
                password: data.auto_generated_password || password,
                style: data.style,
                fileSize: data.file_size,
                messageLength: data.message_length
            };
            callback(null, result);
        } else {
            callback(new Error(data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        callback(error);
    });
}

// Decrypt a message from a QR code
function decryptQrCode(qrCodeFile, password, callback) {
    const formData = new FormData();
    formData.append('file', qrCodeFile);
    
    // Password is optional - will be extracted from QR if embedded
    if (password) {
        formData.append('password', password);
    }
    
    fetch('/api/decrypt-qr', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' || data.status === 'warning') {
            const result = {
                message: data.message,
                messageLength: data.message_length,
                passwordFound: data.password_found
            };
            callback(null, result);
        } else {
            callback(new Error(data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        callback(error);
    });
}

// Sample usage
document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners for QR code related buttons
    const generateQrButton = document.getElementById('generate-qr-button');
    if (generateQrButton) {
        generateQrButton.addEventListener('click', function() {
            const qrData = document.getElementById('qr-data').value;
            generateQrCode(qrData, function(err, downloadUrl) {
                if (err) {
                    displayError(err.message);
                    return;
                }
                
                displaySuccess(`QR code generated! <a href="${downloadUrl}" target="_blank">Download</a>`);
                document.getElementById('qr-preview').src = downloadUrl;
            });
        });
    }
    
    const encryptQrButton = document.getElementById('encrypt-qr-button');
    if (encryptQrButton) {
        encryptQrButton.addEventListener('click', function() {
            const message = document.getElementById('secret-message').value;
            const password = document.getElementById('encryption-password').value;
            const style = document.getElementById('qr-style').value;
            const backgroundFileInput = document.getElementById('background-image');
            
            let backgroundFile = null;
            if (backgroundFileInput && backgroundFileInput.files.length > 0) {
                backgroundFile = backgroundFileInput.files[0];
            }
            
            encryptMessageToQr(message, password, style, backgroundFile, function(err, result) {
                if (err) {
                    displayError(err.message);
                    return;
                }
                
                displaySuccess(`Message encrypted in QR code! <a href="${result.downloadUrl}" target="_blank">Download</a>`);
                document.getElementById('qr-preview').src = result.downloadUrl;
                document.getElementById('generated-password').textContent = result.password;
            });
        });
    }
    
    const decryptQrButton = document.getElementById('decrypt-qr-button');
    if (decryptQrButton) {
        decryptQrButton.addEventListener('click', function() {
            const qrFileInput = document.getElementById('qr-file');
            if (!qrFileInput || qrFileInput.files.length === 0) {
                displayError('Please select a QR code image file.');
                return;
            }
            
            const qrFile = qrFileInput.files[0];
            const password = document.getElementById('decryption-password').value;
            
            decryptQrCode(qrFile, password, function(err, result) {
                if (err) {
                    displayError(err.message);
                    return;
                }
                
                document.getElementById('decrypted-message').textContent = result.message;
                displaySuccess('Message decrypted successfully!');
                
                if (result.passwordFound) {
                    displayInfo('Password was automatically extracted from the QR code.');
                }
            });
        });
    }
});

// Helper functions for UI feedback
function displaySuccess(message) {
    const statusArea = document.getElementById('status-area');
    if (statusArea) {
        statusArea.innerHTML = `<div class="alert alert-success">${message}</div>`;
    }
}

function displayError(message) {
    const statusArea = document.getElementById('status-area');
    if (statusArea) {
        statusArea.innerHTML = `<div class="alert alert-danger">${message}</div>`;
    }
}

function displayInfo(message) {
    const statusArea = document.getElementById('status-area');
    if (statusArea) {
        statusArea.innerHTML += `<div class="alert alert-info">${message}</div>`;
    }
} 