from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont


class FirstScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        # Set the background image
        self.setAutoFillBackground(True)
        palette = QPalette()
        background = QPixmap("black.png")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)))
        self.setPalette(palette)

        # === Main Layout ===
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 80, 40, 80)

        # === Title Label ===
        self.title_label = QLabel("🌍 GlobalVoice")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(self.title_label)

        # === Description Label ===
        self.description_label = QLabel("A multilingual speech-to-speech translation system")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #4fd1c5;
            }
        """)
        layout.addWidget(self.description_label)

        # === Spacer ===
        layout.addSpacing(40)

        # === Upload Audio Button ===
        upload_button = QPushButton("Upload Audio")
        upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_button.setFixedSize(200, 50)
        upload_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4fd1c5;
                color: #1a202c;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #38b2ac;
            }
            QPushButton:pressed {
                background-color: #2c7a7b;
                color: white;
            }
        """)
        upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(upload_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setGeometry(100, 100, 600, 800)

    def open_file_dialog(self):
        try:
            # Open a file dialog to select audio files
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Audio File",
                "",
                "Audio Files (*.wav *.mp3 *.flac *.ogg);;All Files (*)",
            )

            if file_path:
                if self.is_audio_file(file_path):
                    print(f"Selected file path: {file_path}")
                    self.go_to_second_screen(file_path)
                else:
                    print("Invalid file type. Please select an audio file.")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def is_audio_file(file_path):
        audio_extensions = [".wav", ".mp3", ".flac", ".ogg"]
        return any(file_path.lower().endswith(ext) for ext in audio_extensions)

    def go_to_second_screen(self, file_path):
        self.stacked_widget.setCurrentIndex(1)
        second_screen = self.stacked_widget.currentWidget()
        second_screen.start_prediction(file_path)
