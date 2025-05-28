# Steganography Process Documentation

This document explains in detail how the steganography process works in SteganoTool for hiding and extracting encrypted messages in different media types.

## Table of Contents
- [Overview](#overview)
- [Steganography Techniques](#steganography-techniques)
- [Encryption and Steganography Workflow](#encryption-and-steganography-workflow)
- [Media-Specific Implementations](#media-specific-implementations)
- [Security Considerations](#security-considerations)
- [Technical Limitations](#technical-limitations)

## Overview

Steganography is the practice of concealing information within other non-secret data or a physical object to avoid detection. SteganoTool implements steganography by hiding encrypted messages within digital media files such as images, audio files, and QR codes.

The steganography process in SteganoTool follows these general steps:

1. **Preparation**: The message is compressed and encrypted
2. **Embedding**: The encrypted data is hidden in a carrier file
3. **Extraction**: The hidden data is extracted from the carrier file
4. **Decryption**: The extracted data is decrypted to reveal the original message

## Steganography Techniques

### Least Significant Bit (LSB) Steganography

The primary technique used in SteganoTool is LSB steganography, which works by replacing the least significant bit of each byte in the carrier file with a bit from the message to be hidden.

#### How LSB Works

In digital media, changing the least significant bit of a byte causes minimal perceptible change:

- For images: In a 24-bit image (8 bits each for R, G, B), changing the LSB of each color channel is virtually imperceptible to the human eye.
- For audio: In audio samples, changing the LSB causes minimal audible difference.

#### Example: LSB in Images

For an RGB pixel with values:
- Red: 10101010
- Green: 11110000
- Blue: 10001101

To hide the bits '101', we modify the LSBs:
- Red: 1010101**1** (LSB changed from 0 to 1)
- Green: 1111000**0** (LSB remains 0)
- Blue: 1000110**1** (LSB remains 1)

The visual difference is negligible, but we've now stored 3 bits of our message.

## Encryption and Steganography Workflow

### Encryption Process (Hide Message)

1. **Input Collection**
   - User provides a message to hide
   - User provides a carrier file (image, audio)
   - User provides a password or requests auto-generation

2. **Message Preparation**
   - Message is encoded to UTF-8 bytes
   - Data is compressed using zlib **only if compression actually reduces size**
   - If compression would increase size, the original data is used instead

3. **Encryption**
   - For short messages (<32 bytes): Simple XOR encryption with SHA-256 hash of password
   - For normal messages: AES-256-CBC encryption
     - Password is used to derive a key using PBKDF2
     - Random initialization vector (IV) is generated
     - A compression marker byte is added (0x00 if compressed, 0xFF if not)
     - Message is padded and encrypted

4. **Data Packaging**
   - Format: `[encrypted_data][0x01 marker byte][password_bytes]`
   - Encrypted data format: `[salt(16)][IV(16)][compression_marker(1)][ciphertext]`
   - If auto-generated password is used, it's appended for later retrieval

5. **Media-Specific Embedding**
   - Image: LSB embedding in pixel color values
   - Audio: LSB embedding in audio samples
   - QR Code: Encrypted data encoded directly in QR

6. **Output Generation**
   - Modified carrier file is saved with hidden data
   - Metadata is provided to the user (file size, compression ratio, etc.)

### Decryption Process (Extract Message)

1. **Input Collection**
   - User provides the carrier file with hidden data
   - User provides a password (if not embedded in the file)

2. **Data Extraction**
   - Media-specific extraction method retrieves hidden bits
   - Bits are converted back to bytes
   - Format is parsed: `[encrypted_data][0x01 marker byte][password_bytes]`

3. **Password Handling**
   - If 0x01 marker is found, embedded password is used
   - Otherwise, user-provided password is used

4. **Decryption**
   - System attempts XOR decryption for short messages
   - If unsuccessful, AES decryption is used:
     - Salt and IV are extracted from the data
     - Compression marker byte is read (0x00 means compressed, 0xFF means not compressed)
     - Key is derived from password and salt
     - Ciphertext is decrypted and unpadded

5. **Message Recovery**
   - If data was compressed (marker is 0x00), the decrypted data is decompressed using zlib
   - If data was not compressed (marker is 0xFF), the decrypted data is used directly
   - Bytes are decoded to UTF-8 text
   - Original message is presented to the user

## Media-Specific Implementations

### Image Steganography

1. **Carrier Preparation**
   - Image is converted to PNG format if needed (for lossless storage)
   - Image is converted to RGB color mode if needed

2. **Capacity Calculation**
   - Maximum bits = width × height × 3 (RGB channels)
   - System checks if the image can hold the data

3. **Embedding Process**
   - Image data is converted to a NumPy array
   - Each bit of the message replaces the LSB of a color channel value
   - Modified array is converted back to an image
   - Image is saved in PNG format

4. **Extraction Process**
   - Image is loaded and converted to a NumPy array
   - LSB of each color channel value is extracted
   - Bits are collected until a null terminator is found
   - Bits are converted back to bytes

### Audio Steganography

1. **Carrier Preparation**
   - Audio is converted to WAV format if needed
   - Audio frames are read as samples

2. **Capacity Calculation**
   - Maximum bits = number of audio samples
   - System checks if the audio can hold the data

3. **Embedding Process**
   - Each bit of the message replaces the LSB of an audio sample
   - Modified samples are written to a new WAV file

4. **Extraction Process**
   - Audio samples are read from the WAV file
   - LSB of each sample is extracted
   - Bits are collected until a null terminator is found
   - Bits are converted back to bytes

### QR Code Steganography

1. **QR Code Generation**
   - Encrypted message is encoded directly in a QR code
   - Different styles can be applied (standard, fancy, embedded)
   - Optional background image can be added

2. **QR Code Reading**
   - QR code is scanned to extract the encrypted data
   - Data is decrypted to recover the original message

## Security Considerations

### Steganographic Security

1. **Visual/Audible Imperceptibility**
   - Changes to the carrier file should not be perceptible to human senses
   - SteganoTool uses LSB technique which minimizes visual/audible changes

2. **Statistical Imperceptibility**
   - Modified files should not show statistical anomalies
   - Random distribution of message bits helps avoid detection

3. **Format Preservation**
   - Using PNG for images preserves hidden data (lossless)
   - JPEG compression would destroy hidden data, so it's avoided for output

### Cryptographic Security

1. **Strong Encryption**
   - AES-256 in CBC mode provides strong encryption
   - Password-derived keys using PBKDF2 with 100,000 iterations
   - Random IV for each encryption operation

2. **Password Handling**
   - Auto-generated passwords include a mix of character types
   - Passwords are embedded after a marker byte for convenience but can be omitted for higher security

## Technical Limitations

1. **Capacity Limitations**
   - LSB technique can hide ~1/8 of the carrier file size
   - Large messages require large carrier files

2. **Format Requirements**
   - Output image files must be PNG (lossless)
   - Output audio files must be WAV (lossless)
   - Any modification to the carrier file after hiding data will likely corrupt the hidden message

3. **Detection Resistance**
   - Basic statistical analysis might detect the presence of hidden data
   - Not designed to resist advanced steganalysis techniques

4. **Compression Considerations**
   - Small messages may not benefit from compression and might actually increase in size when compressed
   - The system intelligently determines whether to use compression based on the actual size reduction
   - Very random or already compressed data (images, videos, etc.) will typically not be compressed again

5. **Error Resilience**
   - No error correction in the base steganography implementation
   - Even minor modifications to the carrier file can corrupt the hidden message
   - QR codes have built-in error correction that provides some resilience

## Conclusion

SteganoTool implements a comprehensive steganography solution that combines data compression, strong encryption, and LSB steganography techniques to hide secret messages in various media types. The process is designed to be secure, user-friendly, and adaptable to different use cases while maintaining the imperceptibility of the hidden data. 