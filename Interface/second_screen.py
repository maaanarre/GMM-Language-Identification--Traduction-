# ... (imports)
from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget, QLabel,
    QScrollArea, QComboBox, QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt

from inference_pipeline import inference
from language_detection import detect_language


class SecondScreen(QWidget):
    def __init__(self, stacked_widget, third_screen):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.third_screen = third_screen
        self.audio_path = None
        self.detected_lang = None

        # === Background ===
        self.setAutoFillBackground(True)
        palette = QPalette()
        background = QPixmap("background.jpg")  # Remplace par ton image
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)))
        self.setPalette(palette)

        # === Scroll area ===
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # === Title ===
        self.title_label = QLabel("🌍 GlobalVoice")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(self.title_label)

        # === Language detected ===
        self.language_label = QLabel()
        self.language_label.setTextFormat(Qt.TextFormat.RichText)
        self.language_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.language_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.language_label)

        # === Target language selection ===
        self.language_select_label = QLabel("Select Target Language:")
        self.language_select_label.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: bold;
                color: #4fd1c5;
            }
        """)
        layout.addWidget(self.language_select_label)

        self.language_combobox = QComboBox()
        self.language_combobox.setStyleSheet("""
            QComboBox {
                font-size: 15px;
                padding: 8px;
                color: #1a202c;
                background-color: #edf2f7;
                border: 1px solid #4fd1c5;
                border-radius: 6px;
            }
            QComboBox:hover {
                background-color: #e0f7fa;
            }
        """)
        self.language_combobox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.languages = {
            "Arabic": "ar",
            "Darija": "ar",
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "Korean": "ko",
        }
        self.language_combobox.addItems(self.languages.keys())
        layout.addWidget(self.language_combobox)

        # === Translate Button ===
        translate_button = QPushButton("Translate →")
        translate_button.clicked.connect(self.translate_text)
        translate_button.setStyleSheet("""
            QPushButton {
                background-color: #4fd1c5;
                color: #1a202c;
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #38b2ac;
            }
            QPushButton:pressed {
                background-color: #2c7a7b;
                color: white;
            }
        """)
        layout.addWidget(translate_button)

        # === Back Button ===
        main_button = QPushButton("← Back to Main Screen")
        main_button.clicked.connect(self.go_to_main_screen)
        main_button.setStyleSheet("""
            QPushButton {
                background-color: #4fd1c5;
                color: #1a202c;
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #38b2ac;
            }
            QPushButton:pressed {
                background-color: #2c7a7b;
                color: white;
            }
        """)
        layout.addWidget(main_button)

        scroll_area.setWidget(content_widget)

        # === Main layout ===
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

    def go_to_main_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def start_prediction(self, audio_path):
        self.audio_path = audio_path
        lang_prediction = detect_language(self.audio_path)
        self.detected_lang = lang_prediction

        print("language detected :", lang_prediction)

        self.language_label.setText(
            f'<span style="color: #4fd1c5; font-weight: bold;">Language detected:</span> '
            f'<span style="color: white;">{lang_prediction}</span>'
        )

    def translate_text(self):
        try:
            if not self.audio_path or not self.detected_lang:
                raise ValueError("Audio path or detected language is missing.")

            dest_lang_name = self.language_combobox.currentText()
            dest_lang = self.languages[dest_lang_name]

            result = inference(self.audio_path, self.detected_lang, dest_lang)

            self.third_screen.set_audio_and_texts(
                original_audio=self.audio_path,
                translated_audio=result["tts_path"],
                original_text=result["transcription"],
                translated_text=result["translation"]
            )

            self.stacked_widget.setCurrentIndex(2)

        except Exception as e:
            print(f"[❌ ERROR] {e}")
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue :\n{e}")
