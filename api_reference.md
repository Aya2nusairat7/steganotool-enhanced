# Steganography API Reference

This document provides detailed information about the Steganography API endpoints, request parameters, response structures, and example usage.

## Base URL

All API endpoints are relative to the base URL:

```
http://localhost:8080/api
```

## Authentication

The API does not currently require authentication.

## Content Types

- Request bodies should use `multipart/form-data` for file uploads
- Response bodies are in JSON format

## Message Processing

Messages undergo several transformations before being hidden:

1. **Compression**: Messages are compressed using zlib DEFLATE algorithm (level 9)
2. **Encryption**: Compressed messages are encrypted using AES-256 or XOR
3. **Steganography**: Encrypted data is embedded in the media file

## Common Response Structure

Most API responses follow this common structure:

```json
{
  "status": "success | error | warning",
  "message": "Optional message describing the result"
}
```

## Endpoints

### Health Check

Check the health status of the API.

**Endpoint:** `GET /health`

**Request Parameters:** None

**Response:**

```json
{
  "status": "healthy"
}
```

**Example:**

```bash
curl http://localhost:8080/api/health
```

### Get Capabilities

Retrieve the capabilities of the API.

**Endpoint:** `GET /capabilities`

**Request Parameters:** None

**Response:**

```json
{
  "image_steganography": true,
  "audio_steganography": true,
  "audio_conversion": true,
  "image_conversion": true
}
```

**Example:**

```bash
curl http://localhost:8080/api/capabilities
```

### Encrypt Message

Encrypt a message and hide it in a media file.

**Endpoint:** `POST /encrypt`

**Request Parameters (multipart/form-data):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | The media file to hide data in |
| message | String | Yes | The message to encrypt and hide |
| password | String | Conditional | The encryption password (required if auto_generate is not set) |
| auto_generate | Boolean | No | Whether to auto-generate a password (true/false) |
| media_type | String | No | Either "image" or "audio" (default: "image") |

**Response:**

```json
{
  "status": "success",
  "original_filename": "example.png",
  "output_filename": "stego_example.png",
  "file_size": 123456,
  "encrypted_size": 1024,
  "message_length": 255,
  "original_size": 255,
  "compressed_size": 128,
  "compression_ratio": 49.8,
  "auto_generated": true,
  "auto_generated_password": "A3b!9^xK_lP2@dR5",
  "download_url": "/api/download/stego_example.png",
  "media_type": "image"
}
```

| Field | Description |
|-------|-------------|
| original_size | Original size of the message in bytes |
| compressed_size | Size of the message after compression in bytes |
| compression_ratio | Percentage reduction in size due to compression |

**Example:**

```bash
# With a predefined password
curl -X POST http://localhost:8080/api/encrypt \
  -F "file=@/path/to/image.png" \
  -F "message=This is a secret message" \
  -F "password=SecretPassword123" \
  -F "media_type=image"

# With auto-generated password
curl -X POST http://localhost:8080/api/encrypt \
  -F "file=@/path/to/image.png" \
  -F "message=This is a secret message" \
  -F "auto_generate=true" \
  -F "media_type=image"
```

### Decrypt Message

Extract and decrypt a hidden message from a media file.

**Endpoint:** `POST /decrypt`

**Request Parameters (multipart/form-data):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | The media file containing hidden data |
| password | String | Conditional | The decryption password (required if not embedded in file) |
| media_type | String | No | Either "image" or "audio" (default: "image") |

**Response:**

```json
{
  "status": "success",
  "filename": "stego_example.png",
  "message": "This is the decrypted secret message",
  "message_length": 36,
  "password_found": true,
  "used_password": "A3b!9^xK_lP2@dR5"
}
```

**Example:**

```bash
# With password
curl -X POST http://localhost:8080/api/decrypt \
  -F "file=@/path/to/stego_image.png" \
  -F "password=SecretPassword123" \
  -F "media_type=image"

# For files with embedded password
curl -X POST http://localhost:8080/api/decrypt \
  -F "file=@/path/to/stego_image.png" \
  -F "media_type=image"
```

### Download File

Download a processed file from the server.

