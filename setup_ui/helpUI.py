from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox, QFileDialog
from PyQt6                          import QtWidgets, QtCore, QtGui
from PyQt6.QtCore                   import QProcess, QObject, pyqtSignal
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
from pathlib                        import Path
import os, pgpy, sys, warnings
class HelpPageUI:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_help_ui()

    def setup_help_ui(self):
        """Set up the help page, label, and content."""
        self.HelpPage = QtWidgets.QWidget(parent=self.parent)
        self.HelpPage.setObjectName("HelpPage")

        self.HelpLabel = QtWidgets.QLabel(parent=self.HelpPage)
        self.HelpLabel.setGeometry(QtCore.QRect(10, -1, 1041, 51))
        self.HelpLabel.setText("Help")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.HelpLabel.setFont(font)
        self.HelpLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HelpLabel.setObjectName("HelpLabel")

        self.setup_help_page()
    
    def setup_help_page(self):
        self.how_to = DefaultQTextEditStyle(parent=self.HelpPage)
        self.how_to.setGeometry(20, 100, 450, 450)
        self.how_to.setReadOnly(True)
        self.how_to.setHtml(""" <h3>About this project</h3>
        <p>This Python PyQt6 GUI app gives the opportunity to Cryptography enthusiasts, to explore and learn
        (in a friendly environment) various concepts about Cryptanalysis and Cryptography in general.</p>
        <p>You can test various tools used in cryptography and learn their purpose in the world of security and hiding information.
        From simple ciphers to key generation and secure file transfer, you can dive into how cryptography tools operate.</p>
        <p>Each section has a question mark icon, which provides information about the section and its tools. Therefore, each tool
        has exactly the same button, which gives information and instructions about how to use the specific tool.</p>
        <p>Be careful tho, do not use sensitive information/messages in any of the encryption/decryption tools provided.
        You are here because you want to learn and explore the world of cryptography and cryptanalysis. Use the tools carefully and 
        under consideration.</p>""")

        self.about_the_app_textedit = DefaultQTextEditStyle(placeholder_text="blah blah welcome", parent=self.HelpPage)
        self.about_the_app_textedit.setGeometry(560, 100, 450, 450)
        self.about_the_app_textedit.setReadOnly(True)
        self.about_the_app_textedit.setHtml("""<h3>A few words</h3>
        <p>The terms cryptography and cryptanalysis are related but not identical. <b>Cryptology</b> is the broader scientific study of secret communication, 
        which includes both cryptography and cryptanalysis. Both fields rely heavily on mathematics (number theory, algebra, probability).</p>
        <p><b>Cryptography</b> is the art and science of creating secure communication systems that prevent unauthorized access to information.
        It mainly deals with designing encryption algorithms and protocols to protect data, ensure integrity and authenticate users/messages.</p>
        <p><b>Cryptanalysis</b> is the science of analyzing (or breaking) cryptographic systems, to find weaknesses (or break) the security of 
        a cryptographic system. Some examples include: reverse or bypass encryption without the key, key recovery, plaintext recovery, identifying flaws,
        various attacks like brute force attack, side-channel attack etc.</p>
        <p><b>Cryptography</b> is like building a strong, secure lock while <b>Cryptanalysis</b> is like being a lockpicker trying to open it without the key</p>""")
