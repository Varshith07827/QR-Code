import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QFileDialog,
                            QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from pyzbar.pyzbar import decode

class QRCodeReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Reader - PyQt5")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QLabel {
                font-size: 14px;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("QR Code Reader")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1976D2;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Camera button
        self.camera_button = QPushButton("Start Camera")
        self.camera_button.clicked.connect(self.toggle_camera)
        button_layout.addWidget(self.camera_button)

        # File button
        self.file_button = QPushButton("Open File")
        self.file_button.clicked.connect(self.read_from_file)
        button_layout.addWidget(self.file_button)

        layout.addLayout(button_layout)

        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("""
            background-color: white;
            border: 2px solid #2196F3;
            border-radius: 4px;
        """)
        layout.addWidget(self.image_label)

        # Result display
        self.result_label = QLabel("Result will appear here")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            background-color: white;
            padding: 10px;
            border: 2px solid #2196F3;
            border-radius: 4px;
            font-size: 14px;
        """)
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        # Initialize camera variables
        self.camera = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera)
        self.is_camera_active = False

    def toggle_camera(self):
        if self.is_camera_active:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("Failed to open camera")
            
            self.is_camera_active = True
            self.camera_button.setText("Stop Camera")
            self.timer.start(30)  # Update every 30ms
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start camera: {str(e)}")

    def stop_camera(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.is_camera_active = False
        self.camera_button.setText("Start Camera")
        self.timer.stop()
        self.image_label.clear()
        self.result_label.setText("Result will appear here")

    def update_camera(self):
        if not self.is_camera_active:
            return

        ret, frame = self.camera.read()
        if ret:
            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Decode QR codes
            decoded_objects = decode(frame_rgb)
            
            # Draw rectangles around QR codes
            for obj in decoded_objects:
                points = obj.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(
                        np.array([point for point in points], dtype=np.float32)
                    )
                    cv2.polylines(frame_rgb, [hull], True, (0, 255, 0), 2)
                else:
                    cv2.polylines(
                        frame_rgb,
                        [np.array(points, dtype=np.int32)],
                        True,
                        (0, 255, 0),
                        2
                    )

                # Display decoded data
                data = obj.data.decode('utf-8')
                self.result_label.setText(f"Detected: {data}")

            # Convert to QImage
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(
                frame_rgb.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_RGB888
            )
            
            # Scale image to fit label while maintaining aspect ratio
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Update label
            self.image_label.setPixmap(scaled_pixmap)

    def read_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*.*)"
        )

        if not file_path:
            return

        try:
            # Read image
            image = cv2.imread(file_path)
            if image is None:
                raise Exception("Failed to read image")

            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Decode QR codes
            decoded_objects = decode(image_rgb)
            
            if not decoded_objects:
                QMessageBox.information(self, "Info", "No QR code found in the image")
                return

            # Display results
            results = []
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                results.append(data)

            # Update result label
            self.result_label.setText("Detected:\n" + "\n".join(results))

            # Display image
            height, width, channel = image_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(
                image_rgb.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_RGB888
            )
            
            # Scale image to fit label while maintaining aspect ratio
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Update label
            self.image_label.setPixmap(scaled_pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read QR code: {str(e)}")

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeReader()
    window.show()
    sys.exit(app.exec_()) 