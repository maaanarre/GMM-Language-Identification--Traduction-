from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

class ThirdScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.original_audio_path = None
        self.translated_audio_path = None

        # === Fond noir ===
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#121212"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)

        # Titre principal en turquoise
        title = QLabel("🌍 GlobalVoice")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: #4fd1c5;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Layout horizontal pour boutons et textes
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Partie gauche (Original audio + transcription)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        self.play_original_button = QPushButton("🔊 Play Original Audio")
        self.play_original_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_original_button.setStyleSheet(self.turquoise_button_style())
        self.play_original_button.clicked.connect(self.play_original_audio)
        left_layout.addWidget(self.play_original_button)

        self.original_text = QTextEdit()
        self.original_text.setPlaceholderText("Original speech-to-text transcription...")
        self.original_text.setReadOnly(True)
        self.original_text.setStyleSheet(self.dark_textedit_style())
        self.original_text.setFont(QFont("Segoe UI", 14))
        left_layout.addWidget(self.original_text)

        content_layout.addLayout(left_layout)

        # Partie droite (Translated audio + traduction)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        self.play_translated_button = QPushButton("🔊 Play Generated Audio")
        self.play_translated_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_translated_button.setStyleSheet(self.turquoise_button_style())
        self.play_translated_button.clicked.connect(self.play_translated_audio)
        right_layout.addWidget(self.play_translated_button)

        self.translated_text = QTextEdit()
        self.translated_text.setPlaceholderText("Translated text will appear here...")
        self.translated_text.setReadOnly(True)
        self.translated_text.setStyleSheet(self.dark_textedit_style())
        self.translated_text.setFont(QFont("Segoe UI", 14))
        right_layout.addWidget(self.translated_text)

        content_layout.addLayout(right_layout)

        layout.addLayout(content_layout)

        # Bouton retour turquoise avec contour blanc
        back_button = QPushButton("← Back")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4fd1c5;
                border: 2px solid #4fd1c5;
                border-radius: 20px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 18px;
                max-width: 140px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #4fd1c5;
                color: #121212;
            }
            QPushButton:pressed {
                background-color: #3bb6b1;
                color: #0f0f0f;
            }
        """)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # === Audio Players ===
        self.audio_output = QAudioOutput()
        self.audio_player = QMediaPlayer()
        self.audio_player.setAudioOutput(self.audio_output)

    def turquoise_button_style(self):
        return """
            QPushButton {
                background-color: #4fd1c5;
                color: #121212;
                font-weight: bold;
                border-radius: 20px;
                padding: 14px 30px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #3bb6b1;
            }
            QPushButton:pressed {
                background-color: #329995;
            }
        """

    def dark_textedit_style(self):
        return """
            QTextEdit {
                background-color: #1e1e1e;
                border-radius: 15px;
                padding: 14px;
                color: #eeeeee;  /* Texte blanc cassé */
                border: 2px solid #4fd1c5;
            }
            QTextEdit:focus {
                border: 2px solid #7ae3e0;
                background-color: #262626;
            }
        """

    def set_audio_and_texts(self, original_audio, translated_audio, original_text, translated_text):
        self.original_audio_path = original_audio
        self.translated_audio_path = translated_audio
        self.original_text.setText(original_text)
        self.translated_text.setText(translated_text)

    def play_original_audio(self):
        if self.original_audio_path and os.path.exists(self.original_audio_path):
            url = QUrl.fromLocalFile(self.original_audio_path)
            self.audio_player.setSource(url)
            self.audio_player.play()

    def play_translated_audio(self):
        if self.translated_audio_path and os.path.exists(self.translated_audio_path):
            url = QUrl.fromLocalFile(self.translated_audio_path)
            self.audio_player.setSource(url)
            self.audio_player.play()

    def go_back(self):
        self.stacked_widget.setCurrentIndex(1)
