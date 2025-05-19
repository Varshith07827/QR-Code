# QR Code Generator and Reader

A simple Python application that allows you to generate and read QR codes using a graphical user interface.

## Features

### QR Code Generator
- Generate QR codes from text or URLs
- Save QR codes as PNG images
- Modern and user-friendly interface

### QR Code Reader
- Read QR codes from your computer's camera
- Read QR codes from image files
- Real-time QR code detection
- Display decoded information

## Requirements

- Python 3.7 or higher
- Required packages (install using `pip install -r requirements.txt`):
  - qrcode
  - pillow
  - opencv-python
  - pyzbar

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### QR Code Generator
Run the generator:
```bash
python qr_generator.py
```

1. Enter the text or URL you want to encode
2. Click "Generate QR Code"
3. Click "Save QR Code" to save the generated QR code

### QR Code Reader
Run the reader:
```bash
python qr_reader.py
```

1. Choose between reading from camera or file
2. For camera:
   - Click "Read from Camera" to start
   - Point your camera at a QR code
   - Click "Stop Camera" when done
3. For file:
   - Click "Read from File"
   - Select an image containing a QR code

## Notes

- The QR codes are saved in a `qr_codes` directory
- Make sure you have a working webcam for the camera feature
- The application supports common image formats (PNG, JPG, JPEG, BMP, GIF)

## License

This project is open source and available under the MIT License. 