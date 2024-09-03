import webbrowser
import os
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

class ConversionThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, input_folder, output_folder):
        super().__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder

    def run(self):
        convert_files_in_folder(self.input_folder, self.output_folder, self.progress)
        self.finished.emit()

def convert_to_aac(input_file, output_file, progress_signal):
    try:
        # Run the FFmpeg command to convert the audio file to AAC format
        subprocess.run([
            'ffmpeg',
            '-i', input_file,        # Input file
            '-c:a', 'aac',           # Audio codec
            '-b:a', '192k',          # Bitrate
            output_file              # Output file
        ], check=True)
        progress_signal.emit(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        progress_signal.emit(f"Error during conversion: {e}")

def convert_files_in_folder(input_folder, output_folder, progress_signal):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)
        
        # Check if the file is an audio file (you can add more extensions if needed)
        if filename.lower().endswith(('.mp3', '.wav', '.flac', '.ogg')):
            output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.aac')
            convert_to_aac(input_file, output_file, progress_signal)

class AudioConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Audio Converter to AAC')
        self.resize(800, 600)  # Set the initial size of the window
        
        layout = QVBoxLayout()
        
        self.input_label = QLabel('Input Folder: Not selected')
        self.output_label = QLabel('Output Folder: Not selected')
        self.status_label = QLabel('')
        self.credit_label = QLabel('<a href="https://github.com/zinzied"><font color="blue">Created By Zied Boughdir</font></a>')
        self.credit_label.linkActivated.connect
        webbrowser.open('https://github.com/zinzied')
        
        self.input_button = QPushButton('Select Input Folder')
        self.input_button.clicked.connect(self.select_input_folder)
        
        self.output_button = QPushButton('Select Output Folder')
        self.output_button.clicked.connect(self.select_output_folder)
        
        self.convert_button = QPushButton('Convert Files')
        self.convert_button.clicked.connect(self.convert_files)
        
        self.add_files_button = QPushButton('Add Files Manually')
        self.add_files_button.clicked.connect(self.add_files)
        
        self.burn_button = QPushButton('Burn Files')
        self.burn_button.clicked.connect(self.burn_files)
        self.burn_button.setEnabled(False)  # Disable burn button initially
        
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_button)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.add_files_button)
        layout.addWidget(self.burn_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.terminal_output)
        layout.addWidget(self.credit_label)
        
        self.setLayout(layout)
        
        self.input_folder = None
        self.output_folder = None
        self.manual_files = []
        self.thread = None
    
    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')
        if folder:
            self.input_folder = folder
            self.input_label.setText(f'Input Folder: {folder}')
    
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        if folder:
            self.output_folder = folder
            self.output_label.setText(f'Output Folder: {folder}')
    
    def convert_files(self):
        if self.input_folder and self.output_folder:
            self.thread = ConversionThread(self.input_folder, self.output_folder)
            self.thread.progress.connect(self.update_status)
            self.thread.finished.connect(self.enable_burn_button)
            self.thread.start()
        else:
            self.status_label.setText('Please select both input and output folders.')
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select Files to Burn')
        if files:
            self.manual_files.extend(files)
            self.status_label.setText(f'{len(self.manual_files)} files added manually.')
            self.burn_button.setEnabled(True)
    
    def update_status(self, message):
        self.terminal_output.append(message)
    
    def enable_burn_button(self):
        self.burn_button.setEnabled(True)
        self.status_label.setText('Conversion complete. Ready to burn files.')
    
    def burn_files(self):
        if not self.output_folder and not self.manual_files:
            self.status_label.setText('No files to burn.')
            return
        
        try:
            # Create a temporary folder to hold all files to be burned
            temp_burn_folder = os.path.join(self.output_folder, 'burn_temp') if self.output_folder else 'burn_temp'
            os.makedirs(temp_burn_folder, exist_ok=True)
            
            # Copy converted files to the temporary burn folder
            if self.output_folder:
                for filename in os.listdir(self.output_folder):
                    file_path = os.path.join(self.output_folder, filename)
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, temp_burn_folder)
            
            # Copy manually added files to the temporary burn folder
            for file in self.manual_files:
                shutil.copy(file, temp_burn_folder)
            
            # Burn the files using ImgBurn
            subprocess.run([
                'C:\\Program Files (x86)\\ImgBurn\\ImgBurn.exe',
                '/MODE', 'BUILD',
                '/SRC', temp_burn_folder,
                '/DEST', 'F:\\',  # Assuming F: is the CD/DVD drive
                '/START',
                '/CLOSE'
            ], check=True)
            
            self.status_label.setText('Burning process started.')
        except subprocess.CalledProcessError as e:
            self.status_label.setText(f"Error during burning: {e}")

if __name__ == '__main__':
    app = QApplication([])
    window = AudioConverterApp()
    window.show()
    app.exec_()