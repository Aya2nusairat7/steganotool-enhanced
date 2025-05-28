# Utils Documentation

This document provides detailed explanations of the utility functions used in SteganoTool.

## Table of Contents
- [Encryption and Decryption Functions](#encryption-and-decryption-functions)
- [Compression Functions](#compression-functions)
- [Image Steganography Functions](#image-steganography-functions)
- [Audio Steganography Functions](#audio-steganography-functions)
- [QR Code Functions](#qr-code-functions)
- [Utility Functions](#utility-functions)

## Encryption and Decryption Functions

### `derive_key(password, salt=None)`

Derives a 32-byte key from a password using PBKDF2 with SHA-256.

**Parameters:**
- `password` (str): The password to derive the key from
- `salt` (bytes, optional): Salt used in key derivation. If None, a random 16-byte salt is generated

**Returns:**
- Tuple containing (key, salt)

**Process:**
1. If no salt is provided, generates a random 16-byte salt
2. Uses PBKDF2-HMAC with SHA-256 algorithm
3. Performs 100,000 iterations for security
4. Produces a 32-byte (256-bit) key suitable for AES-256

### `encrypt_message(message, password)`

Encrypts a message using AES-256-CBC with the provided password.

**Parameters:**
- `message` (str or bytes): The message to encrypt
- `password` (str): The password to use for encryption

**Returns:**
- bytes: Salt + IV + Compression Marker + Ciphertext

**Process:**
1. Attempts to compress the message using zlib to minimize size
2. Checks if compression actually reduced the size
3. Derives a key from the password
4. Generates a random initialization vector (IV)
5. Adds a compression marker byte (0x00 if compressed, 0xFF if not)
6. Creates an AES cipher in CBC mode with the key and IV
7. Encrypts the message with padding
8. Returns concatenated salt + IV + compression marker + ciphertext

### `decrypt_message(encrypted_data, password)`

Decrypts a message that was encrypted using AES-256-CBC.

**Parameters:**
- `encrypted_data` (bytes): The data to decrypt (salt + IV + compression marker + ciphertext)
- `password` (str): The password to use for decryption

**Returns:**
- str: The decrypted message

**Process:**
1. Extracts salt (first 16 bytes)
2. Extracts IV (next 16 bytes)
3. Extracts compression marker (next 1 byte)
4. Extracts ciphertext (remainder)
5. Derives the key using the password and extracted salt
6. Creates an AES cipher in CBC mode with the key and IV
7. Decrypts the ciphertext and removes padding
8. If compression marker indicates the data was compressed (not 0xFF), decompresses the data
9. Otherwise, uses the decrypted data directly
10. Returns the decoded message

## Compression Functions

### `compress_data(data)`

Compresses data using zlib with maximum compression level, but only if it actually reduces size.

**Parameters:**
- `data` (str or bytes): Data to compress

**Returns:**
- bytes: Compressed data, or original data with marker byte if compression would increase size

**Process:**
1. Encodes the data to UTF-8 if it's a string
2. Attempts to compress the data using zlib with maximum compression level (9)
3. Compares the size of the compressed data with the original data
4. If compression reduces the size, returns the compressed data
5. If compression would increase the size, returns the original data with a 0xFF marker byte

### `decompress_data(compressed_data)`

Decompresses data that was compressed using zlib, or returns original data if not compressed.

**Parameters:**
- `compressed_data` (bytes): Compressed data to decompress

**Returns:**
- bytes: Decompressed data

**Process:**
1. Checks if the data is marked as uncompressed (first byte is 0xFF)
2. If marked as uncompressed, returns the original data (without the marker byte)
3. Otherwise, decompresses the data using zlib
4. Returns the decompressed data

## Image Steganography Functions

### `hide_data_in_image(input_path, output_path, data)`

Hides binary data inside an image using LSB (Least Significant Bit) steganography.

**Parameters:**
- `input_path` (str): Path to the input image
- `output_path` (str): Path to save the output image
- `data` (bytes): Binary data to hide

**Returns:**
- str: Path to the output image

**Process:**
1. Converts binary data to a string of bits
2. Adds a null byte terminator
3. Opens the input image and converts to RGB if needed
4. Checks if the image is large enough to hide the data
5. Converts the image to a NumPy array for manipulation
6. Embeds each bit of data in the least significant bit of each pixel channel value
7. Reshapes and saves the modified image
8. Performs verification to ensure data was embedded correctly

### `extract_data_from_image(image_path)`

Extracts hidden data from an image using LSB steganography.

**Parameters:**
- `image_path` (str): Path to the image containing hidden data

**Returns:**
- bytes: Extracted binary data

**Process:**
1. Opens the image and converts to RGB if needed
2. Converts the image to a NumPy array
3. Extracts the least significant bit from each pixel channel value
4. Converts the bits into bytes
5. Stops when it encounters the null byte terminator
6. Returns the extracted binary data

### `convert_and_hide_in_image(input_path, output_path, data)`

Converts an image to PNG format and hides data using LSB steganography.

**Parameters:**
- `input_path` (str): Path to the input image
- `output_path` (str): Path to save the output image
- `data` (bytes): Binary data to hide

**Returns:**
- str: Path to the output image

## Audio Steganography Functions

### `hide_data_in_audio(audio_path, output_path, data)`

Hides binary data inside a WAV audio file.

**Parameters:**
- `audio_path` (str): Path to the input WAV file
- `output_path` (str): Path to save the modified WAV file
- `data` (bytes): Binary data to hide

**Returns:**
- str: Path to the output WAV file

**Process:**
1. Opens the WAV file
2. Reads the audio frames
3. Converts binary data to a string of bits
4. Adds a null byte terminator
5. Modifies the least significant bit of each audio sample
6. Writes the modified samples to a new WAV file

### `extract_data_from_audio(audio_path)`

Extracts hidden data from a WAV audio file.

**Parameters:**
- `audio_path` (str): Path to the WAV file containing hidden data

**Returns:**
- bytes: Extracted binary data

**Process:**
1. Opens the WAV file
2. Reads the audio frames
3. Extracts the least significant bit from each audio sample
4. Converts the bits into bytes
5. Stops when it encounters the null byte terminator
6. Returns the extracted binary data

### `convert_audio_to_wav(audio_path)`

Converts an audio file to WAV format.

**Parameters:**
- `audio_path` (str): Path to the input audio file

**Returns:**
- str: Path to the converted WAV file

## QR Code Functions

### `generate_qr_code(data, output_path, error_correction, box_size, border)`

Generates a QR code containing the specified data.

**Parameters:**
- `data` (str): Data to encode in the QR code
- `output_path` (str): Path to save the generated QR code
- `error_correction` (int): Error correction level
- `box_size` (int): Size of each box in the QR code
- `border` (int): Border size around the QR code

**Returns:**
- str: Path to the generated QR code

### `hide_message_in_qr(message, password, output_path, background_image, style)`

Encrypts a message and generates a QR code containing it.

**Parameters:**
- `message` (str): Message to hide
- `password` (str): Password for encryption
- `output_path` (str): Path to save the QR code
- `background_image` (str, optional): Path to background image
- `style` (str): QR code style ("standard", "fancy", "embedded")

**Returns:**
- dict: Contains paths, password, and other information

### `extract_message_from_qr(qr_code_path, password)`

Extracts and decrypts a message from a QR code.

**Parameters:**
- `qr_code_path` (str): Path to the QR code image
- `password` (str, optional): Password for decryption

**Returns:**
- dict: Contains extracted message and information

## Utility Functions

### `generate_strong_password(length=16)`

Generates a strong random password.

**Parameters:**
- `length` (int): Length of the password to generate

**Returns:**
- str: Generated password

**Process:**
1. Includes uppercase and lowercase letters, digits, and special characters
2. Ensures at least one character from each category
3. Randomly shuffles all characters

### `find_or_download_ffmpeg()`

Finds ffmpeg on the system or downloads it if not present.

**Returns:**
- str: Path to the ffmpeg executable

### `save_password_to_file(password, output_path)`

Saves a password to a text file.

**Parameters:**
- `password` (str): Password to save
- `output_path` (str): Path to save the password file

**Returns:**
- str: Path to the saved password file 