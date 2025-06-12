from PyQt6.QtWidgets                                    import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                         import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style                     import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style                     import DefaultQLineEditStyle 
from cryptography.hazmat.backends                       import default_backend
from cryptography.hazmat.primitives.asymmetric          import ec
from cryptography.hazmat.primitives                     import hashes
from cryptography.hazmat.primitives.asymmetric.utils    import decode_dss_signature, encode_dss_signature
from cryptography.hazmat.primitives.serialization       import Encoding, PublicFormat

class YAK:
    def __init__(self):
        # Generate private key for participant (Alice or Bob)
        self.private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key = self.private_key.public_key()
    
    def get_public_key_bytes(self):
        # Serialize public key to bytes (to send to the other party)
        return self.public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)

    def sign_message(self, message):
        # Sign a message using ECDSA
        signature = self.private_key.sign(message, ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(signature)
        return r, s
    
    def verify_signature(self, public_key_bytes, message, signature):
        # Verify a signature using the provided public key bytes
        public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), public_key_bytes)
        r, s = signature
        signature_bytes = encode_dss_signature(r, s)
        try:
            public_key.verify(signature_bytes, message, ec.ECDSA(hashes.SHA256()))
            return True
        except:
            return False

    def compute_shared_secret(self, peer_public_key_bytes):
        # Compute shared secret using peer's public key
        peer_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), peer_public_key_bytes)
        shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)
        return shared_secret

# https://asecuritysite.com/keyexchange/yak
class YAKWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YAK public-key authenticated key-agreement protocol")
        self.setFixedSize(700, 800)

'''
    alice = YAK()
    bob = YAK()

    alice_public_key = alice.get_public_key_bytes()
    bob_public_key = bob.get_public_key_bytes()

    alice_shared_secret = alice.compute_shared_secret(bob_public_key)
    bob_shared_secret = bob.compute_shared_secret(alice_public_key)

    assert alice_shared_secret == bob_shared_secret, "Shared secrets don't match!"

    message = b"Hello, Bob!"
    signature = alice.sign_message(message)

    is_valid = bob.verify_signature(alice_public_key, message, signature)
    print("Is Alice's signature valid?", is_valid)
'''