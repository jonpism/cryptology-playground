from PyQt6.QtWidgets    import (QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit)
from PyQt6.QtCore       import QProcess
from PyQt6.QtGui        import QFont, QColor, QPalette
import sys, os

class TerminalWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Terminal")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Consolas", 10))
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Base, QColor("black"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#00FF00"))
        self.output_area.setPalette(palette)
        self.layout.addWidget(self.output_area)

        # input area
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("Consolas", 10))
        self.input_line.setPlaceholderText("Type command here...")
        self.input_line.setStyleSheet("background-color: black; color: #00FF00; border: 1px solid #333;")
        self.input_line.returnPressed.connect(self.run_command)
        self.layout.addWidget(self.input_line)

        self.input_line.setFocus()

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        
        self.output_area.appendPlainText(f">>> Terminal initialized at: {os.getcwd()}")

    def run_command(self):
        command = self.input_line.text().strip()
        if not command:
            return

        self.output_area.appendPlainText(f"$ {command}")
        self.input_line.clear()

        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                os.chdir(path)
                self.output_area.appendPlainText(f"Directory changed to: {os.getcwd()}")
            except FileNotFoundError:
                self.output_area.appendPlainText(f"Error: Cannot find the path specified: {path}")
            return

        if command.lower() in ["cls", "clear"]:
            self.output_area.clear()
            return

        if sys.platform == "win32": # windows
            # cmd.exe /C for internal commands
            self.process.start("cmd.exe", ["/C", command])
        else:
            # mac and linux: /bin/bash -c
            self.process.start("/bin/bash", ["-c", command])

    def handle_output(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8", errors="ignore")
        self.output_area.insertPlainText(stdout)
        
        scrollbar = self.output_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
