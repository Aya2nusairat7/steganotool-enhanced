# API Documentation

This document provides detailed explanations of the API endpoints in SteganoTool.

## Table of Contents
- [Overview](#overview)
- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [Encryption Endpoints](#encryption-endpoints)
  - [Decryption Endpoints](#decryption-endpoints)
  - [QR Code Endpoints](#qr-code-endpoints)
  - [File Management](#file-management)
- [Request & Response Formats](#request--response-formats)
- [Error Handling](#error-handling)

## Overview

The SteganoTool API is a RESTful web service built with Flask that provides steganography functionality. It allows for hiding encrypted messages in various media types including images, audio files, and QR codes.

The API handles:
- File uploads and downloads
- Encryption and decryption of messages
- Embedding messages in various media types
- Extracting hidden messages from media files
- QR code generation and processing

## API Endpoints

### Health Check

#### `GET /api/health`

Checks if the API is operational.

**Response:**
```json
{
  "status": "healthy"
}
```

### Encryption Endpoints

#### `POST /api/encrypt`

Encrypts a message and hides it in a media file (image or audio).

**Request Format (multipart/form-data):**
- `file`: The media file to hide data in
- `message`: The message to hide
- `password`: Password for encryption (optional if auto_generate is true)
- `auto_generate`: Boolean flag to auto-generate a password
- `media_type`: Type of media ("image" or "audio")

**Response:**
```json
{
  "status": "success",
  "original_filename": "original.jpg",
  "output_filename": "stego_original.png",
  "file_size": 123456,
  "encrypted_size": 2048,
  "message_length": 1024,
  "original_size": 1500,
  "compressed_size": 1200,
  "compression_ratio": 20.0,
  "auto_generated": true,
  "auto_generated_password": "password123",
  "download_url": "/api/download/stego_original.png",
  "media_type": "image",
  "encryption_method": "AES-256",
  "hiding_technique": "LSB Image Steganography"
}
```

**Process:**
1. Validates the uploaded file and form parameters
2. Saves the uploaded file temporarily
3. Generates a password if auto_generate is true
4. Encrypts the message using AES-256
5. Embeds the encrypted data and password in the file
6. Saves the output file
7. Returns metadata about the operation

### Decryption Endpoints

#### `POST /api/decrypt`

Extracts and decrypts a message from a media file.

**Request Format (multipart/form-data):**
- `file`: The media file containing hidden data
- `password`: Password for decryption (optional if embedded in the file)
- `media_type`: Type of media ("image", "audio", or "auto")

**Response:**
```json
{
  "status": "success",
  "message": "The extracted message",
  "message_length": 1024,
  "encrypted_size": 2048,
  "compression_ratio": 20.0,
  "method_used": "AES-256",
  "media_type": "image",
  "original_filename": "stego_image.png"
}
```

**Process:**
1. Validates the uploaded file and form parameters
2. Determines the media type if set to "auto"
3. Extracts the hidden data from the file
4. Checks for an embedded password
5. Decrypts the data using the password
6. Returns the decrypted message and metadata

### QR Code Endpoints

#### `POST /api/generate-qr`

Generates a QR code containing the specified data.

**Request Format (application/json):**
```json
{
  "data": "Text to encode in QR",
  "error_correction": "H",
  "box_size": 10,
  "border": 4,
  "style": "standard"
}
```

**Response:**
```json
{
  "status": "success",
  "output_filename": "qr_code.png",
  "download_url": "/api/download/qr_code.png"
}
```

#### `POST /api/encrypt-qr`

Encrypts a message and generates a QR code containing it.

**Request Format (application/json):**
```json
{
  "message": "Secret message",
  "password": "password123",
  "auto_generate": false,
  "background_image": "base64_encoded_image",
  "style": "fancy"
}
```

**Response:**
```json
{
  "status": "success",
  "output_filename": "encrypted_qr.png",
  "download_url": "/api/download/encrypted_qr.png",
  "auto_generated": false,
  "password": "password123"
}
```

#### `POST /api/decrypt-qr`

Extracts and decrypts a message from a QR code.

**Request Format (multipart/form-data):**
- `file`: The QR code image
- `password`: Password for decryption (optional if embedded in QR)

**Response:**
```json
{
  "status": "success",
  "message": "The extracted message",
  "qr_type": "encrypted"
}
```

### File Management

#### `GET /api/download/<filename>`

Downloads a file from the server.

**Parameters:**
- `filename`: Name of the file to download

**Response:**
- File download response

#### `GET /api/capabilities`

Returns the capabilities of the current installation.

**Response:**
```json
{
  "image_steganography": true,
  "audio_steganography": true,
  "video_steganography": false,
  "qr_code_steganography": true,
  "encryption_methods": ["AES-256", "XOR"],
  "supported_image_formats": ["PNG", "JPG", "BMP"],
  "supported_audio_formats": ["WAV"],
  "max_file_size": 67108864
}
```

## Request & Response Formats

### File Upload Requests

File upload requests use `multipart/form-data` encoding to handle binary file data.

### JSON Requests

JSON requests use `application/json` content type and expect valid JSON in the request body.

### Responses

All responses are in JSON format with a `status` field indicating success or failure.

## Error Handling

The API uses standard HTTP status codes to indicate success or failure:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a JSON body with an `error` field describing the issue:

```json
{
  "error": "Detailed error message"
}
```

Common errors include:
- No file uploaded
- File too large
- Unsupported file format
- Invalid password
- No hidden data found
- Decryption failure 