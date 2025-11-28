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
        self.process.finished.connect(self.process_finished)
        
        self.output_area.appendHtml(f'<span style="color: #00FF00;">>>> Terminal initialized at: {os.getcwd()}</span>')

    def run_command(self):
        command = self.input_line.text().strip()
        if not command:
            return

        cmd_html = f'<span style="color: #00FF00;">$ {command}</span><br>'
        self.output_area.appendHtml(cmd_html)
        self.input_line.clear()

        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                os.chdir(path)
                self.output_area.appendHtml(f'<span style="color: #00FF00;">Directory changed to: {os.getcwd()}</span><br>')
            except FileNotFoundError:
                self.output_area.appendHtml(f'<span style="color: #FF0000;">Error: Cannot find the path specified: {path}</span><br>')
            return

        if command.lower() in ["cls", "clear"]:
            self.output_area.clear()
            return
        
        self.process.setWorkingDirectory(os.getcwd())

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

    def process_finished(self):
        self.handle_output()