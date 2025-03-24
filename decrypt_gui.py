import sys
import os
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, 
                             QComboBox, QMessageBox, QProgressBar, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import utils

class DecryptionThread(QThread):
    """Thread for handling decryption and extraction operations"""
    progress_update = pyqtSignal(int)
    operation_complete = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, media_path, media_type, password):
        super().__init__()
        self.media_path = media_path
        self.media_type = media_type
        self.password = password

    def run(self):
        try:
            # Extract hidden data from media
            self.progress_update.emit(25)
            
            if self.media_type == "Image":
                encrypted_data = utils.extract_data_from_image(self.media_path)
            elif self.media_type == "Audio":
                encrypted_data = utils.extract_data_from_audio(self.media_path)
            elif self.media_type == "Video":
                encrypted_data = utils.extract_data_from_video(self.media_path)
            
            self.progress_update.emit(50)
            
            # Decrypt the extracted data
            decrypted_message = utils.decrypt_message(encrypted_data, self.password)
            
            self.progress_update.emit(100)
            self.operation_complete.emit(decrypted_message)
        except Exception as e:
            self.error_occurred.emit(str(e))

class DecryptionApp(QMainWindow):
    """Main application window for the decryption GUI"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Message Decryption & Extraction")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header_label = QLabel("Secret Message Extraction Tool")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Create form layout
        form_group = QGroupBox("Input Information")
        form_layout = QVBoxLayout()
        
        # Media type selection
        media_type_layout = QHBoxLayout()
        media_type_label = QLabel("Select media type:")
        self.media_type_combo = QComboBox()
        self.media_type_combo.addItems(["Image", "Audio", "Video"])
        media_type_layout.addWidget(media_type_label)
        media_type_layout.addWidget(self.media_type_combo)
        form_layout.addLayout(media_type_layout)
        
        # Media file selection
        media_file_layout = QHBoxLayout()
        self.media_path_label = QLabel("No media file selected")
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_media)
        media_file_layout.addWidget(self.media_path_label)
        media_file_layout.addWidget(self.browse_btn)
        form_layout.addLayout(media_file_layout)
        
        # Password section
        password_section = QVBoxLayout()
        
        # Password input layout
        password_layout = QHBoxLayout()
        password_label = QLabel("Enter decryption password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_section.addLayout(password_layout)
        
        # Password file button
        password_file_layout = QHBoxLayout()
        self.password_file_label = QLabel("Or load password from file:")
        self.password_file_btn = QPushButton("Load Password File...")
        self.password_file_btn.clicked.connect(self.load_password_file)
        password_file_layout.addWidget(self.password_file_label)
        password_file_layout.addWidget(self.password_file_btn)
        password_section.addLayout(password_file_layout)
        
        form_layout.addLayout(password_section)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        # Process button
        self.process_btn = QPushButton("Extract & Decrypt Message")
        self.process_btn.clicked.connect(self.process_decryption)
        self.process_btn.setEnabled(False)  # Disable until a file is selected
        main_layout.addWidget(self.process_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Result group
        result_group = QGroupBox("Extracted Message")
        result_layout = QVBoxLayout()
        
        # Message output
        self.message_output = QTextEdit()
        self.message_output.setReadOnly(True)
        result_layout.addWidget(self.message_output)
        
        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Initialize variables
        self.media_path = None
    
    def load_password_file(self):
        """Load password from a text file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Password File", "", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Try to extract the password using regex
                password_match = re.search(r"Encryption Password: (.*?)(?:\n|$)", content)
                
                if password_match:
                    password = password_match.group(1).strip()
                    self.password_input.setText(password)
                    self.status_label.setText(f"Password loaded from file: {os.path.basename(file_path)}")
                else:
                    QMessageBox.warning(
                        self, "Invalid Password File", 
                        "Could not find a valid password in the selected file."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error Reading File", 
                    f"Could not read the password file:\n\n{str(e)}"
                )
        
    def browse_media(self):
        """Open file dialog to select media file"""
        media_type = self.media_type_combo.currentText()
        file_filter = ""
        
        if media_type == "Image":
            file_filter = "Image Files (*.png *.jpg *.jpeg *.bmp)"
        elif media_type == "Audio":
            file_filter = "Audio Files (*.wav *.mp3 *.aac *.flac *.ogg *.m4a)"
        elif media_type == "Video":
            file_filter = "Video Files (*.mp4 *.avi)"
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Media File", "", file_filter)
        
        if file_path:
            # Check if the file is JPEG/JPG format
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                QMessageBox.warning(
                    self, "JPEG Format Warning",
                    "You selected a JPEG/JPG file which is not optimal for steganography due to lossy compression.\n\n"
                    "This may result in failure to extract the hidden message.\n\n"
                    "PNG format is strongly recommended for reliable steganography."
                )
            # Check if the file is a non-WAV audio format
            elif media_type == "Audio" and not file_path.lower().endswith('.wav'):
                QMessageBox.warning(
                    self, "Audio Format Warning",
                    "You selected a non-WAV audio file. The application will automatically convert it to WAV format.\n\n"
                    "However, if this isn't the original file with hidden data, conversion may not recover the message.\n\n"
                    "Only use the original WAV file that was produced during the encryption process."
                )
            
            self.media_path = file_path
            self.media_path_label.setText(os.path.basename(file_path))
            self.process_btn.setEnabled(True)
            
            # Try to automatically locate a corresponding password file
            password_file = os.path.splitext(file_path)[0] + "_password.txt"
            if os.path.exists(password_file):
                self.status_label.setText(f"Found matching password file. Click 'Load Password File' to use it.")
    
    def process_decryption(self):
        """Process the decryption and extraction operation"""
        # Validate inputs
        password = self.password_input.text()
        
        if not password:
            QMessageBox.warning(self, "Input Error", "Please enter the decryption password or load it from a file.")
            return
        
        if not self.media_path:
            QMessageBox.warning(self, "Input Error", "Please select a media file.")
            return
        
        # Clear previous results
        self.message_output.clear()
        
        # Disable UI elements during processing
        self.process_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.status_label.setText("Processing... Please wait")
        
        # Start decryption thread
        media_type = self.media_type_combo.currentText()
        self.decrypt_thread = DecryptionThread(self.media_path, media_type, password)
        self.decrypt_thread.progress_update.connect(self.update_progress)
        self.decrypt_thread.operation_complete.connect(self.decryption_complete)
        self.decrypt_thread.error_occurred.connect(self.decryption_error)
        self.decrypt_thread.start()
    
    def update_progress(self, value):
        """Update the progress bar value"""
        self.progress_bar.setValue(value)
    
    def decryption_complete(self, message):
        """Handle completion of decryption operation"""
        self.status_label.setText("Decryption complete!")
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        
        # Display the decrypted message
        self.message_output.setText(message)
        
        if "Decryption error" in message:
            QMessageBox.warning(
                self, "Decryption Failed", 
                f"{message}\n\nThis could be due to:\n"
                "- Incorrect password\n"
                "- No hidden message in the file\n"
                "- Corrupted data or unsupported format"
            )
    
    def decryption_error(self, error_message):
        """Handle decryption error"""
        self.status_label.setText(f"Error: {error_message}")
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        
        QMessageBox.critical(
            self, "Operation Failed", 
            f"An error occurred during processing:\n\n{error_message}"
        )

def main():
    app = QApplication(sys.argv)
    window = DecryptionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 