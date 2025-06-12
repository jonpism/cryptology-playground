from PyQt6.QtWidgets                import QWidget, QTextBrowser

class CPA(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chosen-Plaintext Analysis")
        self.setFixedSize(700, 370)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("In this type of attack the attacker can choose arbitrary plaintexts and obtain their corresponding "
        "ciphertexts. This capability allows the attacker to analyze how the encryption algorithm processes different inputs "
        ", potentially revealing weaknesses in the encryption scheme. Its very simple to implement like "
        "<a href='https://cointelegraph.com/explained/known-plaintext-attacks-explained'>KPA</a> but the success rate "
        "is quite low. The attacker has the ability to select plaintexts and observe their encrypted outputs. Information about the "
        "encryption key and the structure of the encryption algorithm can be uncovered. <br><br>"
        "<b>Example: Chosen-Plaintext attack on Caesar Cipher</b> <br>"
        "Let's say Eve (the attacker) suspects a system is using Caesar Cipher for encryption. Eve can input plaintext messages and "
        "observe their encrypted versions. She selects the plaintext: ABCDEFGHIJKLMNOPQRSTUVWXYZ and then the system encrypts this "
        "plaintext and returns the output: CIPHERTEXT:  DEFGHIJKLMNOPQRSTUVWXYZABC. <br>"
        "Eve then analyzes the output by comparing the plaintext to the ciphertext and she deduces the shift: A->D, B->E, C->F, etc."
        "Since the shift is consistent for every letter, Eve determines that the encryption uses a Caesar cipher with a shift of 3. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Chosen-plaintext_attack'>Wikipedia</a> <br>"
        "<a href='https://www.baeldung.com/cs/cryptography-known-plaintext-attack-vs-chosen-plaintext-attack'>Baeldung</a> <br>"
        "<a href='https://nordvpn.com/cybersecurity/glossary/chosen-plaintext-attack/'>NordVPN</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
