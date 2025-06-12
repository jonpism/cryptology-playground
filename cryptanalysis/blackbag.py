from PyQt6.QtWidgets    import QWidget, QTextBrowser

class BlackBagCryptanalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Black Bag Cryptanalysis")
        self.setFixedSize(700, 300)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Black-bag cryptanalysis refers to the practice of gaining access "
        "to encrypted information by physically compromising the system rather than breaking "
        "the encryption mathematically. This typically involves covert operations like: "
        "<ul>"
        "<li><b>Physical Theft or Covert Entry: </b>Physically stealing a device, hard drive, or security token to extract cryptographic keys.</li>"
        "<li><b>Hardware Implants & Keyloggers: </b>Installing hidden hardware that captures passwords or encryption keys as they are entered "
        "(or trojan horse software or hardware installed on (or near to) target computers).</li>"
        "<li><b>Cold Boot Attacks: </b>Extracting encryption keys from RAM before data fades after a reboot.</li>"
        "<li><b>Side-Channel Attacks: </b>Monitoring power consumption, electromagnetic radiation, or acoustic signals to infer encryption keys.</li>"
        "<li><b>Social Engineering: </b>Tricking users into revealing passwords, using phishing or pretexting.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Black-bag_cryptanalysis'>Wikipedia</a><br>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
