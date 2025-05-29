import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from first_screen import FirstScreen
from second_screen import SecondScreen
from third_screen import ThirdScreen  #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Synthesis")
        self.setGeometry(310, 70, 800, 586)

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()

        # Create the screens
        self.third_screen = ThirdScreen(self.stacked_widget)  # 👈 Ajouter ThirdScreen d'abord
        self.second_screen = SecondScreen(self.stacked_widget, self.third_screen)  # 👈 On passe third_screen
        self.main_screen = FirstScreen(self.stacked_widget)

        # Add screens to the QStackedWidget
        self.stacked_widget.addWidget(self.main_screen)     # index 0
        self.stacked_widget.addWidget(self.second_screen)   # index 1
        self.stacked_widget.addWidget(self.third_screen)    # index 2

        # Set the QStackedWidget as the central widget
        self.setCentralWidget(self.stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
