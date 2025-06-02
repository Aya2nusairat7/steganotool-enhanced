import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import numpy as np
import wave
import struct
import io
import cv2
import random
import binascii
import string
import subprocess
import tempfile
import urllib.request
import zipfile
import shutil
import zlib  # Add zlib for compression
import qrcode  # Import qrcode library

def derive_key(password, salt=None):
    """Derive a 32-byte key from a password using SHA-256"""
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
    return key, salt

def compress_data(data):
    """Compress data using zlib with maximum compression level, but only if it actually reduces size"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Try compressing the data
    compressed = zlib.compress(data, level=9)  # Use maximum compression level
    
    # Only return the compressed data if it's actually smaller
    if len(compressed) < len(data):
        print(f"DEBUG: Compression reduced size from {len(data)} to {len(compressed)} bytes")
        return compressed
    else:
        print(f"DEBUG: Compression would increase size from {len(data)} to {len(compressed)} bytes, using original data")
        # Add a marker byte (0xFF) to indicate uncompressed data
        return b'\xFF' + data

def decompress_data(compressed_data):
    """Decompress data that was compressed using zlib, or return original data if not compressed"""
    try:
        # Check if data is marked as uncompressed (first byte is 0xFF)
        if compressed_data and len(compressed_data) > 0 and compressed_data[0] == 0xFF:
            # Return the original data (without the marker byte)
            print("DEBUG: Data was not compressed, returning original data")
            return compressed_data[1:]
        
        # Otherwise decompress the data
        decompressed = zlib.decompress(compressed_data)
        print(f"DEBUG: Successfully decompressed data from {len(compressed_data)} to {len(decompressed)} bytes")
        return decompressed
    except zlib.error as e:
        print(f"DEBUG: Decompression error: {str(e)}")
        raise ValueError(f"Decompression error: {str(e)}")

def encrypt_message(message, password):
    """Encrypt a message using AES-256-CBC with a password"""
    # Compress the message first
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    compressed_message = compress_data(message)
    
    # Check if the data was actually compressed (marker byte 0xFF means not compressed)
    is_compressed = True
    if compressed_message and len(compressed_message) > 0 and compressed_message[0] == 0xFF:
        is_compressed = False
        # Remove the marker byte before encryption
        compressed_message = compressed_message[1:]
    
    # Derive key from password
    key, salt = derive_key(password)
    
    # Generate random IV
    iv = os.urandom(16)
    
    # Create cipher object and encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Add a marker byte after salt and IV to indicate compression status
    # Format: [salt][IV][compression_marker][ciphertext]
    if is_compressed:
        # 0x00 means data is compressed
        compression_marker = b'\x00'
    else:
        # 0xFF means data is not compressed
        compression_marker = b'\xFF'
    
    # Pad and encrypt the message
    ciphertext = cipher.encrypt(pad(compressed_message, AES.block_size))
    
    # Return salt + IV + compression marker + ciphertext
    return salt + iv + compression_marker + ciphertext

def decrypt_message(encrypted_data, password):
    """Decrypt a message using AES-256-CBC with a password"""
    try:
        # Check if we have enough data
        if len(encrypted_data) < 34:  # At least salt(16) + iv(16) + compression marker(1) + 1 byte of data
            return "Decryption error: No valid encrypted data found. The file may not contain a hidden message."
        
        # Extract salt, IV, compression marker, and ciphertext
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        compression_marker = encrypted_data[32:33]  # Single byte indicating compression status
        ciphertext = encrypted_data[33:]  # Rest is ciphertext
        
        # Derive key from password and salt
        key, _ = derive_key(password, salt)
        
        # Create cipher object and decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        # Check compression marker to determine if we need to decompress
        is_compressed = compression_marker != b'\xFF'
        
        if is_compressed:
            # Decompress the decrypted data
            decompressed = decompress_data(decrypted)
            return decompressed.decode('utf-8')
        else:
            # Data wasn't compressed, just decode it
            return decrypted.decode('utf-8')
            
    except ValueError as e:
        if "Padding is incorrect" in str(e):
            return "Decryption error: Incorrect password or corrupted data."
        elif "Data must be padded" in str(e):
            return "Decryption error: The extracted data is not properly formatted. The file may not contain a valid encrypted message."
        else:
            return f"Decryption error: {str(e)}"
    except Exception as e:
        return f"Decryption error: {str(e)}"

# Image steganography functions
def hide_data_in_image(input_path, output_path, data):
    """Hide binary data inside an image using LSB steganography"""
    try:
        # Ensure input_path and output_path are strings, not bytes
        if isinstance(input_path, bytes):
            input_path = input_path.decode('utf-8')
        if isinstance(output_path, bytes):
            output_path = output_path.decode('utf-8')
        
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        # Check if input or output file is JPEG/JPG format
        input_is_jpeg = input_path.lower().endswith(('.jpg', '.jpeg'))
        output_is_jpeg = output_path.lower().endswith(('.jpg', '.jpeg'))
        
        if input_is_jpeg:
            print("WARNING: Input image is in JPEG format, which is not suitable for steganography due to lossy compression.")
            print("Converting to PNG format for processing...")
        
        if output_is_jpeg:
            print("WARNING: JPEG output format is not suitable for steganography due to lossy compression!")
            print("The hidden data will likely be corrupted or lost when saved as JPEG.")
            print("Changing output format to PNG for reliable steganography.")
            output_path = os.path.splitext(output_path)[0] + ".png"
        
        # Convert binary data to a string of bits
        binary_data = ''.join(format(byte, '08b') for byte in data)
        # Add terminator
        binary_data += '00000000'  # Null byte as terminator
        
        print(f"DEBUG: Data length in bits: {len(binary_data)}")
        print(f"DEBUG: First 32 bits of data: {binary_data[:32]}")
        
        # Open the image
        img = Image.open(input_path)
        # Convert image to RGB if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        width, height = img.size
        print(f"DEBUG: Image dimensions: {width}x{height}")
        
        # Check if the image is big enough to hide the data
        max_bits = width * height * 3
        print(f"DEBUG: Maximum bits that can be stored: {max_bits}")
        
        if len(binary_data) > max_bits:
            raise ValueError(f"Data too large to hide in this image. Need {len(binary_data)} bits, but image can only store {max_bits} bits")
        
        # Convert image to numpy array for easier manipulation
        img_array = np.array(img)
        
        # Flatten the array for easier iteration
        flattened = img_array.reshape(-1)
        print(f"DEBUG: Array length: {len(flattened)}")
        
        # Embed data
        for i in range(len(binary_data)):
            if i < len(flattened):
                # Replace the least significant bit
                flattened[i] = (flattened[i] & 0xFE) | int(binary_data[i])
        
        print(f"DEBUG: Data embedded: {len(binary_data)} bits")
        
        # Reshape back to original dimensions
        img_array = flattened.reshape(img_array.shape)
        
        # Create a new image from the modified array
        modified_img = Image.fromarray(img_array)
        
        # Save the modified image
        modified_img.save(output_path)
        print(f"DEBUG: Image saved to {output_path}")
        
        # Verify the data was embedded correctly
        # Read back the first 32 bits for verification
        verification_bits = ""
        for i in range(min(32, len(binary_data))):
            verification_bits += str(flattened[i] & 1)
        
        print(f"DEBUG: Verification - first 32 bits read back: {verification_bits}")
        print(f"DEBUG: Do they match? {verification_bits == binary_data[:len(verification_bits)]}")
        
        return output_path
    except Exception as e:
        print(f"Error in hide_data_in_image: {str(e)}")
        raise

def extract_data_from_image(image_path):
    """Extract hidden data from an image using LSB steganography"""
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB if it's not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Get dimensions for debug output
    height, width = img_array.shape[:2]
    print(f"DEBUG: Image dimensions: {width}x{height}")
    
    # Flatten the array for easier iteration
    flattened = img_array.reshape(-1)
    print(f"DEBUG: Total pixels to scan: {len(flattened)}")
    
    # Extract the LSB from each byte
    extracted_bits = ""
    found_terminator = False
    terminator_position = -1
    
    # Print the first 100 bits to see pattern
    debug_bits = []
    
    # Scan the entire image, not just the first 1000 pixels
    for i in range(len(flattened)):
        bit = str(flattened[i] & 1)
        extracted_bits += bit
        
        # Save first 100 bits for debug output
        if i < 100:
            debug_bits.append(bit)
        
        # Check for terminator every 8 bits
        if len(extracted_bits) % 8 == 0 and len(extracted_bits) >= 8:
            byte_index = len(extracted_bits) - 8
            byte = extracted_bits[byte_index:byte_index+8]
            if byte == '00000000':
                found_terminator = True
                terminator_position = i
                extracted_bits = extracted_bits[:byte_index]
                print(f"DEBUG: Found terminator at position {terminator_position}")
                break
    
    print(f"DEBUG: First 100 extracted bits: {''.join(debug_bits)}")
    print(f"DEBUG: Terminator found: {found_terminator}")
    print(f"DEBUG: Total bits extracted: {len(extracted_bits)}")
    
    if len(extracted_bits) % 8 != 0:
        print(f"DEBUG: Warning - extracted bits not multiple of 8: {len(extracted_bits)}")
    
    # Group the bits into bytes
    extracted_bytes = []
    for i in range(0, len(extracted_bits), 8):
        if i + 8 <= len(extracted_bits):
            byte = extracted_bits[i:i+8]
            extracted_bytes.append(int(byte, 2))
    
    result = bytes(extracted_bytes)
    print(f"DEBUG: Extracted {len(result)} bytes of data")
    
    # Print first few bytes as hex for debugging
    if len(result) > 0:
        hex_data = ' '.join([f"{b:02x}" for b in result[:16]])
        print(f"DEBUG: First 16 bytes (hex): {hex_data}")
    else:
        print("DEBUG: No data extracted")
    
    return result

# Audio steganography functions
def hide_data_in_audio(audio_path, output_path, data):
    """Hide binary data inside an audio file using LSB steganography"""
    # Check if input is not WAV
    if not audio_path.lower().endswith('.wav'):
        print(f"Input audio is not WAV format. Converting...")
        converted_path = convert_audio_to_wav(audio_path)
        if not converted_path:
            raise ValueError("Failed to convert audio to WAV format")
        audio_path = converted_path
    
    # Check if output should be WAV
    if not output_path.lower().endswith('.wav'):
        print(f"Warning: Output must be WAV format for audio steganography")
        output_path = os.path.splitext(output_path)[0] + ".wav"
    
    try:
        # Open the audio file
        with wave.open(audio_path, 'rb') as audio_file:
            # Get audio parameters
            n_channels = audio_file.getnchannels()
            sample_width = audio_file.getsampwidth()
            framerate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            
            # Read all frames
            frames = audio_file.readframes(n_frames)
        
        # Print debug info
        print(f"DEBUG: Audio parameters: {n_channels} channels, {sample_width} bytes/sample, {framerate} Hz, {n_frames} frames")
        print(f"DEBUG: Total audio size: {len(frames)} bytes")
        
        # Convert binary data to a string of bits
        binary_data = ''.join(format(byte, '08b') for byte in data)
        # Add terminator
        binary_data += '00000000'  # Null byte as terminator
        
        print(f"DEBUG: Data length in bits: {len(binary_data)}")
        print(f"DEBUG: First 32 bits of data: {binary_data[:32] if len(binary_data) >= 32 else binary_data}")
        
        # Check if the audio file is big enough to hide the data
        if len(binary_data) > len(frames):
            raise ValueError(f"Data too large to hide in this audio file. Need {len(binary_data)} bits, but audio has only {len(frames)} bytes")
        
        # Create a new audio file
        with wave.open(output_path, 'wb') as output_file:
            output_file.setparams((n_channels, sample_width, framerate, n_frames, 'NONE', 'not compressed'))
            
            # Modify frames to hide data
            frames_list = bytearray(frames)
            
            # Embed one bit per byte
            for i in range(len(binary_data)):
                if i < len(frames_list):
                    # Modify the LSB of the frame byte
                    frames_list[i] = (frames_list[i] & 0xFE) | int(binary_data[i])
            
            print(f"DEBUG: Data embedded: {len(binary_data)} bits")
            
            # Write modified frames to output file
            output_file.writeframes(bytes(frames_list))
            
            print(f"DEBUG: Output saved with {len(frames_list)} bytes")
        
        return output_path
    except Exception as e:
        print(f"Error in hide_data_in_audio: {str(e)}")
        raise

def extract_data_from_audio(audio_path):
    """Extract hidden data from an audio file using LSB steganography"""
    # Check if input is not WAV
    if not audio_path.lower().endswith('.wav'):
        print(f"Input audio is not WAV format. Converting...")
        converted_path = convert_audio_to_wav(audio_path)
        if not converted_path:
            raise ValueError("Failed to convert audio to WAV format")
        audio_path = converted_path
    
    try:
        # Open the audio file
        with wave.open(audio_path, 'rb') as audio_file:
            # Get audio parameters
            n_channels = audio_file.getnchannels()
            sample_width = audio_file.getsampwidth()
            framerate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            
            # Read all frames
            frames = audio_file.readframes(n_frames)
        
        # Print debug info
        print(f"DEBUG: Audio parameters: {n_channels} channels, {sample_width} bytes/sample, {framerate} Hz, {n_frames} frames")
        print(f"DEBUG: Total audio size: {len(frames)} bytes")
        
        # Extract the LSB from each byte
        extracted_bits = ""
        for i in range(len(frames)):
            # Get LSB from each byte
            extracted_bits += str(frames[i] & 1)
            
            # Check for terminator every 8 bits
            if len(extracted_bits) % 8 == 0 and len(extracted_bits) >= 8:
                byte_index = len(extracted_bits) - 8
                byte = extracted_bits[byte_index:byte_index+8]
                if byte == '00000000':
                    # Found terminator, truncate the bits
                    extracted_bits = extracted_bits[:byte_index]
                    print(f"DEBUG: Found terminator at position {i}")
                    break
        
        # Print debug info
        print(f"DEBUG: Total bits extracted: {len(extracted_bits)}")
        if len(extracted_bits) > 0:
            print(f"DEBUG: First 32 bits extracted: {extracted_bits[:32] if len(extracted_bits) >= 32 else extracted_bits}")
        
        # Check if we have valid data
        if len(extracted_bits) == 0 or len(extracted_bits) % 8 != 0:
            print(f"DEBUG: Warning - extracted bits not multiple of 8: {len(extracted_bits)}")
            
            # Try to pad if almost a multiple of 8
            remainder = len(extracted_bits) % 8
            if remainder > 0:
                padding = '0' * (8 - remainder)
                extracted_bits += padding
                print(f"DEBUG: Padded with {8 - remainder} zeros")
        
        # Group the bits into bytes
        extracted_bytes = []
        for i in range(0, len(extracted_bits), 8):
            if i + 8 <= len(extracted_bits):
                byte = extracted_bits[i:i+8]
                extracted_bytes.append(int(byte, 2))
        
        result = bytes(extracted_bytes)
        print(f"DEBUG: Extracted {len(result)} bytes of data")
        
        # Print first few bytes as hex for debugging
        if len(result) > 0:
            hex_data = ' '.join([f"{b:02x}" for b in result[:16]])
            print(f"DEBUG: First 16 bytes (hex): {hex_data}")
        else:
            print("DEBUG: No data extracted")
        
        return result
    except Exception as e:
        print(f"Error in extract_data_from_audio: {str(e)}")
        raise

# Video steganography functions
def hide_data_in_video(video_path, data, output_path):
    """Hide binary data inside a video file using LSB steganography in frames"""
    # Convert binary data to a string of bits
    binary_data = ''.join(format(byte, '08b') for byte in data)
    # Add terminator
    binary_data += '00000000'  # Null byte as terminator
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec
    
    # Create video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Calculate total available bits in the video
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Could not read video file")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    bits_per_frame = frame.size  # Each pixel has 3 channels (RGB), and we use 1 bit per channel
    total_bits = total_frames * bits_per_frame
    
    if len(binary_data) > total_bits:
        raise ValueError("Data too large to hide in this video file")
    
    # Reset the video
    cap.release()
    cap = cv2.VideoCapture(video_path)
    
    # Hide data in the first frame
    ret, frame = cap.read()
    if ret:
        # Flatten the frame for easier iteration
        flattened = frame.flatten()
        
        # Embed data
        for i in range(len(binary_data)):
            if i < len(flattened):
                # Replace the least significant bit
                flattened[i] = (flattened[i] & 0xFE) | int(binary_data[i])
        
        # Reshape back to original dimensions
        frame = flattened.reshape(frame.shape)
        
        # Write the modified first frame
        out.write(frame)
    
    # Copy the rest of the frames without modification
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    # Release resources
    cap.release()
    out.release()
    
    return output_path

def extract_data_from_video(video_path):
    """Extract hidden data from a video file using LSB steganography"""
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get the first frame
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Could not read video file")
    
    # Flatten the frame for easier iteration
    flattened = frame.flatten()
    
    # Extract the LSB from each byte
    extracted_bits = ""
    for i in range(len(flattened)):
        extracted_bits += str(flattened[i] & 1)
        
        # Check for terminator every 8 bits
        if len(extracted_bits) % 8 == 0:
            byte_index = len(extracted_bits) - 8
            byte = extracted_bits[byte_index:byte_index+8]
            if byte == '00000000':
                # Found terminator, truncate the bits
                extracted_bits = extracted_bits[:byte_index]
                break
    
    # Group the bits into bytes
    extracted_bytes = []
    for i in range(0, len(extracted_bits), 8):
        if i + 8 <= len(extracted_bits):
            byte = extracted_bits[i:i+8]
            extracted_bytes.append(int(byte, 2))
    
    # Release resources
    cap.release()
    
    # Convert bytes to binary data
    return bytes(extracted_bytes)

def generate_strong_password(length=16):
    """Generate a strong random password"""
    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    # Ensure at least one of each character type
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest of the password
    for _ in range(length - 4):
        password.append(random.choice(
            uppercase_letters + lowercase_letters + digits + special_chars
        ))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    # Convert list to string
    return ''.join(password)

def save_password_to_file(password, output_path):
    """Save the generated password to a text file"""
    password_file = os.path.splitext(output_path)[0] + "_password.txt"
    with open(password_file, 'w') as f:
        f.write(f"Encryption Password: {password}\n")
        f.write("IMPORTANT: Keep this file secure. You will need this password to decrypt the hidden message.\n")
    return password_file 

def convert_audio_to_wav(audio_path):
    """Convert any audio format to WAV for steganography compatibility
    
    Returns the path to the converted WAV file (or original if already WAV)
    """
    # Check if already WAV
    if audio_path.lower().endswith('.wav'):
        return audio_path
    
    # Check if the input file exists
    if not os.path.exists(audio_path):
        print(f"Warning: Input file '{audio_path}' doesn't exist. This might be a test call.")
        # If it looks like a test call, just try to set up FFmpeg
        download_ffmpeg()
        return None
    
    # Create output path
    output_wav = os.path.splitext(audio_path)[0] + "_converted.wav"
    
    try:
        # Function to download FFmpeg if not found (Windows only)
        ffmpeg_cmd = find_or_download_ffmpeg()
        
        if not ffmpeg_cmd:
            print("FFmpeg not found and download failed.")
            print("Please install FFmpeg manually from: https://ffmpeg.org/download.html")
            print("Make sure to add the bin directory to your PATH.")
            return None
                
        # Use raw strings for Windows paths
        cmd = [ffmpeg_cmd, '-i', audio_path, '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_wav]
        
        print(f"Converting {os.path.basename(audio_path)} to WAV format...")
        print(f"Running command: {' '.join(cmd)}")
        
        # Run with shell=True on Windows
        import platform
        is_windows = platform.system() == "Windows"
        
        result = subprocess.run(cmd, 
                              check=True, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              shell=is_windows)
        
        print(f"Successfully converted to WAV: {output_wav}")
        return output_wav
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio: {str(e)}")
        if hasattr(e, 'stderr'):
            print(f"FFmpeg error output: {e.stderr.decode('utf-8', errors='ignore')}")
        print("Please install ffmpeg or convert the file manually to WAV format.")
        return None
    except Exception as e:
        print(f"Unexpected error converting audio: {str(e)}")
        print("If FFmpeg is not installed, please download it from: https://ffmpeg.org/download.html")
        print("Make sure to add FFmpeg to your system PATH after installation.")
        return None

def find_or_download_ffmpeg():
    """Find FFmpeg on the system or download it if not found on Windows"""
    import platform
    
    # Check if we're on Windows
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        # Try to find ffmpeg in common Windows locations
        ffmpeg_paths = [
            "ffmpeg",  # If in PATH
            "ffmpeg.exe",  # If in PATH with extension
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            os.path.join(os.environ.get('LOCALAPPDATA', ''), "Programs", "ffmpeg", "bin", "ffmpeg.exe"),
            os.path.join(os.path.expanduser("~"), "ffmpeg", "bin", "ffmpeg.exe")
        ]
        
        for path in ffmpeg_paths:
            try:
                # Test if this path works
                subprocess.run([path, "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                print(f"Found ffmpeg at: {path}")
                return path
            except Exception:
                continue
        
        # If not found, try to download
        return download_ffmpeg()
    else:
        # On Linux/Mac just return the command name
        return "ffmpeg"

def download_ffmpeg():
    """Download FFmpeg for Windows"""
    try:
        print("FFmpeg not found. Attempting to download...")
        import tempfile
        import urllib.request
        import zipfile
        import shutil
        
        # Create ffmpeg directory in user's home directory
        user_ffmpeg_dir = os.path.join(os.path.expanduser("~"), "ffmpeg", "bin")
        os.makedirs(user_ffmpeg_dir, exist_ok=True)
        
        # Path for the executable
        user_ffmpeg_exe = os.path.join(user_ffmpeg_dir, "ffmpeg.exe")
        
        # Direct download of the static builds
        ffmpeg_url = "https://github.com/GyanD/codexffmpeg/releases/download/6.0/ffmpeg-6.0-essentials_build.zip"
        
        # Download to temp file
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "ffmpeg.zip")
        
        print(f"Downloading FFmpeg from {ffmpeg_url}...")
        
        # Use a custom user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Create request with headers
        request = urllib.request.Request(ffmpeg_url, headers=headers)
        
        # Download the file
        with urllib.request.urlopen(request) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        
        # Extract zip
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the ffmpeg.exe in the extracted folders
        ffmpeg_exe = None
        for root, dirs, files in os.walk(temp_dir):
            if "ffmpeg.exe" in files:
                ffmpeg_exe = os.path.join(root, "ffmpeg.exe")
                # Copy ffmpeg.exe to user's directory
                shutil.copy2(ffmpeg_exe, user_ffmpeg_exe)
                print(f"FFmpeg installed to: {user_ffmpeg_dir}")
                print("Please add this directory to your PATH for future use.")
                break
        
        # Clean up temp directory
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
        
        if os.path.exists(user_ffmpeg_exe):
            return user_ffmpeg_exe
        else:
            print("Could not install FFmpeg automatically.")
            return None
            
    except Exception as e:
        print(f"Error downloading FFmpeg: {str(e)}")
        return None

def convert_and_hide_in_image(input_path, output_path, data):
    """Convert any image format (including JPEG/JPG) to PNG and hide data in it"""
    try:
        # Ensure input_path and output_path are strings, not bytes
        if isinstance(input_path, bytes):
            input_path = input_path.decode('utf-8')
        if isinstance(output_path, bytes):
            output_path = output_path.decode('utf-8')
        
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        # Always ensure output is PNG regardless of extension provided
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + ".png"
            print(f"Changed output path to {output_path} to ensure lossless format")
        
        # Open and convert the image
        print(f"Opening image at {input_path}")
        img = Image.open(input_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print(f"Converted image to RGB mode")
        
        # Save as temporary PNG file
        temp_png_path = os.path.join(os.path.dirname(output_path), "temp_converted.png")
        img.save(temp_png_path, format="PNG")
        print(f"Saved temporary PNG at {temp_png_path}")
        
        # Now hide data in the PNG
        result = hide_data_in_image(temp_png_path, output_path, data)
        
        # Clean up temporary file
        try:
            os.remove(temp_png_path)
        except:
            print(f"Warning: Could not remove temporary file {temp_png_path}")
        
        return result
    
    except Exception as e:
        print(f"Error in convert_and_hide_in_image: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def generate_qr_code(data, output_path, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4):
    """
    Generate a QR code and save it to the specified path
    
    Args:
        data: The data to encode in the QR code
        output_path: The path to save the QR code image
        error_correction: QR error correction level (L, M, Q, H)
        box_size: Size of each box in the QR code
        border: Border size in boxes
        
    Returns:
        Path to the generated QR code
    """
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=None,  # Auto determine version
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        
        # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        img.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        raise

def hide_message_in_qr(message, password, output_path, background_image=None, style="standard"):
    """
    Generate a QR code with a hidden message
    
    Args:
        message: The message to hide
        password: Password for encryption
        output_path: Path to save the QR code
        background_image: Optional background image path
        style: QR code style ("standard", "embedded", "fancy")
        
    Returns:
        Path to the generated QR code
    """
    try:
        # Encrypt the message
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
            
        encrypted_data = encrypt_message(message_bytes, password)
        
        # Create the QR code with embedded password
        data_to_encode = encrypted_data + b'\x01' + password.encode('utf-8')
        
        # Convert binary data to a base64 string for QR encoding
        encoded_data = binascii.hexlify(data_to_encode).decode('ascii')
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(encoded_data)
        qr.make(fit=True)
        
        # Create QR code image
        if style == "standard":
            img = qr.make_image(fill_color="black", back_color="white")
        elif style == "fancy":
            # Create a colored QR code
            img = qr.make_image(fill_color="blue", back_color="white")
        elif style == "embedded":
            # Create QR with lower contrast for better blending
            img = qr.make_image(fill_color="black", back_color="white")
            
        # Handle background image if provided
        if background_image and os.path.exists(background_image):
            # Open background image
            bg = Image.open(background_image)
            
            # Resize background to match QR code size
            bg = bg.resize(img.size)
            
            if style == "embedded":
                # Blend QR code with background image
                img = Image.blend(bg.convert("RGBA"), img.convert("RGBA"), 0.7)
            else:
                # Center QR code on background
                bg.paste(img, (0, 0))
                img = bg
        
        # Save the final image
        img.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error hiding message in QR code: {str(e)}")
        raise

def extract_message_from_qr(qr_code_path, password=None):
    """
    Extract hidden message from a QR code
    
    Args:
        qr_code_path: Path to the QR code image
        password: Optional password for decryption (if not embedded)
        
    Returns:
        The extracted message
    """
    try:
        # Read QR code
        img = Image.open(qr_code_path)
        
        # Try using pyzbar first, which tends to be more reliable
        try:
            from pyzbar.pyzbar import decode
            decoded_objects = decode(img)
            if decoded_objects:
                print("Successfully decoded QR with pyzbar")
                decoded_info = [decoded_objects[0].data.decode('ascii')]
            else:
                # If pyzbar fails, try OpenCV
                print("Pyzbar couldn't decode, trying OpenCV...")
                # Convert PIL image to OpenCV format properly
                # Convert to RGB first to ensure we have a 3-channel image
                img_rgb = img.convert('RGB')
                cv_img = np.array(img_rgb)
                # Convert RGB to BGR (OpenCV format)
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
                
                # Initialize QR code detector
                detector = cv2.QRCodeDetector()
                
                # Detect and decode
                retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(cv_img)
                
                if not retval or len(decoded_info) == 0:
                    return "No QR code found in the image"
        except Exception as e:
            print(f"Error in QR code reading: {str(e)}")
            # Last resort: try OpenCV if pyzbar failed to import or process
            try:
                print("Trying OpenCV as fallback...")
                img_rgb = img.convert('RGB')
                cv_img = np.array(img_rgb)
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
                
                detector = cv2.QRCodeDetector()
                retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(cv_img)
                
                if not retval or len(decoded_info) == 0:
                    return "Failed to extract QR code data. The image may not contain a valid QR code."
            except Exception as nested_e:
                return f"Failed to extract QR code data. Error: {str(nested_e)}"
        
        # Convert hex string back to binary data
        try:
            encrypted_data = binascii.unhexlify(decoded_info[0])
        except (binascii.Error, IndexError) as e:
            return f"Error: Could not decode QR code data. The QR code may not contain steganographic content. Details: {str(e)}"
        
        # Look for embedded password (marker byte 0x01 indicates password follows)
        embedded_password = None
        password_found = False
        data = encrypted_data  # Default if no marker is found
        
        # Search for the marker byte
        for i in range(len(encrypted_data) - 1):
            if encrypted_data[i] == 0x01:  # Found marker
                data = encrypted_data[:i]
                try:
                    embedded_password = encrypted_data[i+1:].decode('utf-8')
                    password_found = True
                    print(f"Found embedded password: {embedded_password}")
                    break
                except UnicodeDecodeError:
                    print("Failed to decode embedded password - possible corruption")
        
        # Always use embedded password if available
        if password_found:
            password = embedded_password
        # Only use provided password if no embedded password was found
        elif not password:
            return "No password provided or found in the QR code"
        
        # Decrypt the message
        try:
            decrypted_message = decrypt_message(data, password)
            return decrypted_message
        except Exception as e:
            return f"Error decrypting message: {str(e)}. The password may be incorrect or the data corrupted."
        
    except Exception as e:
        print(f"Error extracting message from QR code: {str(e)}")
        return f"Error: {str(e)}"