import os
import sys
import utils
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Test QR code steganography')
    parser.add_argument('--action', choices=['generate', 'encrypt', 'decrypt'], required=True,
                        help='Action to perform: generate, encrypt, or decrypt')
    parser.add_argument('--data', help='Data to encode in QR code (for generate action)')
    parser.add_argument('--message', help='Message to hide in QR code (for encrypt action)')
    parser.add_argument('--password', help='Password for encryption/decryption')
    parser.add_argument('--input', help='Input QR code file path (for decrypt action)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--style', choices=['standard', 'fancy', 'embedded'], default='standard',
                      help='QR code style (for encrypt action)')
    parser.add_argument('--background', help='Background image path (for encrypt action)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir:  # Only create directory if there's a path specified
            os.makedirs(output_dir, exist_ok=True)
    
    # Ensure the default output directory exists
    os.makedirs('output', exist_ok=True)
    
    if args.action == 'generate':
        if not args.data:
            print("Error: --data is required for generate action")
            return
            
        output_path = args.output or 'output/qr_code.png'
        print(f"Generating QR code with data: {args.data}")
        utils.generate_qr_code(args.data, output_path)
        print(f"QR code generated and saved to: {output_path}")
        
    elif args.action == 'encrypt':
        if not args.message:
            print("Error: --message is required for encrypt action")
            return
            
        # Auto-generate password if not provided
        password = args.password
        if not password:
            password = utils.generate_strong_password(16)
            print(f"Auto-generated password: {password}")
            
        output_path = args.output or 'output/encrypted_qr.png'
        
        print(f"Encrypting message: {args.message}")
        utils.hide_message_in_qr(
            args.message, 
            password, 
            output_path, 
            background_image=args.background, 
            style=args.style
        )
        print(f"Encrypted QR code generated and saved to: {output_path}")
        print(f"Use this password to decrypt: {password}")
        
    elif args.action == 'decrypt':
        if not args.input:
            print("Error: --input is required for decrypt action")
            return
            
        if not os.path.exists(args.input):
            print(f"Error: Input file {args.input} does not exist")
            return
            
        print(f"Decrypting QR code: {args.input}")
        message = utils.extract_message_from_qr(args.input, args.password)
        print(f"Decrypted message: {message}")
    
    else:
        print(f"Unknown action: {args.action}")

if __name__ == "__main__":
    main() 