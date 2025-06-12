from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.qtextedit_style import DefaultQTextEditStyle

class HomePageUI:

    def __init__(self, parent=None):
        self.parent = parent
        self.setup_home_page_ui()

    def setup_home_page_ui(self):
        """Set up the home  page, label, and buttons."""
        self.HomePage = QtWidgets.QWidget(parent=self.parent)
        self.HomePage.setObjectName("HomePage")

        self.HomePageLabel = QtWidgets.QLabel(parent=self.HomePage)
        self.HomePageLabel.setGeometry(QtCore.QRect(10, 0, 1000, 51))
        self.HomePageLabel.setText("Home")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.HomePageLabel.setFont(font)
        self.HomePageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HomePageLabel.setObjectName("HomePageLabel")

        self.setup_home_page()
    
    def setup_home_page(self):
        self.welcome_textedit = DefaultQTextEditStyle(parent=self.HomePage)
        self.welcome_textedit.setGeometry(20, 100, 450, 450)
        self.welcome_textedit.setReadOnly(True)
        self.welcome_textedit.setHtml("""<p>This tool is a comprehensive, interactive environment for exploring and experimenting with:</p>
        <ul>
          <li><b>Classical & Modern Ciphers</b></li>
          <li><b>Hashing & Encoding Algorithms</b></li>
          <li><b>Asymmetric & Symmetric Encryption</b></li>
          <li><b>File Security Operations</b></li>
          <li><b>Entropy Testing & Key Generation</b></li>
        </ul>
        <p>Designed for students, enthusiasts, and professionals alike, Cryptology's Playground turns cryptographic concepts into hands-on learning.</p>""")

        self.about_the_app_textedit = DefaultQTextEditStyle(placeholder_text="blah blah welcome", parent=self.HomePage)
        self.about_the_app_textedit.setGeometry(560, 100, 450, 450)
        self.about_the_app_textedit.setReadOnly(True)
        self.about_the_app_textedit.setHtml("""<h4><i>Your Personal Crypto Lab</i></h4>
        <p>Tinker, test, and learn in a sandbox environment with no risk.<br>
        Designed with educational clarity and practical use in mind.<br>
        All tools are modular and instant, no need for command-line or complex setups.</p>

        <p>Explore the left-hand menu to get started. Hover over any tool to get a brief description.</p>

        <p style="color: #00ffcc;"><b>Ready to dive in?</b></p>""")