**Endpoint:** `GET /download/{filename}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filename | String | Yes | The name of the file to download |

**Response:** The file as an attachment

**Example:**

```bash
curl -O http://localhost:8080/api/download/stego_example.png
```

## Error Handling

The API returns appropriate HTTP status codes along with error messages in the response body:

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters or file format |
| 404 | Not Found - File or endpoint not found |
| 500 | Internal Server Error - Server-side error |

### Error Response Format

```json
{
  "status": "error",
  "message": "Description of the error"
}
```

### Common Error Messages

| Message | Description |
|---------|-------------|
| "No file part" | No file was provided in the request |
| "No selected file" | An empty file was provided |
| "No message provided" | No message was provided for encryption |
| "No password provided and auto-generate not enabled" | No password was provided and auto-generate is not enabled |
| "No password provided or found in the file" | No password was provided for decryption and none was found in the file |
| "Image steganography not supported in this build" | Image steganography functionality is not available |
| "Audio steganography not supported in this build" | Audio steganography functionality is not available |
| "No valid encrypted data found" | The file does not contain hidden data or the data is corrupt |

## Image Steganography Specifics

### Supported Input Formats

- PNG (Recommended)
- BMP
- GIF
- JPEG (Will be converted to PNG)

### Output Format

- PNG (Default for all image input types)
- BMP (If BMP is provided as input)
- GIF (If GIF is provided as input)

### Storage Capacity

The capacity depends on the image dimensions:

- Each pixel can store 3 bits (1 in each RGB channel)
- Total bits = Width × Height × 3
- Overhead: About 32 bytes for encryption metadata

## Audio Steganography Specifics

### Supported Input Formats

- WAV (Recommended)
- MP3 (Will be converted to WAV)
- OGG (Will be converted to WAV)
- FLAC (Will be converted to WAV)
- M4A (Will be converted to WAV)
- AAC (Will be converted to WAV)

### Output Format

- WAV (All audio outputs are in WAV format)

### Storage Capacity

The capacity depends on the audio file properties:

- Each sample can store 1 bit
- Total bits = Number of samples (depends on duration and sample rate)
- Overhead: About 32 bytes for encryption metadata

## Encryption Details

### Data Compression
- Algorithm: zlib (DEFLATE)
- Compression Level: Maximum (9)
- Applied before encryption to minimize data size
- Automatic decompression during decryption

### AES-256 Encryption (Default for messages ≥32 bytes)

- Mode: CBC (Cipher Block Chaining)
- Key Derivation: PBKDF2 with 100,000 iterations
- Salt: 16 bytes (random, included in encrypted data)
- IV: 16 bytes (random, included in encrypted data)
- Format: [salt (16 bytes)][IV (16 bytes)][encrypted data]

### XOR Encryption (For messages <32 bytes)

- Key: SHA-256 hash of the password
- Format: Simple XOR with the key

## Example Code

### Python

```python
import requests
import os

API_URL = "http://localhost:8080/api"

def check_health():
    """Check if the API is running"""
    response = requests.get(f"{API_URL}/health")
    return response.json()

def get_capabilities():
    """Get API capabilities"""
    response = requests.get(f"{API_URL}/capabilities")
    return response.json()

def encrypt_message(file_path, message, password=None, auto_generate=False, media_type="image"):
    """Encrypt and hide a message in a file"""
    # Validate inputs
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}
    
    if not message:
        return {"status": "error", "message": "No message provided"}
    
    if not password and not auto_generate:
        return {"status": "error", "message": "No password provided and auto-generate not enabled"}
    
    # Prepare the request
    url = f"{API_URL}/encrypt"
    files = {'file': open(file_path, 'rb')}
    data = {
        'message': message,
        'media_type': media_type
    }
    
    if auto_generate:
        data['auto_generate'] = 'true'
    else:
        data['password'] = password
    
    # Send the request
    response = requests.post(url, files=files, data=data)
    
    # Process the response
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            # Download the processed file
            download_url = f"{API_URL}/download/{result['output_filename']}"
            download_response = requests.get(download_url)
            
            # Save the file
            output_path = result['output_filename']
            with open(output_path, 'wb') as f:
                f.write(download_response.content)
            
            print(f"File saved as {output_path}")
            
            # If password was auto-generated, show it
            if result.get('auto_generated_password'):
                print(f"Auto-generated password: {result['auto_generated_password']}")
            
            return result
    
    # Handle errors
    try:
        return response.json()
    except:
        return {"status": "error", "message": f"Request failed with status code {response.status_code}"}

def decrypt_message(file_path, password=None, media_type="image"):
    """Extract and decrypt a message from a file"""
    # Validate inputs
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}
    
    # Prepare the request
    url = f"{API_URL}/decrypt"
    files = {'file': open(file_path, 'rb')}
    data = {'media_type': media_type}
    
    if password:
        data['password'] = password
    
    # Send the request
    response = requests.post(url, files=files, data=data)
    
    # Process the response
    if response.status_code == 200:
        return response.json()
    
    # Handle errors
    try:
        return response.json()
    except:
        return {"status": "error", "message": f"Request failed with status code {response.status_code}"}

