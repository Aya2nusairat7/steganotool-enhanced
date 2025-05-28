# Troubleshooting Guide for Steganography Application

This guide will help you resolve common issues that may arise when using the steganography application.

## Installation Issues

### Python Environment Problems

**Issue**: `ModuleNotFoundError` or `ImportError` when running the application.

**Solution**:
1. Ensure you have activated the virtual environment:
   ```
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```
2. Verify all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```
3. Check Python version compatibility (Python 3.8+ recommended):
   ```
   python --version
   ```

### Flask Server Won't Start

**Issue**: Error when starting the Flask server.

**Solution**:
1. Check if another application is using port 8080:
   ```
   # On Windows
   netstat -ano | findstr :8080
   
   # On macOS/Linux
   lsof -i :8080
   ```
2. Terminate the conflicting process or change the port in `api.py`.
3. Ensure you have administrator/root privileges if needed.

## Encryption Issues

### "No file part" or "No selected file" Error

**Issue**: Error message when trying to encrypt a message.

**Solution**:
1. Ensure you've selected a valid media file.
2. Check if the file size exceeds the maximum allowed by your browser (typically around 50MB).
3. Try a different browser if the issue persists.

### "No message provided" Error

**Issue**: Error when trying to encrypt an empty message.

**Solution**:
1. Enter text in the message field.
2. If you need to hide an empty message (not recommended), use a space character.

### "No password provided and auto-generate not enabled" Error

**Issue**: Error when neither a password is provided nor auto-generate is enabled.

**Solution**:
1. Either enter a password in the password field, or
2. Check the "Auto-generate secure password" option.

### File Size Too Large After Encryption

**Issue**: The resulting file is significantly larger than expected.

**Solution**:
1. For image steganography, use PNG or BMP formats as they are lossless.
2. For audio steganography, use WAV format for the best results.
3. Be aware that the file size increase is proportional to the original file size, not the hidden message size, especially for audio files.

## Decryption Issues

### "No valid encrypted data found" Error

**Issue**: The application cannot find encrypted data in the file.

**Solution**:
1. Verify you're using the correct file that contains hidden data.
2. Check if you're specifying the correct media type (image/audio).
3. Ensure the file hasn't been modified, compressed, or converted after encryption.
4. Try using the file produced directly by the encryption process.

### Incorrect Password Error

**Issue**: The provided password doesn't work for decryption.

**Solution**:
1. Double-check the password for typos.
2. If the password was auto-generated, verify you have the exact password from the encryption process.
3. Remember that passwords are case-sensitive and include special characters exactly as shown.
4. If the file has an embedded password but isn't being detected, ensure the file hasn't been modified.

### Corrupted or Incomplete Decrypted Message

**Issue**: The decrypted message appears corrupted or incomplete.

**Solution**:
1. Verify the file hasn't been modified or damaged after encryption.
2. For image files, ensure no image editing or compression has been applied.
3. For audio files, ensure no audio processing or format conversion has been applied.
4. Try decrypting with the web interface if you were using the command line, or vice versa.

## Audio Steganography Specific Issues

### "Audio steganography not supported in this build" Error

**Issue**: Error when trying to use audio steganography.

**Solution**:
1. Ensure all dependencies for audio processing are installed:
   ```
   pip install pydub numpy wave
   ```
2. For MP3 support, install the required system libraries:
   ```
   # On Ubuntu/Debian
   apt-get install ffmpeg
   
   # On Windows
   # Download and install FFmpeg from https://ffmpeg.org/download.html
   ```

### Audio File Playback Issues After Encryption

**Issue**: Audio file doesn't play correctly after steganography.

**Solution**:
1. Use WAV format for the most reliable results.
2. Keep the hidden message as small as possible relative to the audio file size.
3. Some audio players may have issues with modified WAV files; try VLC media player which is more tolerant.
4. Be aware that audio quality might degrade slightly due to bit manipulation.

## Image Steganography Specific Issues

### "Image steganography not supported in this build" Error

**Issue**: Error when trying to use image steganography.

**Solution**:
1. Ensure Pillow (PIL) is installed:
   ```
   pip install Pillow
   ```
2. Use supported image formats (PNG, BMP, or GIF).

### Visible Artifacts in Image After Encryption

**Issue**: The encrypted image shows visible differences from the original.

**Solution**:
1. Use larger images with more pixels to reduce the visual impact.
2. Choose images with complex textures or high detail areas.
3. Keep the message size small relative to the image capacity.
4. Use PNG or BMP formats for the best quality.

## Compression Issues

### "Decompression error" Message

**Issue**: Error message about decompression failure during decryption.

**Solution**:
1. The encrypted data might be corrupted or incomplete. Ensure the file hasn't been modified.
2. Try using the exact file produced by the encryption process without any modifications.
3. If using an older version of the tool that doesn't support compression, update to the latest version.

### Poor Compression Ratio

**Issue**: Message doesn't compress well, leading to limited capacity for steganography.

**Solution**:
1. Text content generally compresses well; binary data may not compress efficiently.
2. Already compressed files (ZIP, JPEG, MP3, etc.) won't compress much further.
3. For large messages that don't compress well, consider:
   - Breaking the content into multiple smaller files
   - Using a larger carrier file
   - Pre-compressing binary data with specialized algorithms before using the tool

### "Memory Error" During Compression or Decompression

**Issue**: Application crashes with memory error when processing very large messages.

**Solution**:
1. Very large messages (>10MB) may cause memory issues during compression/decompression.
2. Try breaking the message into smaller chunks.
3. Close other applications to free up memory.
4. If possible, increase available RAM on your system.

## Web Interface Issues

### Interface Not Loading Properly

**Issue**: CSS or JavaScript not loading correctly.

**Solution**:
1. Clear your browser cache and reload the page.
2. Check browser console for specific errors (F12 in most browsers).
3. Ensure your browser has JavaScript enabled.
4. Try a different browser (Chrome, Firefox, or Edge recommended).

### Download Button Not Working

**Issue**: Unable to download the processed file.

**Solution**:
1. Check if the file was successfully generated (look for success message).
2. Ensure your browser allows downloads from the site.
3. Check the browser's download settings and permissions.
4. Try using the "right-click > Save link as" option on the download button.

## Command Line Client Issues

### Command Line Arguments Not Recognized

**Issue**: Error when providing arguments to `client.py`.

**Solution**:
1. Check the correct usage syntax:
   ```
   python client.py encrypt --file input.png --message "Secret message" --password "MyPassword"
   python client.py decrypt --file stego_input.png --password "MyPassword"
   ```
2. Ensure all required arguments are provided.
3. Use quotes around arguments that contain spaces.

### API Connection Issues

**Issue**: Command line client cannot connect to the API.

**Solution**:
1. Ensure the Flask server is running:
   ```
   python api.py
   ```
2. Check if the API URL in the client matches the server address (default: http://localhost:8080).
3. Verify there are no firewall or network issues blocking the connection.

## Advanced Troubleshooting

### Enable Debug Mode

For more detailed error information:

1. In `api.py`, ensure debug mode is enabled:
   ```python
   if __name__ == "__main__":
       app.run(debug=True, host="0.0.0.0", port=8080)
   ```
2. Run the application and check the console output for detailed error messages.

### Check Log Files

1. Look for error logs in the terminal/console where you started the application.
2. For web server errors, check your web server's error logs if you're hosting the application.

### Verify File Integrity

If you suspect a file has been corrupted:

1. Compare the file sizes before and after encryption.
2. Try encoding a simple test message in a new file to verify functionality.
3. Use the command line for more direct control and error reporting.

## Getting Help

If you're still experiencing issues:

1. Check the project documentation for updates or known issues.
2. Search for similar issues in the project's issue tracker.
3. Include the following information when seeking help:
   - Error messages (exact text)
   - Steps to reproduce the issue
   - File formats and sizes involved
   - Operating system and Python version
   - Whether you're using the web interface or command line 