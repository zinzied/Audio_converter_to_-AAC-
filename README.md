## Audio Converter to AAC

This Python script provides a graphical user interface (GUI) for converting audio files to AAC format and burning them to a CD/DVD. The application is built using PyQt5 and utilizes FFmpeg for audio conversion and ImgBurn for burning files to a disc.

### Features

- **Select Input and Output Folders**: Choose the folders containing the audio files to be converted and the destination folder for the converted files.
- **Convert Audio Files**: Convert audio files in the selected input folder to AAC format.
- **Add Files Manually**: Add additional files manually to be burned to the disc.
- **Burn Files**: Burn the converted and manually added files to a CD/DVD using ImgBurn.

### Requirements

- Python 3.x
- PyQt5
- FFmpeg
- ImgBurn (for burning files to a CD/DVD)

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/audioconverter.git
    cd audioconverter
    ```

2. **Install the required Python packages**:
    ```sh
    pip install PyQt5
    ```

3. **Install FFmpeg**:
    - Download and install FFmpeg from [FFmpeg official website](https://ffmpeg.org/download.html).
    - Ensure FFmpeg is added to your system's PATH.

4. **Install ImgBurn**:
    - Download and install ImgBurn from [ImgBurn official website](http://www.imgburn.com/).

### Usage

1. **Run the script**:
    ```sh
    python audioconverter.py
    ```

2. **Select Input Folder**: Click on "Select Input Folder" to choose the folder containing the audio files you want to convert.

3. **Select Output Folder**: Click on "Select Output Folder" to choose the destination folder for the converted files.

4. **Convert Files**: Click on "Convert Files" to start the conversion process. The status of the conversion will be displayed in the terminal output section.

5. **Add Files Manually**: Click on "Add Files Manually" to add additional files to be burned to the disc.

6. **Burn Files**: Click on "Burn Files" to start the burning process. Ensure that ImgBurn is installed and the CD/DVD drive is ready.

### Example

![image](https://github.com/user-attachments/assets/5ea051f6-19bc-400d-b549-d222a8b8f822)


### Credits

Created by [Zied Boughdir](https://github.com/zinzied)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

