from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import asn1crypto.core

class Address(asn1crypto.core.Sequence):
    _fields = [
        ('street', asn1crypto.core.OctetString),
        ('city', asn1crypto.core.OctetString),
        ('postal_code', asn1crypto.core.OctetString),
        ('country', asn1crypto.core.OctetString)]

class MyMessage(asn1crypto.core.Sequence):
    _fields = [
        ('id', asn1crypto.core.Integer),
        ('name', asn1crypto.core.OctetString),
        ('email', asn1crypto.core.OctetString),
        ('phone', asn1crypto.core.IA5String),  # Using IA5String for phone number
        ('address', Address),                  # Nested address structure
        ('message', asn1crypto.core.OctetString)] # Message to send

class ASN1About(QWidget):

    def __init__(self, msgbox_title, msgbox_txt, ax, ay, aw, ah, theme_mode):
        super().__init__()

        self.msgbox_title = msgbox_title
        self.msgbox_txt = msgbox_txt
        self.theme_mode = theme_mode

        self.setup_about_button(ax, ay, aw, ah)

    def setup_about_button(self, ax, ay, aw, ah):
        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=self.msgbox_txt, title=self.msgbox_title, geometry=(ax, ay, aw, ah))
        self.aboutButton.update_theme(self.theme_mode)
    
    def show_about_dialog(self):
        """Displays the About dialog using the provided title and text."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.about_title)
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(self.about_text)
        msg_box.exec()


class ASN1EncodeWindow(ASN1About):
    
    def __init__(self, theme_mode):
        self.about_title = "About ASN.1"
        self.about_text = (
        "<p>Abstract Syntax Notation One (ASN.1) is a standard interface description language used for defining the structure of data that is exchanged "
        "between systems in a platform-independent way. ASN.1 is widely used in many communication protocols, cryptographic systems, and data formats, "
        "where it provides a flexible, compact, and extensible method for encoding and decoding data in a manner that is independent of the underlying hardware "
        "or software environment.</p>"
        "<p><strong>Characteristics of ASN.1:</strong></p>"
        "<ul>"
        "<li>ASN.1 is used to describe the structure of data (such as integers, strings, sequences, etc.) in a formal, machine-independent way.</li>"
        "<li>It is commonly used in communication protocols like SNMP (Simple Network Management Protocol), LDAP (Lightweight Directory Access Protocol), "
        "and X.509 certificates (used in public key infrastructure).</li>"
        "<li>ASN.1 is closely related to the concepts of data types and data structures, providing a set of rules for how data should be encoded, transmitted, "
        "and decoded.</li>"
        "<li>It is designed to be both human-readable and machine-readable, with specific encoding rules that enable compact and efficient transmission.</li>"
        "<li>ASN.1 supports multiple encoding formats such as DER (Distinguished Encoding Rules) and BER (Basic Encoding Rules), allowing for flexibility in how data is transmitted.</li>"
        "</ul>"
        "<p>ASN.1 is commonly employed in security systems (for example, X.509 certificates and encryption keys), as well as in network protocols and messaging standards. "
        "Its primary strength lies in its ability to represent complex data structures in a standardized way, making it suitable for use in diverse environments, from cryptographic applications to telecommunications and web services.</p>"
        "<p>One of the key advantages of ASN.1 is its flexibility in encoding formats. While it can be used with a wide variety of encoding schemes (such as BER, DER, or PER), "
        "the Distinguished Encoding Rules (DER) is most commonly used in applications where security and data integrity are critical. DER ensures that the encoding is unique, "
        "which is essential for applications like digital signatures and certificate validation.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One'>ASN.1 - Wikipedia</a></li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 750, 50, 50
        super().__init__(self.about_title, self.about_text, ax, ay, aw, ah, theme_mode)

        self.setWindowTitle("Custom ASN.1 Message Encode (Abstract Syntax Notation One)")
        self.setFixedSize(700, 800)

        # ID input
        id_input_label = QLabel("ID:", parent=self)
        id_input_label.setGeometry(30, 10, 100, 50)
        self.id_input = DefaultQLineEditStyle(parent=self, max_length=12, int_validator=True)
        self.id_input.setGeometry(60, 10, 100, 50)

        # Name input
        name_input_label = QLabel("Fullname:", parent=self)
        name_input_label.setGeometry(220, 10, 100, 50)
        self.name_input = DefaultQLineEditStyle(parent=self, max_length=40)
        self.name_input.setGeometry(300, 10, 250, 50)

        # Email input
        email_input_label = QLabel("Email:", parent=self)
        email_input_label.setGeometry(30, 100, 100, 50)
        self.email_input = DefaultQLineEditStyle(parent=self, max_length=40)
        self.email_input.setGeometry(80, 100, 250, 50)

        # Phone input
        phone_input_label = QLabel("Phone:", parent=self)
        phone_input_label.setGeometry(390, 100, 100, 50)
        self.phone_input = DefaultQLineEditStyle(parent=self, max_length=25, int_validator=True)
        self.phone_input.setGeometry(450, 100, 200, 50)

        # Street input
        street_input_label = QLabel("Street:", parent=self)
        street_input_label.setGeometry(30, 200, 100, 50)
        self.street_input = DefaultQLineEditStyle(parent=self, max_length=35)
        self.street_input.setGeometry(80, 200, 250, 50)
        # City input
        city_input_label = QLabel("City:", parent=self)
        city_input_label.setGeometry(390, 200, 100, 50)
        self.city_input = DefaultQLineEditStyle(parent=self, max_length=20)
        self.city_input.setGeometry(430, 200, 250, 50)
        # Postal code
        postal_code_input_label = QLabel("Postal Code:", parent=self)
        postal_code_input_label.setGeometry(30, 300, 100, 50)
        self.postal_code_input = DefaultQLineEditStyle(parent=self, max_length=15, int_validator=True)
        self.postal_code_input.setGeometry(120, 300, 100, 50)
        # Country
        country_input_label = QLabel("Country:", parent=self)
        country_input_label.setGeometry(300, 300, 100, 50)
        self.country_input = DefaultQLineEditStyle(parent=self, max_length=15)
        self.country_input.setGeometry(380, 300, 150, 50)

        # Message input
        message_input_label = QLabel("Give Message:", parent=self)
        message_input_label.setGeometry(300, 370, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 420, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_asn1_encode)
        submit_button.setGeometry(300, 480, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 580, 680, 150)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

    def call_asn1_encode(self):
        try:
            if self.id_input.text():
                if self.name_input.text():
                    if self.email_input.text():
                        if self.phone_input.text():
                            if self.street_input.text():
                                if self.city_input.text():
                                    if self.postal_code_input.text():
                                        if self.country_input.text():
                                            if self.message_input.text():
                                                id = int(self.id_input.text())
                                                name = self.name_input.text().encode('utf-8')
                                                email = self.email_input.text().encode('utf-8')
                                                phone = self.phone_input.text()
                                                street = self.street_input.text().encode('utf-8')
                                                city = self.city_input.text().encode('utf-8')
                                                postal_code = self.postal_code_input.text().encode('utf-8')
                                                country = self.country_input.text().encode('utf-8')
                                                msg = self.message_input.text().encode('utf-8') 

                                                message = MyMessage({
                                                    'id': id,
                                                    'name': name,
                                                    'email': email,
                                                    'phone': phone,
                                                    'address': {
                                                        'street': street,
                                                        'city': city,
                                                        'postal_code': postal_code,
                                                        'country': country},
                                                    'message': msg})

                                                encoded_message = message.dump()
                                                self.result_label.clear()
                                                self.result_label.setHtml(f"<b>Encoded message (DER format):</b><br>{str(encoded_message.hex())}")
                                                self.result_label.show()
                                            else:
                                                raise ValueError('Please enter message.')
                                        else:
                                            raise ValueError('Please enter country.')    
                                    else:
                                        raise ValueError('Please enter postal code.')
                                else:
                                    raise ValueError('Please enter city.')
                            else:
                                raise ValueError('Please enter street.')
                        else:
                            raise ValueError('Please enter phone.')
                    else:
                        raise ValueError('Please enter email.')
                else:
                    raise ValueError('Please enter name.')
            else:
                raise ValueError('Please enter ID.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ====================================================================================================================

class ASN1DecodeWindow(ASN1About):
    
    def __init__(self, theme_mode):
        self.about_title = "About ASN.1"
        self.about_text = (
        "<p>Abstract Syntax Notation One (ASN.1) is a standard interface description language used for defining the structure of data that is exchanged "
        "between systems in a platform-independent way. ASN.1 is widely used in many communication protocols, cryptographic systems, and data formats, "
        "where it provides a flexible, compact, and extensible method for encoding and decoding data in a manner that is independent of the underlying hardware "
        "or software environment.</p>"
        "<p><strong>Characteristics of ASN.1:</strong></p>"
        "<ul>"
        "<li>ASN.1 is used to describe the structure of data (such as integers, strings, sequences, etc.) in a formal, machine-independent way.</li>"
        "<li>It is commonly used in communication protocols like SNMP (Simple Network Management Protocol), LDAP (Lightweight Directory Access Protocol), "
        "and X.509 certificates (used in public key infrastructure).</li>"
        "<li>ASN.1 is closely related to the concepts of data types and data structures, providing a set of rules for how data should be encoded, transmitted, "
        "and decoded.</li>"
        "<li>It is designed to be both human-readable and machine-readable, with specific encoding rules that enable compact and efficient transmission.</li>"
        "<li>ASN.1 supports multiple encoding formats such as DER (Distinguished Encoding Rules) and BER (Basic Encoding Rules), allowing for flexibility in how data is transmitted.</li>"
        "</ul>"
        "<p>ASN.1 is commonly employed in security systems (for example, X.509 certificates and encryption keys), as well as in network protocols and messaging standards. "
        "Its primary strength lies in its ability to represent complex data structures in a standardized way, making it suitable for use in diverse environments, from cryptographic applications to telecommunications and web services.</p>"
        "<p>One of the key advantages of ASN.1 is its flexibility in encoding formats. While it can be used with a wide variety of encoding schemes (such as BER, DER, or PER), "
        "the Distinguished Encoding Rules (DER) is most commonly used in applications where security and data integrity are critical. DER ensures that the encoding is unique, "
        "which is essential for applications like digital signatures and certificate validation.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One'>ASN.1 - Wikipedia</a></li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 650, 50, 50
        super().__init__(self.about_title, self.about_text, ax, ay, aw, ah, theme_mode)

        self.setWindowTitle("Custom ASN.1 Message Decode (Abstract Syntax Notation One)")
        self.setFixedSize(700, 700)

        # Encoded asn1 input
        encoded_input_label = QLabel("Give Encoded message from custom ASN.1 format:", parent=self)
        encoded_input_label.setGeometry(100, 10, 350, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_asn1_decode)
        submit_button.setGeometry(300, 120, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 220, 680, 300)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

    def call_asn1_decode(self):
        try:
            # Retrieve the hexadecimal string from the input field
            encoded_message_hex = self.encoded_input.text()

            # Convert the hex string back to bytes
            encoded_message = bytes.fromhex(encoded_message_hex)

            # Decode the message using the ASN.1 MyMessage class
            decoded_message = MyMessage.load(encoded_message)

            # Display the decoded fields
            decoded_output = (
                f"Decoded ID: {decoded_message['id'].native}\n"
                f"Decoded Name: {decoded_message['name'].native.decode('utf-8')}\n"
                f"Decoded Email: {decoded_message['email'].native.decode('utf-8')}\n"
                f"Decoded Phone: {decoded_message['phone'].native}\n"
                f"Decoded Address: {decoded_message['address']['street'].native.decode('utf-8')}, "
                f"{decoded_message['address']['city'].native.decode('utf-8')}, "
                f"{decoded_message['address']['postal_code'].native.decode('utf-8')}, "
                f"{decoded_message['address']['country'].native.decode('utf-8')}\n"
                f"Decoded Message: {decoded_message['message'].native.decode('utf-8')}")
            self.result_label.setText(decoded_output)
            self.result_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
            self.result_label.setText(f"Error decoding message: {str(ve)}")
            self.result_label.show()