# Example usage
if __name__ == "__main__":
    # Check API health
    health = check_health()
    print(f"API Health: {health}")
    
    # Get capabilities
    capabilities = get_capabilities()
    print(f"API Capabilities: {capabilities}")
    
    # Encrypt a message
    result = encrypt_message(
        "example.png", 
        "This is a secret message", 
        auto_generate=True
    )
    print(f"Encryption result: {result}")
    
    # Decrypt a message
    if result['status'] == 'success':
        decrypt_result = decrypt_message(
            result['output_filename']
        )
        print(f"Decryption result: {decrypt_result}")
        print(f"Decrypted message: {decrypt_result.get('message', 'No message found')}")
```

### JavaScript

```javascript
// Using Fetch API with async/await

const API_URL = 'http://localhost:8080/api';

// Check API health
async function checkHealth() {
  const response = await fetch(`${API_URL}/health`);
  return response.json();
}

// Get API capabilities
async function getCapabilities() {
  const response = await fetch(`${API_URL}/capabilities`);
  return response.json();
}

// Encrypt and hide a message
async function encryptMessage(file, message, password = null, autoGenerate = false, mediaType = 'image') {
  // Create FormData
  const formData = new FormData();
  formData.append('file', file);
  formData.append('message', message);
  formData.append('media_type', mediaType);
  
  if (autoGenerate) {
    formData.append('auto_generate', 'true');
  } else if (password) {
    formData.append('password', password);
  } else {
    throw new Error('No password provided and auto-generate not enabled');
  }
  
  // Send request
  const response = await fetch(`${API_URL}/encrypt`, {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  
  // Download the file if encryption was successful
  if (result.status === 'success') {
    const downloadResponse = await fetch(`${API_URL}/download/${result.output_filename}`);
    const blob = await downloadResponse.blob();
    
    // Create a download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = result.output_filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  }
  
  return result;
}

// Extract and decrypt a message
async function decryptMessage(file, password = null, mediaType = 'image') {
  // Create FormData
  const formData = new FormData();
  formData.append('file', file);
  formData.append('media_type', mediaType);
  
  if (password) {
    formData.append('password', password);
  }
  
  // Send request
  const response = await fetch(`${API_URL}/decrypt`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
}

// Example usage (in an async function context)
async function exampleUsage() {
  try {
    // Check health
    const health = await checkHealth();
    console.log('API Health:', health);
    
    // Get capabilities
    const capabilities = await getCapabilities();
    console.log('API Capabilities:', capabilities);
    
    // Get a file input from a form
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    // Encrypt a message
    const encryptResult = await encryptMessage(
      file,
      'This is a secret message',
      null,
      true // Auto-generate password
    );
    console.log('Encryption Result:', encryptResult);
    
    // Decrypt a message (would need to upload the downloaded file)
    // const decryptFile = ... (get uploaded stego file)
    // const decryptResult = await decryptMessage(decryptFile);
    // console.log('Decryption Result:', decryptResult);
  } catch (error) {
    console.error('API Error:', error);
  }
}
```

## Advanced API Usage

### Batch Processing

For batch processing, use a loop to process multiple files:

```python
import os
import requests

def batch_encrypt_directory(directory, message, password, media_type="image"):
    """Encrypt the same message into all files in a directory"""
    results = []
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip directories and non-supported files
        if os.path.isdir(file_path):
            continue
            
        # Determine media type based on extension if not specified
        if media_type == "auto":
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac']:
                file_media_type = "audio"
            elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                file_media_type = "image"
            else:
                print(f"Skipping unsupported file: {filename}")
                continue
        else:
            file_media_type = media_type
        
        # Process the file
        print(f"Processing {filename}...")
        result = encrypt_message(file_path, message, password, False, file_media_type)
        results.append({
            'filename': filename,
            'result': result
        })
    
    return results
```

## Data Compression Details

### Compression Algorithm

- **Algorithm**: zlib DEFLATE (RFC 1951)
- **Compression Level**: 9 (maximum compression)
- **Implementation**: Python's built-in zlib module

### Compression Effects

- **Text Data**: Typically achieves 30-70% reduction in size
- **Binary Data**: Compression efficiency varies based on content entropy
- **Already Compressed Data**: Minimal additional compression

### Decompression

- Decompression is automatically performed during the decryption process
- If decompression fails, an error message will be returned: "Decompression error: ..." 