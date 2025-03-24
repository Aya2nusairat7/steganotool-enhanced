# Encryption and Decryption Process Documentation

This document provides a detailed technical explanation of the complete encryption and decryption processes used in the steganography application.

## Table of Contents

1. [Overview](#overview)
2. [Complete Process Flow](#complete-process-flow)
3. [Compression](#compression)
4. [Encryption](#encryption)
5. [Steganography](#steganography)
6. [Decryption](#decryption)
7. [Technical Implementation](#technical-implementation)
8. [Security Considerations](#security-considerations)

## Overview

The steganography application uses a multi-layered approach to secure messages:

1. **Compression** - Reduces message size using zlib DEFLATE algorithm
2. **Encryption** - Secures the compressed data using AES-256 or XOR encryption
3. **Steganography** - Hides the encrypted data in media files using LSB (Least Significant Bit) technique
4. **Password Management** - Optionally embeds passwords within the carrier file

This layered approach provides both security (encryption) and privacy (steganography).

## Complete Process Flow

### Encryption Flow

```
┌───────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌───────────┐
│  Original │    │   Compress │    │  Encrypt   │    │ Hide in    │    │  Output   │
│  Message  │───►│   (zlib)   │───►│ (AES/XOR)  │───►│ Media File │───►│  File     │
└───────────┘    └────────────┘    └────────────┘    └────────────┘    └───────────┘
                                         ▲
                       ┌─────────────────┘
┌────────────┐         │
│ Password   │─────────┘
└────────────┘
```

### Decryption Flow

```
┌───────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌───────────┐
│  Stego    │    │  Extract   │    │  Decrypt   │    │ Decompress │    │ Original  │
│  File     │───►│  Hidden    │───►│ (AES/XOR)  │───►│   (zlib)   │───►│ Message   │
└───────────┘    │  Data      │    └────────────┘    └────────────┘    └───────────┘
                 └────────────┘          ▲
                                         │
┌────────────┐                           │
│ Password   │───────────────────────────┘
│(from file  │
│or provided)│
└────────────┘
```

## Compression

### Process

1. **Input**: Original message (string or binary data)
2. **Conversion**: If the message is a string, it's converted to bytes
3. **Compression**: zlib compression is applied with level 9 (maximum)
4. **Output**: Compressed binary data

### Technical Details

- **Algorithm**: zlib DEFLATE (RFC 1951)
- **Compression Level**: 9 (maximum)
- **Implementation**: Python's built-in zlib module
- **Function**: `compress_data()` in utils.py

### Example (Pseudo-code)

```python
def compress_data(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    return zlib.compress(message, level=9)
```

## Encryption

The application uses two encryption methods depending on message size:

### AES-256 Encryption (for messages ≥32 bytes)

#### Process

1. **Input**: Compressed message bytes, password
2. **Key Derivation**: PBKDF2 with SHA-256 derives a 32-byte key from the password
3. **Salt Generation**: 16 random bytes are generated for the salt
4. **IV Generation**: 16 random bytes are generated for the Initialization Vector
5. **Encryption**: AES-256 in CBC mode encrypts the compressed message
6. **Output**: Combined salt + IV + ciphertext

#### Technical Details

- **Algorithm**: AES-256-CBC
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Salt Size**: 16 bytes
- **IV Size**: 16 bytes
- **Padding**: PKCS#7
- **Implementation**: PyCryptodome library
- **Function**: `encrypt_message()` in utils.py

#### Example (Pseudo-code)

```python
def encrypt_message(compressed_data, password):
    # Derive key from password
    salt = os.urandom(16)
    key = pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
    
    # Generate random IV
    iv = os.urandom(16)
    
    # Encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(compressed_data, AES.block_size))
    
    # Combine salt + IV + ciphertext
    return salt + iv + ciphertext
```

### XOR Encryption (for messages <32 bytes)

#### Process

1. **Input**: Compressed message bytes, password
2. **Key Derivation**: SHA-256 hash of the password creates the key
3. **Encryption**: Each byte of the message is XORed with the corresponding byte of the key (cycling through the key)
4. **Output**: XOR-encrypted bytes

#### Technical Details

- **Algorithm**: XOR with SHA-256 hash of password
- **Key Size**: 32 bytes (SHA-256 output)
- **Padding**: None required
- **Implementation**: Custom implementation
- **Function**: Fallback encryption in `encrypt_message()` in api.py

#### Example (Pseudo-code)

```python
def xor_encrypt(compressed_data, password):
    # Generate key from password
    key = sha256(password.encode()).digest()
    
    # XOR each byte
    result = bytearray()
    for i, byte in enumerate(compressed_data):
        key_byte = key[i % len(key)]
        encrypted_byte = byte ^ key_byte
        result.append(encrypted_byte)
    
    return bytes(result)
```

## Steganography

The application employs LSB (Least Significant Bit) steganography to hide encrypted data within media files.

### Image Steganography

#### Process

1. **Input**: Encrypted data, carrier image
2. **Bit Conversion**: Encrypted data is converted to a string of bits
3. **LSB Substitution**: The least significant bit of each color channel (R,G,B) in pixels is replaced with a bit from the data
4. **Output**: An image visually identical to the original but containing the hidden data

#### Technical Details

- **Method**: LSB (Least Significant Bit) substitution
- **Bits Per Pixel**: 3 bits (one in each RGB channel)
- **Capacity**: Width × Height × 3 bits
- **Image Formats**: PNG preferred (lossless), JPEG converted to PNG
- **Functions**: `hide_data_in_image()` and `convert_and_hide_in_image()` in utils.py

#### Example (Pseudo-code)

```python
def hide_data_in_image(image_path, output_path, encrypted_data):
    # Convert encrypted data to bits
    binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)
    
    # Open image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    # Hide data in LSB of each color channel
    width, height = img.size
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Modify each color channel if data remains
            if data_index < len(binary_data):
                r = (r & ~1) | int(binary_data[data_index])
                data_index += 1
            
            if data_index < len(binary_data):
                g = (g & ~1) | int(binary_data[data_index])
                data_index += 1
                
            if data_index < len(binary_data):
                b = (b & ~1) | int(binary_data[data_index])
                data_index += 1
                
            pixels[x, y] = (r, g, b)
            
            if data_index >= len(binary_data):
                break
    
    # Save the modified image
    img.save(output_path)
```

### Audio Steganography

#### Process

1. **Input**: Encrypted data, carrier audio file
2. **Bit Conversion**: Encrypted data is converted to a string of bits
3. **LSB Substitution**: The least significant bit of each audio sample is replaced with a bit from the data
4. **Output**: An audio file audibly identical to the original but containing the hidden data

#### Technical Details

- **Method**: LSB substitution in audio samples
- **Bits Per Sample**: 1 bit
- **Capacity**: Number of audio samples
- **Audio Format**: WAV (other formats converted to WAV)
- **Function**: `hide_data_in_audio()` in utils.py

## Decryption

### Extraction Process

#### Process

1. **Input**: Stego media file (image or audio)
2. **LSB Extraction**: Extract the least significant bits from the media file
3. **Data Parsing**: Identify the encrypted data and embedded password (if present)
4. **Output**: Encrypted data and password (if found)

#### Technical Details

- **Image Extraction**: Read LSB from each color channel (RGB)
- **Audio Extraction**: Read LSB from each audio sample
- **Terminator**: Null byte (00000000) used to mark the end of data
- **Password Marker**: Byte 0x01 used to mark the start of embedded password
- **Functions**: `extract_data_from_image()` and `extract_data_from_audio()` in utils.py

### Decryption Process

#### Process

1. **Input**: Extracted encrypted data, password
2. **Method Detection**: Attempt XOR decryption first, then AES-256
3. **AES-256 Decryption**:
   - Extract salt (first 16 bytes) and IV (next 16 bytes)
   - Derive key from password and salt
   - Decrypt using AES-256-CBC
4. **XOR Decryption**:
   - Generate key from password using SHA-256
   - XOR each byte with the corresponding key byte
5. **Output**: Compressed message bytes

#### Technical Details

- **Algorithm Detection**: Automatic, based on decryption success
- **Implementation**: Matching the encryption methods
- **Validation**: UTF-8 decode check helps validate correct decryption
- **Function**: `decrypt_message()` in utils.py

### Decompression Process

#### Process

1. **Input**: Decrypted compressed data
2. **Decompression**: zlib decompression is applied
3. **String Conversion**: Decompressed bytes are converted to UTF-8 string
4. **Output**: Original message

#### Technical Details

- **Algorithm**: zlib DEFLATE
- **Implementation**: Python's built-in zlib module
- **Function**: `decompress_data()` in utils.py

## Technical Implementation

### Data Format Within Carrier File

The data hidden in the carrier file has the following structure:

```
┌─────────────────────┬─────────┬────────────────┐
│ Encrypted Data      │ Marker  │ Password       │
│ (Variable Length)   │ (0x01)  │ (Optional)     │
└─────────────────────┴─────────┴────────────────┘
```

For AES-encrypted data, the encrypted data has this structure:

```
┌─────────────┬─────────────┬─────────────────────┐
│ Salt        │ IV          │ Ciphertext          │
│ (16 bytes)  │ (16 bytes)  │ (Variable Length)   │
└─────────────┴─────────────┴─────────────────────┘
```

### Key Functions in Code

#### utils.py

```python
# Compression functions
def compress_data(data):
    """Compress data using zlib with maximum compression level"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return zlib.compress(data, level=9)

def decompress_data(compressed_data):
    """Decompress data that was compressed using zlib"""
    try:
        decompressed = zlib.decompress(compressed_data)
        return decompressed
    except zlib.error as e:
        raise ValueError(f"Decompression error: {str(e)}")

# Encryption functions
def encrypt_message(message, password):
    """Encrypt a message using AES-256-CBC with a password"""
    # Compress the message first
    if isinstance(message, str):
        message = message.encode('utf-8')
    compressed_message = compress_data(message)
    
    # Derive key from password
    key, salt = derive_key(password)
    
    # Generate random IV
    iv = os.urandom(16)
    
    # Create cipher object and encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(compressed_message, AES.block_size))
    
    # Return salt + IV + ciphertext
    return salt + iv + ciphertext

def decrypt_message(encrypted_data, password):
    """Decrypt a message using AES-256-CBC with a password"""
    try:
        # Check if we have enough data
        if len(encrypted_data) < 33:  # At least salt(16) + iv(16) + 1 byte of data
            return "Decryption error: No valid encrypted data found."
        
        # Extract salt, IV, and ciphertext
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        
        # Derive key from password and salt
        key, _ = derive_key(password, salt)
        
        # Create cipher object and decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        # Decompress the decrypted data
        decompressed = decompress_data(decrypted)
        
        return decompressed.decode('utf-8')
    except ValueError as e:
        if "Padding is incorrect" in str(e):
            return "Decryption error: Incorrect password or corrupted data."
        else:
            return f"Decryption error: {str(e)}"
    except Exception as e:
        return f"Decryption error: {str(e)}"
```

## Security Considerations

### Cryptographic Strength

- **AES-256**: Considered secure against brute force attacks
- **PBKDF2**: Key derivation with 100,000 iterations slows down brute force attempts
- **XOR with SHA-256**: Secure for small messages but less robust than AES for large data

### Compression Security Benefits

- **Reduced Footprint**: Smaller data means less information to hide
- **Increased Entropy**: Compressed data has higher entropy, making statistical analysis more difficult
- **Enhanced Deniability**: Lower impact on carrier files makes steganography harder to detect

### Potential Vulnerabilities

1. **Known-Plaintext Attacks**: If an attacker knows part of the original message
2. **Weak Passwords**: Dictionary words or short passwords reduce security significantly
3. **Steganalysis**: Statistical analysis might detect the presence of hidden data
4. **Format Conversion**: Converting the carrier file to another format will likely destroy hidden data

### Best Security Practices

1. **Use Strong Passwords**: At least 16 characters with mix of character types
2. **Use Auto-Generated Passwords**: The application can generate cryptographically strong passwords
3. **Separate Channels**: Send the password and stego file through different channels
4. **Avoid Reuse**: Don't reuse the same carrier file for multiple messages
5. **Use Original Files**: Don't modify stego files after creation
6. **Choose Appropriate Carriers**: Larger files with complex patterns hide data more effectively 