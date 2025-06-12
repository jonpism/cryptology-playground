from PyQt6.QtWidgets    import QWidget, QTextBrowser

class PowerAnalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Power Analysis")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Power Analysis is a type of side-channel attack that exploits variations "
        "in the power consumption of a cryptographic device, like a smartcard, CPU, or other hardware, during "
        "cryptographic operations (such as encryption or decryption). The goal is to extract sensitive information "
        "like cryptographic keys by analyzing how the device's power usage changes while performing operations. "
        "This method of attack is powerful because it doesn't require access to the device's internal memory or code; "
        "instead, it leverages information that can be obtained from the physical device, making it a significant "
        "concern in secure hardware design. There are 3 types of power analysis: "
        "<ol>"
        "<li><b>Simple Power Analysis (SPA): </b>SPA involves directly observing the power consumption of a device during cryptographic operations.</li>"
        "<li><b>Differential Power Analysis (DPA): </b>DPA is a more advanced and sophisticated form of power analysis. "
        "It involves statistically analyzing the power consumption during multiple cryptographic operations and comparing power traces taken from different inputs or states.</li>"
        "<li><b>Higher-Order Differential Power Analysis (HO-DPA): </b>HO-DPA is an advanced form of DPA attack, but is less widely practiced than SPA and DPA.</li>"
        "</ol>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Power_analysis'>Wikipedia</a><br>"
        "<a href='https://www.allaboutcircuits.com/technical-articles/a-basic-introduction-to-power-based-side-channel-attacks/'>AllAboutCircuits</a><br>"
        "<a href='https://www.mdpi.com/2410-387X/4/2/15'>MDPI</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
