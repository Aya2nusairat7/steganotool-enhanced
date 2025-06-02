import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QGroupBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import subprocess

class LauncherApp(QMainWindow):
    """Main launcher application to choose between encryption and decryption"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Steganography Tool")
        self.setGeometry(300, 300, 600, 400)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header_label = QLabel("Secure Steganography Tool")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Create description
        description = QLabel(
            "This application allows you to hide encrypted messages in various media types.\n"
            "Choose whether you want to hide a message or extract a hidden message."
        )
        description.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(description)
        
        # Create buttons layout
        buttons_group = QGroupBox("Select Operation")
        buttons_layout = QHBoxLayout()
        
        # Encrypt button
        self.encrypt_btn = QPushButton("Encrypt & Hide Message")
        self.encrypt_btn.setMinimumHeight(80)
        self.encrypt_btn.setFont(QFont("Arial", 12))
        self.encrypt_btn.clicked.connect(self.launch_encrypt)
        buttons_layout.addWidget(self.encrypt_btn)
        
        # Decrypt button
        self.decrypt_btn = QPushButton("Extract & Decrypt Message")
        self.decrypt_btn.setMinimumHeight(80)
        self.decrypt_btn.setFont(QFont("Arial", 12))
        self.decrypt_btn.clicked.connect(self.launch_decrypt)
        buttons_layout.addWidget(self.decrypt_btn)
        
        buttons_group.setLayout(buttons_layout)
        main_layout.addWidget(buttons_group)
        
        # Add author information
        author_label = QLabel("Advanced Security Application with Steganography & AES Encryption")
        author_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(author_label)
    
    def launch_encrypt(self):
        """Launch the encryption application"""
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        encrypt_script = os.path.join(script_dir, 'encrypt_gui.py')
        
        try:
            subprocess.Popen([sys.executable, encrypt_script])
        except Exception as e:
            print(f"Error launching encryption application: {str(e)}")
    
    def launch_decrypt(self):
        """Launch the decryption application"""
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        decrypt_script = os.path.join(script_dir, 'decrypt_gui.py')
        
        try:
            subprocess.Popen([sys.executable, decrypt_script])
        except Exception as e:
            print(f"Error launching decryption application: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = LauncherApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
