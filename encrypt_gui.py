import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, 
                             QComboBox, QMessageBox, QProgressBar, QGroupBox, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import utils

class EncryptionThread(QThread):
    """Thread for handling encryption and steganography operations"""
    progress_update = pyqtSignal(int)
    operation_complete = pyqtSignal(str, str)  # output_path, password_file_path
    error_occurred = pyqtSignal(str)

    def __init__(self, message, password, media_path, media_type, output_path, auto_generate_password=False):
        super().__init__()
        self.message = message
        self.password = password
        self.media_path = media_path
        self.media_type = media_type
        self.output_path = output_path
        self.auto_generate_password = auto_generate_password
        self.password_file_path = None

    def run(self):
        try:
            # Generate a password if auto-generate is enabled
            if self.auto_generate_password:
                self.password = utils.generate_strong_password()
                self.password_file_path = utils.save_password_to_file(self.password, self.output_path)
            
            # Encrypt the message
            self.progress_update.emit(25)
            encrypted_data = utils.encrypt_message(self.message, self.password)
            self.progress_update.emit(50)
            
            # Hide the encrypted data in the media
            if self.media_type == "Image":
                utils.hide_data_in_image(self.media_path, encrypted_data, self.output_path)
            elif self.media_type == "Audio":
                utils.hide_data_in_audio(self.media_path, encrypted_data, self.output_path)
            elif self.media_type == "Video":
                utils.hide_data_in_video(self.media_path, encrypted_data, self.output_path)
            
            self.progress_update.emit(100)
            self.operation_complete.emit(self.output_path, self.password_file_path)
        except Exception as e:
            self.error_occurred.emit(str(e))

class EncryptionApp(QMainWindow):
    """Main application window for the encryption GUI"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Message Encryption & Steganography")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header_label = QLabel("Secure Message Hiding Tool")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Create form layout
        form_group = QGroupBox("Input Information")
        form_layout = QVBoxLayout()
        
        # Message input
        message_label = QLabel("Enter your secret message:")
        self.message_input = QTextEdit()
        form_layout.addWidget(message_label)
        form_layout.addWidget(self.message_input)
        
        # Password section
        password_section = QVBoxLayout()
        
        # Auto-generate password option
        self.auto_generate_password = QCheckBox("Auto-generate secure password (recommended)")
        self.auto_generate_password.setChecked(True)
        self.auto_generate_password.stateChanged.connect(self.toggle_password_input)
        password_section.addWidget(self.auto_generate_password)
        
        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Or enter your own password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setEnabled(False)  # Initially disabled since auto-generate is checked
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_section.addLayout(password_layout)
        
        form_layout.addLayout(password_section)
        
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
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        # Process button
        self.process_btn = QPushButton("Encrypt & Hide Message")
        self.process_btn.clicked.connect(self.process_encryption)
        self.process_btn.setEnabled(False)  # Disable until a file is selected
        main_layout.addWidget(self.process_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Initialize variables
        self.media_path = None
        self.output_path = None
    
    def toggle_password_input(self, state):
        """Enable or disable manual password input based on checkbox state"""
        self.password_input.setEnabled(not state)
        if state:
            self.password_input.clear()
        
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
                    "The application will convert it to PNG format during processing, but some image quality may be affected."
                )
            # Check if the file is a non-WAV audio format
            elif media_type == "Audio" and not file_path.lower().endswith('.wav'):
                QMessageBox.information(
                    self, "Audio Format Conversion",
                    "You selected a non-WAV audio file. The application will automatically convert it to WAV format "
                    "since WAV is required for audio steganography.\n\n"
                    "This requires FFmpeg to be installed on your system."
                )
            
            self.media_path = file_path
            self.media_path_label.setText(os.path.basename(file_path))
            self.process_btn.setEnabled(True)
    
    def process_encryption(self):
        """Process the encryption and steganography operation"""
        # Validate inputs
        message = self.message_input.toPlainText()
        auto_generate = self.auto_generate_password.isChecked()
        password = "" if auto_generate else self.password_input.text()
        
        if not message:
            QMessageBox.warning(self, "Input Error", "Please enter a message to encrypt.")
            return
        
        if not auto_generate and not password:
            QMessageBox.warning(self, "Input Error", "Please enter an encryption password or use auto-generate.")
            return
        
        if not self.media_path:
            QMessageBox.warning(self, "Input Error", "Please select a media file.")
            return
        
        # Get output file path
        media_type = self.media_type_combo.currentText()
        file_extension = os.path.splitext(self.media_path)[1]
        output_dir = os.path.dirname(self.media_path)
        
        # Force PNG format for images due to steganography requirements
        if media_type == "Image":
            file_extension = ".png"
            filter_str = "PNG Files (*.png)"
        else:
            filter_str = f"{media_type} Files (*{file_extension})"
        
        output_file = os.path.join(output_dir, f"stego_output{file_extension}")
        
        # Get save file location
        self.output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Output File", output_file, filter_str
        )
        
        if not self.output_path:
            return  # User cancelled
        
        # Force PNG extension for images
        if media_type == "Image" and not self.output_path.lower().endswith('.png'):
            self.output_path += '.png'
            QMessageBox.information(self, "Format Changed", 
                                  "The output format has been changed to PNG for reliable steganography.\n"
                                  "JPEG/JPG formats use lossy compression which destroys hidden data.")
        
        # Disable UI elements during processing
        self.process_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.status_label.setText("Processing... Please wait")
        
        # Start encryption thread
        self.encrypt_thread = EncryptionThread(
            message, password, self.media_path, 
            media_type, self.output_path, auto_generate
        )
        self.encrypt_thread.progress_update.connect(self.update_progress)
        self.encrypt_thread.operation_complete.connect(self.encryption_complete)
        self.encrypt_thread.error_occurred.connect(self.encryption_error)
        self.encrypt_thread.start()
    
    def update_progress(self, value):
        """Update the progress bar value"""
        self.progress_bar.setValue(value)
    
    def encryption_complete(self, output_path, password_file_path):
        """Handle completion of encryption operation"""
        self.status_label.setText(f"Encryption complete! Output saved to: {os.path.basename(output_path)}")
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        
        message = f"Message successfully encrypted and hidden in the media file.\n\nSaved to: {output_path}"
        
        if password_file_path:
            message += f"\n\nPassword saved to: {password_file_path}\n\nIMPORTANT: Keep this password file secure. You will need it for decryption."
        
        QMessageBox.information(self, "Operation Complete", message)
    
    def encryption_error(self, error_message):
        """Handle encryption error"""
        self.status_label.setText(f"Error: {error_message}")
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        
        QMessageBox.critical(
            self, "Operation Failed", 
            f"An error occurred during processing:\n\n{error_message}"
        )

def main():
    app = QApplication(sys.argv)
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 