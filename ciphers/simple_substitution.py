from PyQt6.QtWidgets        import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout


class SimpleSubWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("Simple Substitution")
        self.setGeometry(150, 150, 200, 150)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Hello from the new window!"))
        self.setLayout(layout)