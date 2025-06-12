from PyQt6.QtWidgets                import QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from .file_conversion               import FileConversionWindow
from capstone                       import *
from capstone.x86                   import *
import os, pefile, json

class DisassembleExeFilesWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Disassemble .exe files tool"
        about_text = ("<p>This tool allows you to analyze and disassemble Windows executable files (<code>.exe</code>) "
    "by extracting and decoding the raw machine instructions from their main code section.</p>"

    "<h3>Key Features:</h3>"
    "<ul>"
    "<li><b>Automatic Architecture Detection:</b> Supports both 32-bit and 64-bit executables using Capstone engine.</li>"
    "<li><b>Readable Output:</b> Converts raw binary instructions into human-readable assembly instructions.</li>"
    "<li><b>Flexible Export Options:</b> Save the disassembled output in <code>.json</code>, <code>.txt</code>, or <code>.xml</code> formats.</li>"
    "<li><b>Built-in Viewer:</b> View the disassembly result directly within the application before saving.</li>"
    "<li><b>Easy Access:</b> Output files are automatically saved to your Downloads folder for convenience.</li>"
    "</ul>"

    "<h3>Technical Details:</h3>"
    "<ul>"
    "<li>Uses <code>pefile</code> to parse the Portable Executable structure.</li>"
    "<li>Leverages <code>capstone</code> for lightweight and fast disassembly of x86 instructions.</li>"
    "<li>Only disassembles the main code section determined using the PE's base of code.</li>"
    "</ul>"

    "<p>This tool is ideal for reverse engineers, malware analysts, or security researchers looking for a simple "
    "and effective way to inspect .exe binaries without needing full-featured platforms like IDA or Ghidra.</p>")
        
        ax, ay, aw, ah = 650, 650, 50, 50
        file_filter = ".exe files (*.exe)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Disassemble .exe files")
        self.setFixedSize(700, 700)

        select_file_button = DefaultButtonStyle(
            'Select a .exe file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(10, 50, 230, 50)

        # Output file format
        output_format_label = QLabel("Output file format:", parent=self)
        output_format_label.setGeometry(300, 10, 130, 50)
        self.output_format_options = DefaultQComboBoxStyle(
            parent=self, 
            items=['.json', '.txt', '.xml'])
        self.output_format_options.setGeometry(300, 50, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.disassemble_file)
        submit_button.setGeometry(500, 50, 100, 50)

        self.data_label = QTextEdit(parent=self)
        self.data_label.setGeometry(10, 130, 680, 500)
        self.data_label.setReadOnly(True)
        self.data_label.hide()

    def disassemble_file(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension in ['.exe']:
                    # Get preferred output format
                    output_file_format = self.output_format_options.currentText()
                    output_extension = output_file_format.strip('.')
                    file_path = os.path.join(self.downloads_path, f'disassembled_file.{output_extension}')

                    try:
                        # Parse the .exe file
                        exe = pefile.PE(self.selected_file)
                        try:
                            result = self.fine_disassemble(exe)
                            self.data_label.clear()
                            formatted_result = "<br>".join(result)
                            self.data_label.setHtml(f"<b>Data (instructions):</b><br>{formatted_result}")
                            self.data_label.show()
                        except Exception as disassembly_error:
                            QMessageBox.critical(self, 'Disassembly Error', f'Error in disassembling file:\n{str(disassembly_error)}')
                        try:    
                            # Save disassembly in preferred format
                            with open(file_path, 'w', encoding='utf-8') as file:
                                if output_file_format == '.json':
                                    json.dump(result, file, indent=4)
                                elif output_file_format == '.txt':
                                    file.write("\n".join(result))
                                elif output_file_format == '.xml':
                                    file.write("<disassembly>\n")
                                    for line in result:
                                        file.write(f"    <instruction>{line}</instruction>\n")
                                    file.write("</disassembly>\n")
                                else:
                                    file.write("\n".join(result))  # Fallback to plain text if the format is unrecognized

                        except Exception as save_error:
                            QMessageBox.critical(self, 'Save Error', f'Failed to save file:\n{str(save_error)}')
                    except Exception as parse_error:
                        QMessageBox.critical(self, 'Parse Error', f'PE file parsing failed: {str(parse_error)}')

                    # Show a message box to confirm file save location
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Operation Successful')
                    msg_box.setText(f'File saved at: {file_path}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                    # Add a button to open the Downloads folder
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    # Open Downloads folder if selected
                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()
                else:
                    QMessageBox.warning(self, 'Invalid File Type', 'Please select a .exe file for conversion.')
            except Exception as e:
                QMessageBox.critical(self, 'Operation Failed', f'An error occurred: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

# https://isleem.medium.com/create-your-own-disassembler-in-python-pefile-capstone-754f863b2e1c
    def fine_disassemble(self, exe):
        try:
            data_list = []
            #get main code section
            main_code = self.get_main_code_section(exe.sections, exe.OPTIONAL_HEADER.BaseOfCode)
            #define architecutre of the machine 
            is_64bit = exe.FILE_HEADER.Machine == 0x8664
            md = Cs(CS_ARCH_X86, CS_MODE_64 if is_64bit else CS_MODE_32)
            md.detail = True
            last_address = 0
            last_size = 0
            #Beginning of code section
            begin = main_code.PointerToRawData
            #the end of the first continuous bloc of code
            end = begin+main_code.SizeOfRawData
            while True:
                #parse code section and disassemble it
                data = exe.get_memory_mapped_image()[begin:end]
                for i in md.disasm(data, begin):
                    data_list.append(f"{i.address:x}: {i.mnemonic} {i.op_str}")
                    last_address = int(i.address)
                    last_size = i.size
                #sometimes you need to skip some bytes
                begin = max(int(last_address),begin)+last_size+1
                if begin >= end:
                    return data_list
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpeted Error', str(e))
    
    #the function takes two arguments, both are fetched from the exe file using
    #pefile. the first one is the list of all sections. The second one is the
    #address of the first instruction in the program
    def get_main_code_section(self, sections, base_of_code):
        addresses = []
        #get addresses of all sections
        for section in sections: 
            addresses.append(section.VirtualAddress)

        #if the address of section corresponds to the first instruction then
        #this section should be the main code section
        if base_of_code in addresses:    
            return sections[addresses.index(base_of_code)]
        #otherwise, sort addresses and look for the interval to which the base of code
        #belongs
        else:
            addresses.append(base_of_code)
            addresses.sort()
            if addresses.index(base_of_code)!= 0:
                return sections[addresses.index(base_of_code)-1]
            else:
                #this means we failed to locate it
                return None
