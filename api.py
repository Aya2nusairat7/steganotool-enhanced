import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
import utils
import hashlib
import traceback

# Create Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64MB max upload (increased from 16MB)

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Utility function for encryption
def encrypt_message(message, password):
    try:
        # Print debug info
        if isinstance(message, bytes):
            try:
                message_preview = message.decode('utf-8')[:10] + "..." if len(message) > 10 else message.decode('utf-8')
            except UnicodeDecodeError:
                message_preview = f"<binary data, {len(message)} bytes>"
        else:
            message_preview = message[:10] + "..." if len(message) > 10 else message
            
        print(f"DEBUG: Encrypting message: '{message_preview}' ({len(message)} chars/bytes) with password: {password[:2]}{'*' * (len(password) - 4)}{password[-2:] if len(password) > 2 else ''}")
        
        if isinstance(message, str):
            message = message.encode('utf-8')
            
        # For very short messages, use simpler encryption
        if len(message) < 32:
            print("DEBUG: Using simple XOR encryption for short message")
            # Use simple XOR encryption for short messages
            if isinstance(password, str):
                password_bytes = password.encode('utf-8')
            else:
                password_bytes = password
                
            key = hashlib.sha256(password_bytes).digest()
            encrypted = []
            for i, char in enumerate(message):
                key_char = key[i % len(key)]
                encrypted_char = char ^ key_char
                encrypted.append(encrypted_char)
            
            result = bytes(encrypted)
            print(f"DEBUG: XOR encryption result: {len(result)} bytes")
            return result
        
        # Use the utils encrypt_message function for normal messages
        try:
            print("DEBUG: Using AES encryption")
            return utils.encrypt_message(message, password)
        except Exception as e:
            # Fallback encryption if utils function fails
            print(f"DEBUG: AES encryption failed: {str(e)}, falling back to XOR")
            if isinstance(password, str):
                password_bytes = password.encode('utf-8')
            else:
                password_bytes = password
                
            key = hashlib.sha256(password_bytes).digest()
            encrypted = []
            for i, char in enumerate(message):
                key_char = key[i % len(key)]
                encrypted_char = char ^ key_char
                encrypted.append(encrypted_char)
            return bytes(encrypted)
    except Exception as e:
        print(f"DEBUG: Encryption failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

# Utility function for decryption
def decrypt_message(encrypted_data, password):
    try:
        # Use the decrypt_message function from utils module
        return utils.decrypt_message(encrypted_data, password)
    except (AttributeError, ImportError):
        # Fallback decryption if utils function is not available
        if isinstance(password, str):
            password = password.encode('utf-8')
            
        key = hashlib.sha256(password).digest()
        decrypted = []
        for i, char in enumerate(encrypted_data):
            key_char = key[i % len(key)]
            decrypted_char = char ^ key_char
            decrypted.append(decrypted_char)
        return bytes(decrypted)

# API routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    """Encrypt a message and hide it in a media file"""
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        message = request.form.get('message', '')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get auto_generate flag from request
        auto_generate = request.form.get('auto_generate', 'false').lower() == 'true'
        
        # Auto-generate password or use provided one
        if auto_generate:
            password = utils.generate_strong_password(16)
            print(f"Auto-generated password: {password}")
        else:
            password = request.form.get('password', '')
            if not password:
                return jsonify({'error': 'No password provided and auto-generate not enabled'}), 400
        
        media_type = request.form.get('media_type', 'image')
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        orig_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(orig_file_path)
        
        # Get original message size
        original_size = len(message.encode('utf-8'))
        
        # Encrypt the message
        message_bytes = message.encode('utf-8') if isinstance(message, str) else message
        encrypted_data = encrypt_message(message_bytes, password)
        
        # Calculate compression ratio
        compressed_size = len(encrypted_data)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        # Prepare the data to be hidden
        # Format: [encrypted data][1 byte: marker][password bytes]
        password_bytes = password.encode('utf-8') if isinstance(password, str) else password
        data_to_hide = encrypted_data + b'\x01' + password_bytes
        
        # Generate output filename
        file_extension = Path(filename).suffix.lower()
        filename_base = Path(filename).stem
        
        # Process based on media type
        if media_type == 'image':
            # Handle all image formats, including JPEG/JPG
            output_filename = f"stego_{filename_base}.png"  # Always use PNG for output
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # Use convert_and_hide_in_image for all image formats
            if hasattr(utils, 'convert_and_hide_in_image'):
                utils.convert_and_hide_in_image(orig_file_path, output_path, data_to_hide)
            else:
                return jsonify({'error': 'Image conversion not supported in this build'}), 400
            
            # Get file size for response
            file_size = os.path.getsize(output_path)
            
            return jsonify({
                'status': 'success',
                'original_filename': filename,
                'output_filename': output_filename,
                'file_size': file_size,
                'encrypted_size': len(encrypted_data),
                'message_length': len(message),
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'auto_generated': auto_generate,
                'auto_generated_password': password if auto_generate else None,
                'download_url': f"/api/download/{output_filename}",
                'media_type': 'image'
            })
        
        elif media_type == 'audio':
            # Convert to WAV if needed
            if file_extension != '.wav':
                print(f"Converting audio to WAV: {filename}")
                if hasattr(utils, 'convert_audio_to_wav'):
                    wav_path = utils.convert_audio_to_wav(orig_file_path)
                    orig_file_path = wav_path
                    file_extension = '.wav'
                else:
                    return jsonify({'error': 'Audio conversion not supported in this build'}), 400
            
            output_filename = f"stego_{filename_base}.wav"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # Hide data in audio
            if hasattr(utils, 'hide_data_in_audio'):
                utils.hide_data_in_audio(orig_file_path, output_path, data_to_hide)
            else:
                return jsonify({'error': 'Audio steganography not supported in this build'}), 400
            
            # Get file size for response
            file_size = os.path.getsize(output_path)
            
            return jsonify({
                'status': 'success',
                'original_filename': filename,
                'output_filename': output_filename,
                'file_size': file_size,
                'encrypted_size': len(encrypted_data),
                'message_length': len(message),
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'auto_generated': auto_generate,
                'auto_generated_password': password if auto_generate else None,
                'download_url': f"/api/download/{output_filename}",
                'media_type': 'audio'
            })
        
        else:
            return jsonify({'error': 'Unsupported media type'}), 400
    
    except Exception as e:
        print(f"Error in encryption process: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    """Extract and decrypt a hidden message from a media file"""
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        # Password is optional now - it will be extracted from the file if not provided
        password = request.form.get('password', '')
        media_type = request.form.get('media_type', 'image')
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract data based on media type
        if media_type == 'image':
            # Extract data from image
            if hasattr(utils, 'extract_data_from_image'):
                extracted_data = utils.extract_data_from_image(file_path)
            else:
                return jsonify({'status': 'error', 'message': 'Image steganography not supported in this build'}), 400
            
        elif media_type == 'audio':
            # Convert to WAV if needed
            file_extension = Path(filename).suffix.lower()
            if file_extension != '.wav':
                print(f"Converting audio to WAV for extraction: {filename}")
                if hasattr(utils, 'convert_audio_to_wav'):
                    wav_path = utils.convert_audio_to_wav(file_path)
                    file_path = wav_path
                else:
                    return jsonify({'status': 'error', 'message': 'Audio conversion not supported in this build'}), 400
            
            # Extract data from audio
            if hasattr(utils, 'extract_data_from_audio'):
                extracted_data = utils.extract_data_from_audio(file_path)
            else:
                return jsonify({'status': 'error', 'message': 'Audio steganography not supported in this build'}), 400
            
        else:
            return jsonify({'status': 'error', 'message': 'Unsupported media type'}), 400
        
        # Debug info
        print(f"DEBUG: Extracted data length: {len(extracted_data)} bytes")
        if len(extracted_data) > 0:
            print(f"DEBUG: First few bytes: {' '.join([f'{b:02x}' for b in extracted_data[:16]])}")
        
        # Look for embedded password (marker byte 0x01 indicates password follows)
        embedded_password = None
        password_found = False
        encrypted_data = extracted_data
        
        # Search for the marker byte
        for i in range(len(extracted_data) - 1):
            if extracted_data[i] == 0x01:  # Found marker
                encrypted_data = extracted_data[:i]
                try:
                    embedded_password = extracted_data[i+1:].decode('utf-8')
                    password_found = True
                    print(f"Found embedded password: {embedded_password}")
                    print(f"DEBUG: Encrypted data length: {len(encrypted_data)} bytes")
                    break
                except UnicodeDecodeError:
                    print("Failed to decode embedded password - possible corruption")
        
        # Always use embedded password if available
        if password_found:
            password = embedded_password
            print(f"Using embedded password from file: {password}")
        # Only use provided password if no embedded password was found
        elif not password:
            return jsonify({
                'status': 'error', 
                'message': 'No password provided or found in the file',
                'filename': filename
            }), 400
        
        # Check if we have any encrypted data
        if len(encrypted_data) < 1:  # Just check that we have some data
            print(f"DEBUG: No encrypted data found: {len(encrypted_data)} bytes")
            return jsonify({
                'status': 'error',
                'filename': filename,
                'message': "No valid encrypted data found. The file may not contain a hidden message.",
                'message_length': 0,
                'password_found': password_found,
                'used_password': password if password_found else None
            })
        
        # Try simple XOR decryption first for legacy/small messages
        try:
            print(f"DEBUG: Trying XOR decryption with password: {password[:2]}{'*' * (len(password) - 4)}{password[-2:] if len(password) > 2 else ''}")
            # Simple XOR encryption/decryption
            if isinstance(password, str):
                password_bytes = password.encode('utf-8')
            else:
                password_bytes = password
                
            key = hashlib.sha256(password_bytes).digest()
            decrypted = []
            for i, char in enumerate(encrypted_data):
                key_char = key[i % len(key)]
                decrypted_char = char ^ key_char
                decrypted.append(decrypted_char)
            
            decrypted_bytes = bytes(decrypted)
            
            # Try to convert to string
            try:
                decrypted_message = decrypted_bytes.decode('utf-8')
                # If it decodes as valid UTF-8, it's likely the correct message
                print(f"DEBUG: Successfully decoded message using XOR: {decrypted_message[:20]}...")
                
                return jsonify({
                    'status': 'success',
                    'filename': filename,
                    'message': decrypted_message,
                    'message_length': len(decrypted_message),
                    'password_found': password_found,
                    'used_password': password if password_found else None
                })
            except UnicodeDecodeError:
                # Not valid UTF-8, try AES decryption next
                print("DEBUG: XOR result not valid UTF-8, trying AES decryption")
                pass
                
            # Fall through to AES if the XOR result isn't valid UTF-8
        except Exception as e:
            print(f"DEBUG: XOR decryption failed: {str(e)}")
        
        # Try AES decryption if XOR didn't work
        try:
            # Only try AES if we have enough data
            if len(encrypted_data) >= 33:  # Need at least salt(16) + IV(16) + 1 byte
                print("DEBUG: Trying AES decryption")
                decrypted_message = utils.decrypt_message(encrypted_data, password)
                
                # Convert to string if it's bytes
                if isinstance(decrypted_message, bytes):
                    try:
                        message_str = decrypted_message.decode('utf-8')
                    except UnicodeDecodeError:
                        message_str = f"Binary data (could not decode as UTF-8): {decrypted_message.hex()[:50]}..."
                else:
                    message_str = str(decrypted_message)
                
                # Check if the decrypted message contains an error indication
                has_error = isinstance(message_str, str) and "error" in message_str.lower()
                
                return jsonify({
                    'status': 'warning' if has_error else 'success',
                    'filename': filename,
                    'message': message_str,
                    'message_length': len(message_str),
                    'password_found': password_found,
                    'used_password': password if password_found else None
                })
            else:
                # Not enough data for AES, and XOR didn't work
                return jsonify({
                    'status': 'error',
                    'filename': filename,
                    'message': "Not enough data for AES decryption and XOR decryption failed.",
                    'message_length': 0,
                    'password_found': password_found,
                    'used_password': password if password_found else None
                })
        except Exception as e:
            print(f"ERROR: AES Decryption failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'filename': filename,
                'message': f"Decryption error: {str(e)}",
                'message_length': 0,
                'password_found': password_found,
                'used_password': password if password_found else None
            })
    
    except Exception as e:
        print(f"Error in decryption process: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file from the output folder"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Return the capabilities of the API"""
    capabilities = {
        'image_steganography': hasattr(utils, 'hide_data_in_image'),
        'audio_steganography': hasattr(utils, 'hide_data_in_audio'),
        'audio_conversion': hasattr(utils, 'convert_audio_to_wav'),
        'image_conversion': hasattr(utils, 'convert_and_hide_in_image'),
        'supports_jpg_jpeg': hasattr(utils, 'convert_and_hide_in_image'),
        'supports_png': hasattr(utils, 'hide_data_in_image'),
        'supports_bmp': hasattr(utils, 'hide_data_in_image'),
        'supports_gif': hasattr(utils, 'convert_and_hide_in_image')
    }
    return jsonify(capabilities)

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 