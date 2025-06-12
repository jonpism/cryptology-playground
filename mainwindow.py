import sys
from PyQt6.QtWidgets    import QApplication, QMainWindow, QMessageBox; from PyQt6.QtMultimedia   import QMediaPlayer, QAudioOutput
from PyQt6.QtCore   import QUrl; from DefaultStyles.button_style import DefaultButtonStyle, DefaultAboutButtonStyle
from ui_MainWindow  import Ui_MainWindow
from asymmetric import *; from symmetric    import *; from ciphers      import *; from hashingalgo  import *
from encoders   import *; from converters   import *; from fileHandling import *; from othertools   import *
from section_titles_and_texts_about import *; from cryptanalysis import *

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.theme_mode = "dark"
        self.ui.setupUi(self, theme_mode=self.theme_mode)

        # Music player/button setup
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.music_playing = False
        self.MusicButton = DefaultButtonStyle("", parent=self, command=self.TurnOnOffMusic, music=True)
        self.MusicButton.setGeometry(170, 25, 50, 50)
        self.MusicButton.setStyleSheet(self.MusicButton.get_style_music_off())

        # Help button setup
        self.HelpButton = DefaultButtonStyle("", parent=self, command=self.OpenHelpPage)
        self.HelpButton.setGeometry(90, 25, 50, 50)
        self.HelpButton.setStyleSheet(self.HelpButton.get_help_style())
        self.HelpButton.setCheckable(True)
        self.HelpButton.clicked.connect(lambda: self.handle_checked(self.HelpButton))

        # Settings button setup
        self.SettingsButton = DefaultButtonStyle("", parent=self, command=self.OpenSettingsPage)
        self.SettingsButton.setGeometry(10, 25, 50, 50)
        self.SettingsButton.setStyleSheet(self.SettingsButton.get_settings_style())
        self.SettingsButton.setCheckable(True)
        self.SettingsButton.clicked.connect(lambda: self.handle_checked(self.SettingsButton))
        # update song
        self.ui.settings_ui.song_selected.connect(self.update_selected_song)
        # update theme mode and change buttons style regarding theme mode
        self.theme_mode = "dark"
        self.ui.settings_ui.theme_changed.connect(self.apply_theme)
        self.about_buttons = []

        ''' Show Home Page first: '''
        self.ui.stackedWidget.setCurrentWidget(self.ui.homepage_ui.HomePage)

        '''Set the border and stylesheet of every stackedWidget'''
        self.ui.stackedWidget.setStyleSheet("""
            QStackedWidget {
                border: 2px solid #5D6D7E;
                border-radius: 15px;
                padding: 10px;}""")

        ''' Buttons to open sections AND each section button method: '''
        self.ui.HomePageButton.clicked.connect              (self.OpenHomePageSection)
        self.ui.HomePageButton.setCheckable(True)
        self.ui.HomePageButton.clicked.connect              (lambda: self.handle_checked(self.ui.HomePageButton))
        
        # ASYMMETRIC SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.AsymmetricEncryptionButton.clicked.connect  (self.OpenAsymmetricSection)
        self.ui.AsymmetricEncryptionButton.setCheckable(True)
        self.ui.AsymmetricEncryptionButton.clicked.connect  (lambda: self.handle_checked(self.ui.AsymmetricEncryptionButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.asymmetric_ui.AsymmetricPage, txt=asymmetric_text, 
            title=asymmetric_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.asymmetric_ui.asymmetric_buttons["CSRButton"].clicked.connect(self.OpenCSRWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["DHKeyExchangeButton"].clicked.connect(self.OpenDHKeyExchangeWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["DSAButton"].clicked.connect(self.OpenDSAWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["ElGamalButton"].clicked.connect(self.OpenElGamalWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["RSAWienerAttackButton"].clicked.connect(self.OpenRSAWienerAttackWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["RSAButton"].clicked.connect(self.OpenRSAWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["X509SelfSignedButton"].clicked.connect(self.OpenX509SelfSignedCertWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["CramerShoupEncButton"].clicked.connect(self.OpenCramerShoupEncWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["CramerShoupDecButton"].clicked.connect(self.OpenCramerShoupDecWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["PaillierEncButton"].clicked.connect(self.OpenPaillierEncWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["PaillierDecButton"].clicked.connect(self.OpenPaillierDecWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["ECDSAButton"].clicked.connect(self.OpenECDSAWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["ECDHButton"].clicked.connect(self.OpenECDHWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["EdDSAButton"].clicked.connect(self.OpenEdDSAWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["NTRUEncryptButton"].clicked.connect(self.OpenNTRUEncryptWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["KyberKEMButton"].clicked.connect(self.OpenKyberKEMWindow)
        self.ui.asymmetric_ui.asymmetric_buttons["KyberKEMDecButton"].clicked.connect(self.OpenKyberKEMDecWindow)
        
        # SYMMETRIC SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.SymmetricEncryptionButton.clicked.connect   (self.OpenSymmetricSection)
        self.ui.SymmetricEncryptionButton.setCheckable(True)
        self.ui.SymmetricEncryptionButton.clicked.connect   (lambda: self.handle_checked(self.ui.SymmetricEncryptionButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.symmetric_ui.SymmetricPage, txt=symmetric_text, 
            title=symmetric_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.symmetric_ui.symmetric_buttons["AESEncButton"].clicked.connect(self.OpenAESEncryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["AESDecButton"].clicked.connect(self.OpenAESDecryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["DESEncButton"].clicked.connect(self.OpenDESEncryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["DESDecButton"].clicked.connect(self.OpenDESDecryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["BlowfishButton"].clicked.connect(self.OpenBlowfishWindow)
        self.ui.symmetric_ui.symmetric_buttons["CamelliaButton"].clicked.connect(self.OpenCamelliaWindow)
        self.ui.symmetric_ui.symmetric_buttons["RC2EncButton"].clicked.connect(self.OpenRC2EncryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["RC2DecButton"].clicked.connect(self.OpenRC2DecryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["RC5EncButton"].clicked.connect(self.OpenRC5EncryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["RC5DecButton"].clicked.connect(self.OpenRC5DecryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["SerpentButton"].clicked.connect(self.OpenSerpentWindow)
        self.ui.symmetric_ui.symmetric_buttons["TripleDESEncButton"].clicked.connect(self.Open3DESEncryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["TripleDESDecButton"].clicked.connect(self.Open3DESDecryptionWindow)
        self.ui.symmetric_ui.symmetric_buttons["TwofishButton"].clicked.connect(self.OpenTwofishWindow)
        self.ui.symmetric_ui.symmetric_buttons["FERNETButton"].clicked.connect(self.OpenFernetWindow)

        # CIPHERS SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.CiphersButton.clicked.connect               (self.OpenCiphersSection)
        self.ui.CiphersButton.setCheckable(True)
        self.ui.CiphersButton.clicked.connect               (lambda: self.handle_checked(self.ui.CiphersButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.ciphers_ui.CiphersPage, txt=ciphers_text, 
            title=ciphers_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.ciphers_ui.ciphers_buttons["BaconCipherButton"].clicked.connect(self.OpenBaconCipherWindow)
        self.ui.ciphers_ui.ciphers_buttons["CaesarCipherButton"].clicked.connect(self.OpenCaesarCipherWindow)
        self.ui.ciphers_ui.ciphers_buttons["ChaChaPolyButton"].clicked.connect(self.OpenChaChaPolyWindow)
        self.ui.ciphers_ui.ciphers_buttons["ChaCha20Button"].clicked.connect(self.OpenChaCha20Window)
        self.ui.ciphers_ui.ciphers_buttons["EnigmaButton"].clicked.connect(self.OpenEnigmaMachineWindow)
        self.ui.ciphers_ui.ciphers_buttons["GOSTButton"].clicked.connect(self.OpenGOSTMagmaWindow)
        self.ui.ciphers_ui.ciphers_buttons["RabbitButton"].clicked.connect(self.OpenRabbitStreamCipherWindow)
        self.ui.ciphers_ui.ciphers_buttons["RC4EncButton"].clicked.connect(self.OpenRC4EncryptionWindow)
        self.ui.ciphers_ui.ciphers_buttons["RC4DecButton"].clicked.connect(self.OpenRC4DecryptionWindow)
        self.ui.ciphers_ui.ciphers_buttons["ROT13Button"].clicked.connect(self.OpenROT13Window)
        self.ui.ciphers_ui.ciphers_buttons["ROT13BFButton"].clicked.connect(self.OpenROT13BruteForceWindow)
        self.ui.ciphers_ui.ciphers_buttons["ROT47Button"].clicked.connect(self.OpenROT47Window)
        self.ui.ciphers_ui.ciphers_buttons["ROT47BFButton"].clicked.connect(self.OpenROT47BruteForceWindow)
        self.ui.ciphers_ui.ciphers_buttons["SimpleSubButton"].clicked.connect(self.OpenSimpleSubstitutionWindow)
        self.ui.ciphers_ui.ciphers_buttons["TEAButton"].clicked.connect(self.OpenTEAWindow)
        self.ui.ciphers_ui.ciphers_buttons["XTEAButton"].clicked.connect(self.OpenXTEAWindow)
        self.ui.ciphers_ui.ciphers_buttons["XXTEAButton"].clicked.connect(self.OpenXXTEAWindow)
        self.ui.ciphers_ui.ciphers_buttons["VigenereEncButton"].clicked.connect(self.OpenVigenereEncrptionWindow)
        self.ui.ciphers_ui.ciphers_buttons["VigenereDecButton"].clicked.connect(self.OpenVigenereDecrptionWindow)
        self.ui.ciphers_ui.ciphers_buttons["SM4EncryptButton"].clicked.connect(self.OpenSM4EncryptWindow)
        self.ui.ciphers_ui.ciphers_buttons["SM4DecryptButton"].clicked.connect(self.OpenSM4DecryptWindow)
        self.ui.ciphers_ui.ciphers_buttons["BifidCipherButton"].clicked.connect(self.OpenBifidCipherWindow)
        self.ui.ciphers_ui.ciphers_buttons["AffineCipherEncButton"].clicked.connect(self.OpenAffineCipherEncWindow)
        self.ui.ciphers_ui.ciphers_buttons["AffineCipherDecButton"].clicked.connect(self.OpenAffineCipherDecWindow)

        # HASHING ALGORITHMS SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.HashAlgoButton.clicked.connect              (self.OpenHashAlgoSection)
        self.ui.HashAlgoButton.setCheckable(True)
        self.ui.HashAlgoButton.clicked.connect              (lambda: self.handle_checked(self.ui.HashAlgoButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.hashalgo_ui.HashAlgoPage, txt=hashalgo_text, 
            title=hashalgo_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.hashalgo_ui.hash_algo_buttons["BcryptButton"].clicked.connect(self.OpenBcryptWindow)
        self.ui.hashalgo_ui.hash_algo_buttons["BLAKE2Button"].clicked.connect(self.OpenBLAKE2Window)
        self.ui.hashalgo_ui.hash_algo_buttons["BLAKE3Button"].clicked.connect(self.OpenBLAKE3Window)
        self.ui.hashalgo_ui.hash_algo_buttons["MD4Button"].clicked.connect(self.OpenMD4Window)
        self.ui.hashalgo_ui.hash_algo_buttons["MD5Button"].clicked.connect(self.OpenMD5Window)
        self.ui.hashalgo_ui.hash_algo_buttons["RIPEMD160Button"].clicked.connect(self.OpenRIPEMD160Window)
        self.ui.hashalgo_ui.hash_algo_buttons["SHA1Button"].clicked.connect(self.OpenSHA1Window)
        self.ui.hashalgo_ui.hash_algo_buttons["SHA256Button"].clicked.connect(self.OpenSHA256Window)
        self.ui.hashalgo_ui.hash_algo_buttons["SHA384Button"].clicked.connect(self.OpenSHA384Window)
        self.ui.hashalgo_ui.hash_algo_buttons["SHA512Button"].clicked.connect(self.OpenSHA512Window)
        self.ui.hashalgo_ui.hash_algo_buttons["WhirlpoolButton"].clicked.connect(self.OpenWhirlpoolWindow)
        self.ui.hashalgo_ui.hash_algo_buttons["HashIdentifier"].clicked.connect(self.OpenHashIdentifierWindow)
        self.ui.hashalgo_ui.hash_algo_buttons["GostHfButton"].clicked.connect(self.OpenGOSTHashFunctionWindow)
        self.ui.hashalgo_ui.hash_algo_buttons["TigerHashFunctionButton"].clicked.connect(self.OpenTigerHasFunctionWindow)
        self.ui.hashalgo_ui.hash_algo_buttons["KeccakButton"].clicked.connect(self.OpenKeccakWindow)
        
        # ENCODERS/DECODERS SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.EncodersButton.clicked.connect              (self.OpenEncodersSection)
        self.ui.EncodersButton.setCheckable(True)
        self.ui.EncodersButton.clicked.connect              (lambda: self.handle_checked(self.ui.EncodersButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.encoders_ui.EncodersPage, txt=encoders_text, 
            title=encoders_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.encoders_ui.encoders_buttons["A1Z26EncButton"].clicked.connect(self.OpenA1Z26EncWindow)
        self.ui.encoders_ui.encoders_buttons["A1Z26DecButton"].clicked.connect(self.OpenA1Z26DecWindow)
        self.ui.encoders_ui.encoders_buttons["BASE32Button"].clicked.connect(self.OpenBase32Window)
        self.ui.encoders_ui.encoders_buttons["BASE45Button"].clicked.connect(self.OpenBase45Window)
        self.ui.encoders_ui.encoders_buttons["BASE58Button"].clicked.connect(self.OpenBase58Window)
        self.ui.encoders_ui.encoders_buttons["BASE62Button"].clicked.connect(self.OpenBase62Window)
        self.ui.encoders_ui.encoders_buttons["BASE64Button"].clicked.connect(self.OpenBase64Window)
        self.ui.encoders_ui.encoders_buttons["BASE85Button"].clicked.connect(self.OpenBase85Window)
        self.ui.encoders_ui.encoders_buttons["BASE92Button"].clicked.connect(self.OpenBase92Window)
        self.ui.encoders_ui.encoders_buttons["BrailleButton"].clicked.connect(self.OpenBrailleWindow)
        self.ui.encoders_ui.encoders_buttons["MorseCodeButton"].clicked.connect(self.OpenMorseCodeWindow)
        self.ui.encoders_ui.encoders_buttons["URLEncButton"].clicked.connect(self.OpenURLEncodeWindow)
        self.ui.encoders_ui.encoders_buttons["URLDecButton"].clicked.connect(self.OpenURLDecodeWindow)
        self.ui.encoders_ui.encoders_buttons["TxttoCharcodeButton"].clicked.connect(self.OpentexttoCharcodeWindow)
        self.ui.encoders_ui.encoders_buttons["CharcodetoTxtButton"].clicked.connect(self.OpenCharcodetoTextWindow)
        self.ui.encoders_ui.encoders_buttons["ToQPButton"].clicked.connect(self.OpenToQPWindow)
        self.ui.encoders_ui.encoders_buttons["FromQPButton"].clicked.connect(self.OpenFromQPWindow)

        # CONVERTERS SECTION BUTTON AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.ConvertersButton.clicked.connect            (self.OpenConvertersSection)
        self.ui.ConvertersButton.setCheckable(True)
        self.ui.ConvertersButton.clicked.connect            (lambda: self.handle_checked(self.ui.ConvertersButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.converters_ui.ConvertersPage, txt=converters_text, 
            title=converters_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.converters_ui.converters_buttons["TexttoOctalButton"].clicked.connect(self.OpenTexttoOctalWindow)
        self.ui.converters_ui.converters_buttons["OctaltoTextButton"].clicked.connect(self.OpenOctaltoTextWindow)
        self.ui.converters_ui.converters_buttons["TxttoBinButton"].clicked.connect(self.OpenTexttoBinaryWindow)
        self.ui.converters_ui.converters_buttons["BintoTxtButton"].clicked.connect(self.OpenBinarytoTextWindow)
        self.ui.converters_ui.converters_buttons["TxttoASCIIButton"].clicked.connect(self.OpenTexttoASCIIWindow)
        self.ui.converters_ui.converters_buttons["ASCIItoTxtButton"].clicked.connect(self.OpenASCIItoTextWindow)
        self.ui.converters_ui.converters_buttons["DecimaltoBinButton"].clicked.connect(self.OpenDecimaltoBinaryWindow)
        self.ui.converters_ui.converters_buttons["BintoDecimalButton"].clicked.connect(self.OpenBinarytoDecimalWindow)
        self.ui.converters_ui.converters_buttons["CodepointConverterButton"].clicked.connect(self.OpenCodepointConverterWindow)
        self.ui.converters_ui.converters_buttons["TxttoHexButton"].clicked.connect(self.OpenTxttoHexWindow)
        self.ui.converters_ui.converters_buttons["HextoTxtButton"].clicked.connect(self.OpenHextoTxtWindow)
        self.ui.converters_ui.converters_buttons["DectoRadixButton"].clicked.connect(self.OpenDecToRadixWindow)
        self.ui.converters_ui.converters_buttons["RadixtoDecButton"].clicked.connect(self.OpenRadixToDecWindow)
        self.ui.converters_ui.converters_buttons["DectoBCDButton"].clicked.connect(self.OpenDecimalToBCDWindow)
        self.ui.converters_ui.converters_buttons["BCDtoDecButton"].clicked.connect(self.OpenBCDToDecimalWindow)
        self.ui.converters_ui.converters_buttons["ChartoHTMLEntityBtn"].clicked.connect(self.OpenChartoHTMLEntityWindow)
        self.ui.converters_ui.converters_buttons["HTMLEntitytoCharBtn"].clicked.connect(self.OpenHTMLEntitytoCharWindow)
        self.ui.converters_ui.converters_buttons["PEMtoDERButton"].clicked.connect(self.OpenPEMtoDERWindow)
        self.ui.converters_ui.converters_buttons["DERtoPEMButton"].clicked.connect(self.OpenDERtoPEMWindow)
        self.ui.converters_ui.converters_buttons["ToUnixButton"].clicked.connect(self.OpenToUnixTimestampWindow)
        self.ui.converters_ui.converters_buttons["FromUnixButton"].clicked.connect(self.OpenFromUnixTimestampWindow)
        self.ui.converters_ui.converters_buttons["toNATOButton"].clicked.connect(self.OpenToNatoWindow)
        self.ui.converters_ui.converters_buttons["fromNATOButton"].clicked.connect(self.OpenFromNatoWindow)

        # CRYPTANALYSIS SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.CryptanalysisButton.clicked.connect         (self.OpenCryptanalysisSection)
        self.ui.CryptanalysisButton.setCheckable(True)
        self.ui.CryptanalysisButton.clicked.connect         (lambda: self.handle_checked(self.ui.CryptanalysisButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.cryptanalysis_ui.CryptanalysisPage, txt=cryptanalysis_text, 
            title=cryptanalysis_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["KPAButton"].clicked.connect(self.OpenKPAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["CPAButton"].clicked.connect(self.OpenCPAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["COAButton"].clicked.connect(self.OpenCOAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["MITMButton"].clicked.connect(self.OpenMITMWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["ACPAButton"].clicked.connect(self.OpenACPAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["BirthdayAttackButton"].clicked.connect(self.OpenBirthdayAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["SideChannelAButton"].clicked.connect(self.OpenSideChannelAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["BruteForceAButton"].clicked.connect(self.OpenBruteForceAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["DiffAnalysisButton"].clicked.connect(self.OpenDiffAnalysisWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["RelatedKeyAButton"].clicked.connect(self.OpenRelatedKeyAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["BoomerangAButton"].clicked.connect(self.OpenBoomerangAWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["DaviesAttackButton"].clicked.connect(self.OpenDaviesAttackWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["HarvestNowDLButton"].clicked.connect(self.OpenHarvestNowDLWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["IntegralCryptanalysisButton"].clicked.connect(self.OpenIntegralCryptWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["LinearCryptanalysisButton"].clicked.connect(self.OpenLinearCryptanalysisWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["ModnCryptanalysisButton"].clicked.connect(self.OpenModNcryptanalysisWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["SlideAttackButton"].clicked.connect(self.OpenSlideAttackWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["XSLAttackButton"].clicked.connect(self.OpenXSLAttackWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["RainbowTableButton"].clicked.connect(self.OpenRainbowTableWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["BlackBagCButton"].clicked.connect(self.OpenBlackBagCryptWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["PowerAnalysisButton"].clicked.connect(self.OpenPowerAnalysisWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["ReplayAttackButton"].clicked.connect(self.OpenReplayAttackWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["RubberHoseCButton"].clicked.connect(self.OpenRubberHoseCryptWindow)
        self.ui.cryptanalysis_ui.cryptanalysis_buttons["TimingAnalysisButton"].clicked.connect(self.OpenTimingAnalysisWindow)

        # FILE HANDLING SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.FileHandlingButton.clicked.connect          (self.OpenFileHandlingSection)
        self.ui.FileHandlingButton.setCheckable(True)
        self.ui.FileHandlingButton.clicked.connect          (lambda: self.handle_checked(self.ui.FileHandlingButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.filehandling_ui.FileHandlingPage, txt=file_handling_text, 
            title=file_handling_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.filehandling_ui.filehandling_buttons["FernetFileEncButton"].clicked.connect(self.OpenFernetFileEncWindow)
        self.ui.filehandling_ui.filehandling_buttons["FernetFileDecButton"].clicked.connect(self.OpenFernetFileDecWindow)
        self.ui.filehandling_ui.filehandling_buttons["CSVtoJSONButton"].clicked.connect(self.OpenCSVtoJSONWindow)
        self.ui.filehandling_ui.filehandling_buttons["JSONtoCSVButton"].clicked.connect(self.OpenJSONtoCSVWindow)
        self.ui.filehandling_ui.filehandling_buttons["Img2PDFButton"].clicked.connect(self.OpenImg2PDFWindow)
        self.ui.filehandling_ui.filehandling_buttons["PDF2ImgButton"].clicked.connect(self.OpenPDF2ImgWindow)
        self.ui.filehandling_ui.filehandling_buttons["ExifImagesButton"].clicked.connect(self.OpenExifImagesWindow)
        self.ui.filehandling_ui.filehandling_buttons["ZipFileWithPwdButton"].clicked.connect(self.OpenZipFileWithPwdWindow)
        self.ui.filehandling_ui.filehandling_buttons["ZipFolderWithPwdButton"].clicked.connect(self.OpenZipFolderWithPwdWindow)
        self.ui.filehandling_ui.filehandling_buttons["BfPwdProtectedButton"].clicked.connect(self.OpenBfPwdProtectedFilesWindow)
        self.ui.filehandling_ui.filehandling_buttons["DisExeFilesButton"].clicked.connect(self.OpenDisExeFilesWindow)
        self.ui.filehandling_ui.filehandling_buttons["DecompilePycButton"].clicked.connect(self.OpenDecompilePycFilesWindow)
        self.ui.filehandling_ui.filehandling_buttons["JSONtoMsgPackButton"].clicked.connect(self.OpenJSONtoMsgPackWindow)
        self.ui.filehandling_ui.filehandling_buttons["MsgPacktoJSONButton"].clicked.connect(self.OpenMsgPacktoJSONWindow)
        self.ui.filehandling_ui.filehandling_buttons["JSONtoXMLButton"].clicked.connect(self.OpenJSONtoXMLWindow)
        self.ui.filehandling_ui.filehandling_buttons["XMLtoJSONBUtton"].clicked.connect(self.OpenXMLtoJSONWindow)
        self.ui.filehandling_ui.filehandling_buttons["PyCodeDisassemblerButton"].clicked.connect(self.OpenPyCodeDisassemblerWindow)
        self.ui.filehandling_ui.filehandling_buttons["FileTypeDetectorButton"].clicked.connect(self.OpenFileTypeDetectorWindow)
        self.ui.filehandling_ui.filehandling_buttons["PGPEncryptorButton"].clicked.connect(self.OpenPGPEncryptorWindow)
        self.ui.filehandling_ui.filehandling_buttons["PGPDecryptorButton"].clicked.connect(self.OpenPGPDecryptorWindow)

        # OTHER TOOLS SECTION AND BUTTONS TO OPEN METHODS/ALGORITHMS:
        self.ui.OtherToolsButton.clicked.connect            (self.OpenOtherToolsSection)
        self.ui.OtherToolsButton.setCheckable(True)
        self.ui.OtherToolsButton.clicked.connect            (lambda: self.handle_checked(self.ui.OtherToolsButton))
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self.ui.othertools_ui.OtherToolsPage, txt=othertools_text, 
            title=othertools_title, geometry=(975, 545, 50, 50))
        self.about_buttons.append(self.aboutButton)
        self.ui.othertools_ui.other_tools_buttons["CircBitShiftButton"].clicked.connect(self.OpenCircularBitShiftWindow)
        self.ui.othertools_ui.other_tools_buttons["FreqAnalysisButton"].clicked.connect(self.OpenFrequencyAnalysisWindow)
        self.ui.othertools_ui.other_tools_buttons["OTPButton"].clicked.connect(self.OpenOneTimePadWindow)
        self.ui.othertools_ui.other_tools_buttons["PBKDF2Button"].clicked.connect(self.OpenPBKDF2Window)
        self.ui.othertools_ui.other_tools_buttons["PrimeNumGenButton"].clicked.connect(self.OpenPrimeNumGeneratorWindow)
        self.ui.othertools_ui.other_tools_buttons["PRNGButton"].clicked.connect(self.OpenPRNGeneratorWindow)
        self.ui.othertools_ui.other_tools_buttons["PwdGenButton"].clicked.connect(self.OpenStrongPwdGeneratorWindow)
        self.ui.othertools_ui.other_tools_buttons["RSAKeyGenButton"].clicked.connect(self.OpenRSAKeyGeneratorWindow)
        self.ui.othertools_ui.other_tools_buttons["ScryptButton"].clicked.connect(self.OpenScryptWindow)
        self.ui.othertools_ui.other_tools_buttons["XORButton"].clicked.connect(self.OpenXOROperationWindow)
        self.ui.othertools_ui.other_tools_buttons["ASN1EncButton"].clicked.connect(self.OpenASN1EncodeWindow)
        self.ui.othertools_ui.other_tools_buttons["ASN1DecButton"].clicked.connect(self.OpenASN1DecodeWindow)
        self.ui.othertools_ui.other_tools_buttons["IntFactorButton"].clicked.connect(self.OpenIntFactorWindow)
        self.ui.othertools_ui.other_tools_buttons["SwapEndianButton"].clicked.connect(self.OpenSwapEndianessWindow)
        self.ui.othertools_ui.other_tools_buttons["ReverseTextButton"].clicked.connect(self.OpenReverseTextWindow)
        self.ui.othertools_ui.other_tools_buttons["HMACButton"].clicked.connect(self.OpenHMACWindow)
        self.ui.othertools_ui.other_tools_buttons["Argon2Button"].clicked.connect(self.OpenArgon2Window)
        self.ui.othertools_ui.other_tools_buttons["ShowOnMapButton"].clicked.connect(self.OpenShowOnMapWindow)
        self.ui.othertools_ui.other_tools_buttons["ShowOnMap2Button"].clicked.connect(self.OpenShowOnMap2Window)
        self.ui.othertools_ui.other_tools_buttons["ECKeyPairButton"].clicked.connect(self.OpenECKeyPairWindow)
        self.ui.othertools_ui.other_tools_buttons["EntropyButton"].clicked.connect(self.OpenEntropyWindow)
        self.ui.othertools_ui.other_tools_buttons["DataDiffButton"].clicked.connect(self.OpenDataDifferencingWindow)
        self.ui.othertools_ui.other_tools_buttons["DataCompressionButton"].clicked.connect(self.OpenDataCompressionWindow)
        self.ui.othertools_ui.other_tools_buttons["RandomnessTesterButton"].clicked.connect(self.OpenRandomnessTesterWindow)
        self.ui.othertools_ui.other_tools_buttons["PGPKeyPairButton"].clicked.connect(self.OpenPGPKeyPairGenerateWindow)
        self.ui.othertools_ui.other_tools_buttons["DSAKeyPairGenButton"].clicked.connect(self.OpenDSAKeyPairGenerateWindow)
        self.ui.othertools_ui.other_tools_buttons["EdDSAKeyPairGenButton"].clicked.connect(self.OpenEdDSAKeyPairGenWindow)
        self.ui.othertools_ui.other_tools_buttons["LoremIpsumGenButton"].clicked.connect(self.OpenLoremIpsumGenWindow)
        self.ui.othertools_ui.other_tools_buttons["ModCalcButton"].clicked.connect(self.OpenModCalcWindow)
        self.ui.othertools_ui.other_tools_buttons["JWTSignButton"].clicked.connect(self.OpenJWTSignWindow)
        self.ui.othertools_ui.other_tools_buttons["JWTVerifyButton"].clicked.connect(self.OpenJWTVerifyWindow)
        self.ui.othertools_ui.other_tools_buttons["JWTDecodeButton"].clicked.connect(self.OpenJWTDecodeWindow)
        self.ui.othertools_ui.other_tools_buttons["QRCodeGenButton"].clicked.connect(self.OpenGenQRcodeWindow)

    def handle_checked(self, button):
        buttons = [
            self.HelpButton, self.SettingsButton, self.ui.HomePageButton, self.ui.AsymmetricEncryptionButton,
            self.ui.SymmetricEncryptionButton, self.ui.CiphersButton, self.ui.HashAlgoButton,
            self.ui.EncodersButton, self.ui.ConvertersButton, self.ui.CryptanalysisButton,
            self.ui.FileHandlingButton, self.ui.OtherToolsButton]
        for btn in buttons:
            if btn != button:
                btn.setChecked(False)

    def apply_theme(self, theme_name):
        if theme_name == "dark":
            self.qapp.setStyleSheet("QWidget { background-color: #3B3B3B; color: white; }")
            self.theme_mode = "dark"
        elif theme_name == "light":
            self.qapp.setStyleSheet("QWidget { background-color: #F0F0F0; color: black; }")
            self.theme_mode = "light"
        
        self.SettingsButton.update_theme_settings(theme_name)
        self.HelpButton.update_theme_help(theme_name)
        if not self.music_playing:
            self.MusicButton.update_theme_music_off(self.theme_mode)
        else:
            self.MusicButton.update_theme_music_on(self.theme_mode)
        for btn in self.about_buttons:
            btn.update_theme(theme_name)

    def update_selected_song(self, song_path: str):
        self.current_song = song_path
        print(f"Song updated: {self.current_song}")

    def TurnOnOffMusic(self):
        if not self.music_playing:
            if not hasattr(self, 'current_song'):
                QMessageBox.warning(self, 'No song selected', 'Please go to settings and select a song.')
            else:
                self.MusicButton.update_theme_music_on(self.theme_mode)
                self.player.setSource(QUrl.fromLocalFile(self.current_song))
                self.player.play()
                self.music_playing = True
        else:
            self.MusicButton.update_theme_music_off(self.theme_mode)
            self.player.stop()
            self.music_playing = False
        
    def OpenHomePageSection(self):          self.ui.stackedWidget.setCurrentWidget(self.ui.homepage_ui.HomePage)
    def OpenHelpPage(self):                 self.ui.stackedWidget.setCurrentWidget(self.ui.help_ui.HelpPage)
    def OpenSettingsPage(self):             self.ui.stackedWidget.setCurrentWidget(self.ui.settings_ui.SettingsPage)

    """ASYMMETRIC SECTION"""
    def OpenAsymmetricSection(self):        self.ui.stackedWidget.setCurrentWidget(self.ui.asymmetric_ui.AsymmetricPage)
    def OpenCSRWindow(self):                self.csr =          CSRWindow(self.theme_mode);                 self.csr.show()
    def OpenDHKeyExchangeWindow(self):      self.dhke =         DHKeyExchangeWindow(self.theme_mode);       self.dhke.show()
    def OpenDSAWindow(self):                self.dsa =          DSAWindow(self.theme_mode);                 self.dsa.show()
    def OpenElGamalWindow(self):            self.elgamal =      ElGamalWindow(self.theme_mode);             self.elgamal.show()
    def OpenRSAWienerAttackWindow(self):    self.rsawa =        RSAWienerAttackWindow(self.theme_mode);     self.rsawa.show()
    def OpenRSAWindow(self):                self.rsa =          RSAWindow(self.theme_mode);                 self.rsa.show()
    def OpenX509SelfSignedCertWindow(self): self.x509 =         X509SelfSignedWindow(self.theme_mode);      self.x509.show()
    def OpenCramerShoupEncWindow(self):     self.csenc =        CramerShoupEncryptWindow(self.theme_mode);  self.csenc.show()
    def OpenCramerShoupDecWindow(self):     self.csdec =        CramerShoupDecryptWindow();                 self.csdec.show()
    def OpenPaillierEncWindow(self):        self.paillierenc =  PaillierEncWindow(self.theme_mode);         self.paillierenc.show()
    def OpenPaillierDecWindow(self):        self.paillierdec =  PaillierDecWindow(self.theme_mode);         self.paillierdec.show()
    def OpenECDSAWindow(self):              self.ecdsa =        ECDSAWindow(self.theme_mode);               self.ecdsa.show()
    def OpenECDHWindow(self):               self.ecdh =         ECDHWindow(self.theme_mode);                self.ecdh.show()
    def OpenEdDSAWindow(self):              self.eddsa =        EdDSAWindow(self.theme_mode);               self.eddsa.show()
    def OpenNTRUEncryptWindow(self):        self.ntruencrypt =  NTRUEncryptWindow(self.theme_mode);         self.ntruencrypt.show()
    def OpenKyberKEMWindow(self):           self.kyberkem =     KyberKEMWindow(self.theme_mode);            self.kyberkem.show()
    def OpenKyberKEMDecWindow(self):        self.kyberkemdec =  KyberKEMDecWindow(self.theme_mode);         self.kyberkemdec.show()

    """SYMMETRIC SECTION"""
    def OpenSymmetricSection(self):         self.ui.stackedWidget.setCurrentWidget(self.ui.symmetric_ui.SymmetricPage)
    def OpenAESEncryptionWindow(self):      self.aesenc =       AESEncryptionWindow(self.theme_mode);          self.aesenc.show()
    def OpenAESDecryptionWindow(self):      self.aesdec =       AESDecryptionWindow(self.theme_mode);          self.aesdec.show()
    def OpenDESEncryptionWindow(self):      self.desenc =       DESEncryptionWindow(self.theme_mode);          self.desenc.show()
    def OpenDESDecryptionWindow(self):      self.desdec =       DESDecryptionWindow(self.theme_mode);          self.desdec.show()
    def OpenBlowfishWindow(self):           self.blowfish =     BlowfishWindow(self.theme_mode);               self.blowfish.show()
    def OpenCamelliaWindow(self):           self.camellia =     CamelliaWindow(self.theme_mode);               self.camellia.show()
    def OpenRC2EncryptionWindow(self):      self.rc2enc =       RC2EncryptionWindow(self.theme_mode);          self.rc2enc.show()
    def OpenRC2DecryptionWindow(self):      self.rc2dec =       RC2DecryptionWindow(self.theme_mode);          self.rc2dec.show()
    def OpenRC5EncryptionWindow(self):      self.rc5enc =       RC5EncryptionWindow();          self.rc5enc.show()
    def OpenRC5DecryptionWindow(self):      self.rc5dec =       RC5DecryptionWindow();          self.rc5dec.show()
    def OpenSerpentWindow(self):            self.serpent =      SerpentWindow();                self.serpent.show()
    def Open3DESEncryptionWindow(self):     self.tripledesenc = TripleDESEncryptionWindow(self.theme_mode);    self.tripledesenc.show()
    def Open3DESDecryptionWindow(self):     self.tripledesdec = TripleDESDecryptionWindow(self.theme_mode);    self.tripledesdec.show()
    def OpenTwofishWindow(self):            self.twofish =      TwofishWindow(self.theme_mode);                self.twofish.show()
    def OpenFernetWindow(self):             self.fernet =       FERNETWindow(self.theme_mode);  self.fernet.show()

    """CIPHERS SECTION"""
    def OpenCiphersSection(self):           self.ui.stackedWidget.setCurrentWidget(self.ui.ciphers_ui.CiphersPage)
    def OpenBaconCipherWindow(self):        self.bacon =        BaconCipherWindow(self.theme_mode);            self.bacon.show()
    def OpenCaesarCipherWindow(self):       self.caesar =       CaesarCipherWindow(self.theme_mode);           self.caesar.show()
    def OpenChaChaPolyWindow(self):         self.chachapoly =   ChaCha20Poly1305Window(self.theme_mode);       self.chachapoly.show()
    def OpenChaCha20Window(self):           self.chacha =       ChaCha20Window(self.theme_mode);               self.chacha.show()
    def OpenEnigmaMachineWindow(self):      self.enigma =       EnigmaMachineWindow(self.theme_mode);          self.enigma.show()
    def OpenGOSTMagmaWindow(self):          self.gostmagma =    GOSTMagmaWindow(self.theme_mode);              self.gostmagma.show()
    def OpenRabbitStreamCipherWindow(self): self.rabbit =       RabbitStreamCipherWindow(self.theme_mode);     self.rabbit.show()
    def OpenRC4EncryptionWindow(self):      self.rc4enc =       RC4EncryptionWindow(self.theme_mode);          self.rc4enc.show()
    def OpenRC4DecryptionWindow(self):      self.rc4dec =       RC4DecryptionWindow(self.theme_mode);          self.rc4dec.show()
    def OpenROT13Window(self):              self.rot13 =        ROT13Window(self.theme_mode);                  self.rot13.show()
    def OpenROT13BruteForceWindow(self):    self.rot13bf =      ROT13BFWindow(self.theme_mode);                self.rot13bf.show()
    def OpenROT47Window(self):              self.rot47 =        ROT47Window(self.theme_mode);                  self.rot47.show()
    def OpenROT47BruteForceWindow(self):    self.rot47bf =      ROT47BFWindow(self.theme_mode);                self.rot47bf.show()
    def OpenSimpleSubstitutionWindow(self): self.simplesub =    SimpleSubWindow(self.theme_mode);              self.simplesub.show()
    def OpenTEAWindow(self):                self.tea =          TEAWindow(self.theme_mode);                    self.tea.show()
    def OpenXTEAWindow(self):               self.xtea =         XTEAWindow(self.theme_mode);                   self.xtea.show()
    def OpenXXTEAWindow(self):              self.xxtea =        XXTEAWindow(self.theme_mode);                  self.xxtea.show()
    def OpenVigenereEncrptionWindow(self):  self.vigenereenc =  VigenereEncryptionWindow(self.theme_mode);     self.vigenereenc.show()
    def OpenVigenereDecrptionWindow(self):  self.vigeneredec =  VigenereDecryptionWindow(self.theme_mode);     self.vigeneredec.show()
    def OpenSM4EncryptWindow(self):         self.sm4encrypt =   SM4BlockCipherEncryptWindow(self.theme_mode);  self.sm4encrypt.show()
    def OpenSM4DecryptWindow(self):         self.sm4decrypt =   SM4BlockCipherDecryptWindow(self.theme_mode);  self.sm4decrypt.show()
    def OpenBifidCipherWindow(self):        self.bifid =        BifidCipherWindow(self.theme_mode);            self.bifid.show()
    def OpenAffineCipherEncWindow(self):    self.affinenc =     AffineCipherEncWindow(self.theme_mode);        self.affinenc.show()
    def OpenAffineCipherDecWindow(self):    self.affinedec =    AffineCipherDecWindow(self.theme_mode);        self.affinedec.show()

    """HASHING ALGORITHMS SECTION"""
    def OpenHashAlgoSection(self):          self.ui.stackedWidget.setCurrentWidget(self.ui.hashalgo_ui.HashAlgoPage)
    def OpenBcryptWindow(self):             self.bcrypt =       BcryptWindow(self.theme_mode);              self.bcrypt.show()
    def OpenBLAKE2Window(self):             self.blake2 =       BLAKE2Window(self.theme_mode);              self.blake2.show()
    def OpenBLAKE3Window(self):             self.blake3 =       BLAKE3Window(self.theme_mode);              self.blake3.show()
    def OpenMD4Window(self):                self.md4 =          MD4Window(self.theme_mode);                 self.md4.show()
    def OpenMD5Window(self):                self.md5 =          MD5Window(self.theme_mode);                 self.md5.show()
    def OpenRIPEMD160Window(self):          self.ripemd160 =    RIPEMD160Window(self.theme_mode);           self.ripemd160.show()
    def OpenSHA1Window(self):               self.sha1 =         SHA1Window(self.theme_mode);                self.sha1.show()
    def OpenSHA256Window(self):             self.sha256 =       SHA256Window(self.theme_mode);              self.sha256.show()
    def OpenSHA384Window(self):             self.sha384 =       SHA384Window(self.theme_mode);              self.sha384.show()
    def OpenSHA512Window(self):             self.sha512 =       SHA512Window(self.theme_mode);              self.sha512.show()
    def OpenWhirlpoolWindow(self):          self.whirlpool =    WhirlpoolWindow(self.theme_mode);           self.whirlpool.show()
    def OpenHashIdentifierWindow(self):     self.hashid =       HashIdentifierWindow(self.theme_mode);      self.hashid.show()
    def OpenGOSTHashFunctionWindow(self):   self.gosthf =       GOST34112012Window(self.theme_mode);        self.gosthf.show()
    def OpenTigerHasFunctionWindow(self):   self.tiger =        TigerHashFunctionWindow(self.theme_mode);   self.tiger.show()
    def OpenKeccakWindow(self):             self.kecc =         KeccakHash(self.theme_mode);                self.kecc.show()

    """ENCODERS SECTION"""
    def OpenEncodersSection(self):          self.ui.stackedWidget.setCurrentWidget(self.ui.encoders_ui.EncodersPage)
    def OpenA1Z26EncWindow(self):           self.a1z26enc =     A1Z26EncodeWindow(self.theme_mode);            self.a1z26enc.show()
    def OpenA1Z26DecWindow(self):           self.a1z26dec =     A1Z26DecodeWindow(self.theme_mode);            self.a1z26dec.show()
    def OpenBase32Window(self):             self.base32 =       BASE32Window(self.theme_mode);                 self.base32.show()
    def OpenBase45Window(self):             self.base45 =       BASE45Window(self.theme_mode);                 self.base45.show()
    def OpenBase58Window(self):             self.base58 =       BASE58Window(self.theme_mode);                 self.base58.show()
    def OpenBase62Window(self):             self.base62 =       BASE62Window(self.theme_mode);                 self.base62.show()
    def OpenBase64Window(self):             self.base64 =       BASE64Window(self.theme_mode);                 self.base64.show()
    def OpenBase85Window(self):             self.base85 =       BASE85Window(self.theme_mode);                 self.base85.show()
    def OpenBase92Window(self):             self.base92 =       BASE92Window(self.theme_mode);                 self.base92.show()
    def OpenBrailleWindow(self):            self.braille =      BrailleWindow(self.theme_mode);                self.braille.show()
    def OpenMorseCodeWindow(self):          self.morsecode =    MorseCodeWindow(self.theme_mode);              self.morsecode.show()
    def OpenURLEncodeWindow(self):          self.urlenc =       URLEncodeWindow(self.theme_mode);              self.urlenc.show()
    def OpenURLDecodeWindow(self):          self.urldec =       URLDecodeWindow(self.theme_mode);              self.urldec.show()
    def OpentexttoCharcodeWindow(self):     self.txttochrcd =   TexttoCharcodeWindow(self.theme_mode);         self.txttochrcd.show()
    def OpenCharcodetoTextWindow(self):     self.chrcdtotxt =   CharcodetoTextWindow(self.theme_mode);         self.chrcdtotxt.show()
    def OpenToQPWindow(self):               self.toqp =         ToQuotedPrintableWindow(self.theme_mode);      self.toqp.show()
    def OpenFromQPWindow(self):             self.fromqp =       FromQuotedPrintableWindow(self.theme_mode);    self.fromqp.show()

    """CONVERTERS SECTION"""
    def OpenConvertersSection(self):        self.ui.stackedWidget.setCurrentWidget(self.ui.converters_ui.ConvertersPage)
    def OpenTexttoOctalWindow(self):        self.txttooctal =   TexttoOctalWindow();            self.txttooctal.show()
    def OpenOctaltoTextWindow(self):        self.octaltotxt =   OctaltoTextWindow();            self.octaltotxt.show()
    def OpenTexttoBinaryWindow(self):       self.txttobin =     TexttoBinaryWindow();           self.txttobin.show()
    def OpenBinarytoTextWindow(self):       self.bintotxt =     BinarytoTextWindow();           self.bintotxt.show()
    def OpenTexttoASCIIWindow(self):        self.txttoascii =   TexttoASCIIWindow();            self.txttoascii.show()
    def OpenASCIItoTextWindow(self):        self.asciitotxt =   ASCIItoTextWindow();            self.asciitotxt.show()
    def OpenDecimaltoBinaryWindow(self):    self.decimaltobin = DecimaltoBinaryWindow();        self.decimaltobin.show()
    def OpenBinarytoDecimalWindow(self):    self.bintodecimal = BinarytoDecimalWindow();        self.bintodecimal.show()
    def OpenCodepointConverterWindow(self): self.cpconverter =  CodepointConverterWindow();     self.cpconverter.show()
    def OpenTxttoHexWindow(self):           self.txttohex =     TexttoHexWindow();              self.txttohex.show()
    def OpenHextoTxtWindow(self):           self.hextotxt =     HextoTextWindow();              self.hextotxt.show()
    def OpenDecToRadixWindow(self):         self.dectoradix =   DecimalToRadixWindow();         self.dectoradix.show()
    def OpenRadixToDecWindow(self):         self.radixtodec =   RadixToDecimalWindow();         self.radixtodec.show()
    def OpenDecimalToBCDWindow(self):       self.dectobcd =     DecimalToBCDWindow();           self.dectobcd.show()
    def OpenBCDToDecimalWindow(self):       self.bcdtodec =     BCDToDecimalWindow();           self.bcdtodec.show()
    def OpenHTMLEntitytoCharWindow(self):   self.htmlenttochr = HTMLEntityToCharWindow();       self.htmlenttochr.show()
    def OpenChartoHTMLEntityWindow(self):   self.chrtohtmlent = CharToHTMLEntityWindow();       self.chrtohtmlent.show()
    def OpenPEMtoDERWindow(self):           self.pemtoder =     PEMtoDERWindow();               self.pemtoder.show()
    def OpenDERtoPEMWindow(self):           self.dertopem =     DERtoPEMWindow();               self.dertopem.show()
    def OpenToUnixTimestampWindow(self):    self.tounix =       ToUnixTimestampWindow();        self.tounix.show()
    def OpenFromUnixTimestampWindow(self):  self.fromunix =     FromUnixTimestampWindow();      self.fromunix.show()
    def OpenToNatoWindow(self):             self.tonato =       ToNatoAlphabet();               self.tonato.show()
    def OpenFromNatoWindow(self):           self.fromnato =     FromNatoAlphabet();             self.fromnato.show()

    """CRYPTANALYSIS SECTION"""
    def OpenCryptanalysisSection(self):     self.ui.stackedWidget.setCurrentWidget(self.ui.cryptanalysis_ui.CryptanalysisPage)
    def OpenKPAWindow(self):                self.kpa =              KPA();                      self.kpa.show()
    def OpenCPAWindow(self):                self.cpa =              CPA();                      self.cpa.show()
    def OpenCOAWindow(self):                self.coa =              COA();                      self.coa.show()
    def OpenMITMWindow(self):               self.mitm =             MITM();                     self.mitm.show()
    def OpenACPAWindow(self):               self.acpa =             ACPA();                     self.acpa.show()
    def OpenBirthdayAWindow(self):          self.birthdayattack =   BirthdayAttack();           self.birthdayattack.show()
    def OpenSideChannelAWindow(self):       self.sca =              SCA();                      self.sca.show()
    def OpenBruteForceAWindow(self):        self.bfattack =         BruteForceAttack();         self.bfattack.show()
    def OpenDiffAnalysisWindow(self):       self.diff_analysis =    DifferentialCryptanalysis();self.diff_analysis.show()
    def OpenRelatedKeyAWindow(self):        self.rka =              RKA();                      self.rka.show()
    def OpenBoomerangAWindow(self):         self.boomeranga =       BoomerangAttack();          self.boomeranga.show()
    def OpenDaviesAttackWindow(self):       self.daviesattack =     DaviesAttack();             self.daviesattack.show()
    def OpenHarvestNowDLWindow(self):       self.hndl =             HNDL();                     self.hndl.show()
    def OpenIntegralCryptWindow(self):      self.intcrypt =         IntegralCryptanalysis();    self.intcrypt.show()
    def OpenLinearCryptanalysisWindow(self):self.linearcrypt =      LinearCryptanalysis();      self.linearcrypt.show()
    def OpenModNcryptanalysisWindow(self):  self.modn =             Mod_N();                    self.modn.show()
    def OpenSlideAttackWindow(self):        self.slideattack =      SlideAttack();              self.slideattack.show()
    def OpenXSLAttackWindow(self):          self.xslattack =        XSLattack();                self.xslattack.show()
    def OpenRainbowTableWindow(self):       self.rainbowtable =     RainbowTable();             self.rainbowtable.show()
    def OpenBlackBagCryptWindow(self):      self.blackbag =         BlackBagCryptanalysis();    self.blackbag.show()
    def OpenPowerAnalysisWindow(self):      self.poweranalysis =    PowerAnalysis();            self.poweranalysis.show()
    def OpenReplayAttackWindow(self):       self.replayattack =     ReplayAttack();             self.replayattack.show()
    def OpenRubberHoseCryptWindow(self):    self.rubberhose =       RubberHoseCryptanalysis();  self.rubberhose.show()
    def OpenTimingAnalysisWindow(self):     self.timinganalysis =   TimingAnalysis();           self.timinganalysis.show()

    """FILE HANDLING SECTION"""
    def OpenFileHandlingSection(self):      self.ui.stackedWidget.setCurrentWidget(self.ui.filehandling_ui.FileHandlingPage)
    def OpenFernetFileEncWindow(self):      self.fernetenc =    FernetFileEncWindow(self.theme_mode);          self.fernetenc.show()
    def OpenFernetFileDecWindow(self):      self.fernetdec =    FernetFileDecWindow(self.theme_mode);          self.fernetdec.show()
    def OpenCSVtoJSONWindow(self):          self.csvtojson =    CSVtoJSONWindow(self.theme_mode);              self.csvtojson.show()
    def OpenJSONtoCSVWindow(self):          self.jsontocsv =    JSONtoCSVWindow(self.theme_mode);              self.jsontocsv.show()
    def OpenImg2PDFWindow(self):            self.img2pdf =      Img2PDFWindow(self.theme_mode);                self.img2pdf.show()
    def OpenPDF2ImgWindow(self):            self.pdf2img =      PDF2ImgWindow(self.theme_mode);                self.pdf2img.show()
    def OpenExifImagesWindow(self):         self.exifimg =      ExifImageWindow(self.theme_mode);              self.exifimg.show()
    def OpenZipFileWithPwdWindow(self):     self.zipfile =      ZipFileWithPwdWindow(self.theme_mode);         self.zipfile.show()
    def OpenZipFolderWithPwdWindow(self):   self.zipfolder =    ZipFolderWithPwdWindow(self.theme_mode);       self.zipfolder.show()
    def OpenBfPwdProtectedFilesWindow(self):self.bfpwd =        BfPwdProtectedFilesWindow(self.theme_mode);    self.bfpwd.show()
    def OpenDisExeFilesWindow(self):        self.disexe =       DisassembleExeFilesWindow(self.theme_mode);    self.disexe.show()
    def OpenDecompilePycFilesWindow(self):  self.decpyc =       DecompilePycFilesWindow(self.theme_mode);      self.decpyc.show()
    def OpenJSONtoMsgPackWindow(self):      self.jsonmsgpack =  JSONtoMsgPackWindow(self.theme_mode);          self.jsonmsgpack.show()
    def OpenMsgPacktoJSONWindow(self):      self.msgpackjson =  MsgPacktoJSONWindow(self.theme_mode);          self.msgpackjson.show()
    def OpenJSONtoXMLWindow(self):          self.jsontoxml =    JSONtoXMLWindow(self.theme_mode);              self.jsontoxml.show()
    def OpenXMLtoJSONWindow(self):          self.xmltojson =    XMLtoJSONWindow(self.theme_mode);              self.xmltojson.show()
    def OpenPyCodeDisassemblerWindow(self): self.pycdis =       PyCodeDisassemblerWindow(self.theme_mode);     self.pycdis.show()
    def OpenFileTypeDetectorWindow(self):   self.ftdetector =   FileTypeDetectorWindow(self.theme_mode);       self.ftdetector.show()
    def OpenPGPEncryptorWindow(self):       self.pgpenc =       PGPEncryptWindow(self.theme_mode);             self.pgpenc.show()
    def OpenPGPDecryptorWindow(self):       self.pgpdec =       PGPDecryptWindow(self.theme_mode);             self.pgpdec.show()

    """OTHER TOOLS SECTION"""
    def OpenOtherToolsSection(self):        self.ui.stackedWidget.setCurrentWidget(self.ui.othertools_ui.OtherToolsPage)        
    def OpenCircularBitShiftWindow(self):   self.circbitshift = CircularBitShiftWindow(self.theme_mode);       self.circbitshift.show()
    def OpenFrequencyAnalysisWindow(self):  self.freqanalysis = FrequencyAnalysisWindow(self.theme_mode);      self.freqanalysis.show()
    def OpenOneTimePadWindow(self):         self.otp =          OneTimePadWindow(self.theme_mode);             self.otp.show()
    def OpenPBKDF2Window(self):             self.pbkdf2 =       PBKDF2Window(self.theme_mode);                 self.pbkdf2.show()
    def OpenPrimeNumGeneratorWindow(self):  self.primenumgen =  PrimeNumGenWindow(self.theme_mode);            self.primenumgen.show()
    def OpenPRNGeneratorWindow(self):       self.prng =         PRNGWindow(self.theme_mode);                   self.prng.show()
    def OpenStrongPwdGeneratorWindow(self): self.pwdgen =       PwdGeneratorWindow(self.theme_mode);           self.pwdgen.show()
    def OpenRSAKeyGeneratorWindow(self):    self.rsakeygen =    RSAKeyGenWindow(self.theme_mode);              self.rsakeygen.show()
    def OpenScryptWindow(self):             self.scrypt =       ScryptWindow(self.theme_mode);                 self.scrypt.show()
    def OpenXOROperationWindow(self):       self.xor =          XOROperationWindow(self.theme_mode);           self.xor.show()
    def OpenASN1EncodeWindow(self):         self.asn1enc =      ASN1EncodeWindow(self.theme_mode);             self.asn1enc.show()
    def OpenASN1DecodeWindow(self):         self.asn1dec =      ASN1DecodeWindow(self.theme_mode);             self.asn1dec.show()
    def OpenIntFactorWindow(self):          self.intfactor =    IntFactorizationWindow(self.theme_mode);       self.intfactor.show()
    def OpenSwapEndianessWindow(self):      self.swapendian =   SwapEndianessWindow(self.theme_mode);          self.swapendian.show()
    def OpenReverseTextWindow(self):        self.rvrstxt =      ReverseTextWindow(self.theme_mode);            self.rvrstxt.show()
    def OpenHMACWindow(self):               self.hmac =         HMACWindow(self.theme_mode);                   self.hmac.show()
    def OpenArgon2Window(self):             self.argon2 =       Argon2Window(self.theme_mode);                 self.argon2.show()
    def OpenShowOnMapWindow(self):          self.showonmap =    ShowOnMapWindow(self.theme_mode);              self.showonmap.show()
    def OpenShowOnMap2Window(self):         self.showonmap2 =   ShowOnMap2Window(self.theme_mode);             self.showonmap2.show()
    def OpenECKeyPairWindow(self):          self.eckeypair =    EllipticCurveKeyPairWindow(self.theme_mode);   self.eckeypair.show()
    def OpenEntropyWindow(self):            self.entropy =      EntropyWindow(self.theme_mode);                self.entropy.show()
    def OpenDataDifferencingWindow(self):   self.datadiff =     DataDifferencingWindow(self.theme_mode);       self.datadiff.show()
    def OpenDataCompressionWindow(self):    self.datacomp =     DataCompressionWindow(self.theme_mode);        self.datacomp.show()
    def OpenRandomnessTesterWindow(self):   self.randtester =   RandomnessTesterWindow(self.theme_mode);       self.randtester.show()
    def OpenPGPKeyPairGenerateWindow(self): self.pgpkeypair =   PGPKeyPairGenerateWindow(self.theme_mode);     self.pgpkeypair.show()
    def OpenDSAKeyPairGenerateWindow(self): self.dsakeypair =   DSAKeyPairGenerateWindow(self.theme_mode);     self.dsakeypair.show()
    def OpenEdDSAKeyPairGenWindow(self):    self.eddsakeypair = EdDSAKeyPairWindow(self.theme_mode);           self.eddsakeypair.show()
    def OpenLoremIpsumGenWindow(self):      self.loremipsum =   LoremIpsumGenerateWindow(self.theme_mode);     self.loremipsum.show()
    def OpenModCalcWindow(self):            self.modcalc =      ModCalculatorWindow(self.theme_mode);          self.modcalc.show()
    def OpenJWTSignWindow(self):            self.jwtsign =      JWTSignWindow(self.theme_mode);                self.jwtsign.show()
    def OpenJWTVerifyWindow(self):          self.jwtverify =    JWTVerifyWindow(self.theme_mode);              self.jwtverify.show()
    def OpenJWTDecodeWindow(self):          self.jwtdecode =    JWTDecodeWindow(self.theme_mode);              self.jwtdecode.show()
    def OpenGenQRcodeWindow(self):          self.generateqr =   GenerateQRcode(self.theme_mode);               self.generateqr.show()

try:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.setStyleSheet("QWidget { background-color: #3B3B3B; color: white; }")
        widget = MainWindow()
        widget.qapp = app # reference
        widget.show()
        sys.exit(app.exec())
except Exception as e:
    raise ValueError(f"An error occured: {e}")
