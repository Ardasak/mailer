from re import S
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6 import QtGui
import sys
import smtplib, ssl
from styles import styles_black_background
from email_validator import validate_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import configparser

config = configparser.ConfigParser()

config.read("account.ini")

email = config.get("ACCOUNT","email")
password = config.get("ACCOUNT","password")
provider = config.get("ACCOUNT", "provider")
provider_port = config.get("ACCOUNT", "provider_port")

context = ssl.create_default_context()

def validate(email):
    try:
        validate_email(email)
        return 1
    except:
        return 0

def logout():
    if not (email == "" or password == ""):
        config["ACCOUNT"] = {
            "email" : "",
            "password": "",
            "provider": "",
            "provider_port": ""
        }
        with open('account.ini', 'w') as configfile:
            config.write(configfile)
        exit()
    else:
        message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "Already logged out.")

def message_box(icon, buttons, title, text):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setStandardButtons(buttons)
    msg.setWindowTitle(title)
    return msg.exec()

    
class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.init()


    def init(self):
        self.attached = 0
        self.preferences = ["Group","Personal"]

        self.send_button = QPushButton()
        self.send_button.setStyleSheet(
            styles_black_background.button_new_page_style
        )
        send_icon = QtGui.QPixmap("icon/send-message.png")
        self.send_button.setIcon(QtGui.QIcon(send_icon))
        self.send_button.setIconSize(QtCore.QSize(32, 32))
        self.send_button.clicked.connect(self.send_mail)

        self.clear_button = QPushButton()
        self.clear_button.setStyleSheet(
            styles_black_background.button_new_page_style
        )
        trash_icon = QtGui.QPixmap("icon/trash.png")
        self.clear_button.setIcon(QtGui.QIcon(trash_icon))
        self.clear_button.setIconSize(QtCore.QSize(32, 32))
        self.clear_button.clicked.connect(self.clear_all)

        self.attach_file_button = QPushButton()
        self.attach_file_button.setStyleSheet(styles_black_background.button_new_page_style)
        attach_icon = QtGui.QPixmap("icon/attachment.png")
        self.attach_file_button.setIcon(QtGui.QIcon(attach_icon))
        self.attach_file_button.setIconSize(QtCore.QSize(32, 32))
        self.attach_file_button.clicked.connect(self.attach_file)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(styles_black_background.list_style)
        font = self.list_widget.font()
        font.setPointSize(12)
        self.list_widget.setFont(font)
        self.list_widget.itemClicked.connect(self.clicked_item)

        self.subject_area = QLineEdit()
        self.subject_area.setPlaceholderText("Subject: ")
        self.subject_area.setStyleSheet(styles_black_background.subject_and_mail_style)
        font = self.subject_area.font()
        font.setPointSize(12)
        self.subject_area.setFont(font)

        self.message_area = QTextEdit()
        self.message_area.setPlaceholderText("Message: ")
        self.message_area.setStyleSheet(styles_black_background.subject_and_mail_style)

        self.add_button = QPushButton()
        self.add_button.setStyleSheet(styles_black_background.add_button_style)
        add_icon = QtGui.QPixmap("icon/plus.png")
        self.add_button.setIcon(QtGui.QIcon(add_icon))
        self.add_button.setIconSize(QtCore.QSize(32, 32))
        self.add_button.clicked.connect(self.add_item)

        self.add_from_txt_button = QPushButton()
        self.add_from_txt_button.setStyleSheet(styles_black_background.add_button_style)
        add_from_txt_icon = QtGui.QPixmap("icon/txt-file.png")
        self.add_from_txt_button.setIcon(QtGui.QIcon(add_from_txt_icon))
        self.add_from_txt_button.setIconSize(QtCore.QSize(32, 32))
        self.add_from_txt_button.clicked.connect(self.add_from_txt_file)

        self.delete_button = QPushButton()
        self.delete_button.setStyleSheet(styles_black_background.button_new_page_style)
        delete_icon = QtGui.QPixmap("icon/delete.png")
        self.delete_button.setIcon(QtGui.QIcon(delete_icon))
        self.delete_button.setIconSize(QtCore.QSize(32, 32))
        self.delete_button.clicked.connect(self.delete_item)

        self.edit_button = QPushButton()
        self.edit_button.setStyleSheet(styles_black_background.button_new_page_style)
        edit_icon = QtGui.QPixmap("icon/edit.png")
        self.edit_button.setIcon(QtGui.QIcon(edit_icon))
        self.edit_button.setIconSize(QtCore.QSize(32, 32))
        self.edit_button.clicked.connect(self.edit_item)

        self.email_add_field = QLineEdit()
        self.email_add_field.setPlaceholderText("Email: ")
        self.email_add_field.setStyleSheet(styles_black_background.search_field_style)
        font = self.email_add_field.font()
        font.setPointSize(12)
        self.email_add_field.setFont(font)

        self.preference_combobox = QComboBox()
        self.preference_combobox.setStyleSheet(styles_black_background.combobox_style)
        self.preference_combobox.addItems(self.preferences)


        self.main_v_box = QVBoxLayout()
        self.top_placement()
        self.center_placement()
        self.bottom_placement()
        self.setLayout(self.main_v_box)

    def add_from_txt_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Open File", "", "TXT Files (*.txt*)")
        line_set = {}
        line_set = set(line_set)
        with open(self.file[0], 'r') as f:
            for line in f:
                line = line.replace("\n", "")
                line_set.add(line)
                
        for line in line_set:
            self.list_widget.addItem(line)

    def attach_file(self):
        if not (self.attached):
            self.file = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
            if self.file[0]!="":
                self.attached = 1
                self.attach_file_button.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/attachment-remove.png")))
                return
            self.attached = 0
        elif self.attached:
            self.file = ""
            self.attached = 0
            self.attach_file_button.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/attachment.png")))


    def clicked_item(self):
        self.email_add_field.setText(self.list_widget.currentItem().text())
    
    def get_mail_list(self):
        mail_list = []
        for index in range(self.list_widget.count()):
            mail_list.append(self.list_widget.item(index).text())
        return mail_list

    def send_mail(self):
        try:
            subject = self.subject_area.text()
            message_text = self.message_area.toPlainText()
            server = smtplib.SMTP(provider, provider_port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(email, password)
            mail_list = self.get_mail_list()
            for mail in mail_list:
                message = MIMEMultipart()
                message["Subject"] = subject
                message["From"] = email
                message["To"] = mail
                text = message_text
                mtext = MIMEText(text, "plain")
                message.attach(mtext)
                if self.attached == 1:
                    file = MIMEApplication(open(self.file[0], 'rb').read())
                    path_list = self.file[0].split("/")
                    file.add_header('Content-Disposition','attachment',filename=path_list[-1])
                    message.attach(file)

                text = message.as_string()
                if(self.preference_combobox.currentText()=="Group"):
                    server.sendmail(email, mail_list, text)
                    break
                else:
                    server.sendmail(email, mail, text)
            server.quit()
            self.attached = 0
            self.attach_file_button.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/attachment.png")))
            self.clear_fields()
        except smtplib.SMTPAuthenticationError:
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok,"Error", "It looks like we can't send mails with the infos you provide, try logging in again. Make sure the infos are correct.")
            logout()
        except ssl.SSLCertVerificationError:
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok ,"Error", "SSL certificate verify failed.")
        except: 
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "An error occured while sending the email.")

    def clear_fields(self):
        self.list_widget.clear()
        self.email_add_field.clear()
        self.subject_area.clear()
        self.message_area.clear()

    def add_item(self):
        if(validate(self.email_add_field.text())):
            self.list_widget.addItem(self.email_add_field.text())
            self.email_add_field.clear()
        else:
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "Please check the validity of the email address")

    def edit_item(self):
        index = self.list_widget.currentRow()
        if index == -1:
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "Please select an item to edit.")
            return
        if(validate(self.email_add_field.text())):
            self.list_widget.takeItem(index)
            self.list_widget.insertItem(index, self.email_add_field.text())
            self.email_add_field.clear()

    def delete_item(self):
        item = self.list_widget.takeItem(self.list_widget.currentRow())
        if item == None:
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "Please select an item to delete.")
            return
        self.list_widget.removeItemWidget(item)
        self.email_add_field.clear()

    def clear_all(self):
        if self.get_mail_list() == [] and self.subject_area.text() == '' and self.message_area.toPlainText() == '':
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "There is nothing to clear.")
            return
            
        result = message_box(QMessageBox.Icon.Warning, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,"Warning", "Are you sure you want to clear all the fields?")
        if result == 16384:
            self.clear_fields()
    

    def top_placement(self):
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.email_add_field)
        top_layout.addWidget(self.add_button)
        top_layout.addWidget(self.add_from_txt_button)
        top_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_v_box.addLayout(top_layout)

    def center_placement(self):
        self.main_v_box.addWidget(self.list_widget)
        self.main_v_box.addWidget(self.subject_area)
        self.main_v_box.addWidget(self.message_area)

    def bottom_placement(self):
        combobox_h_box = QHBoxLayout()
        combobox_h_box.addWidget(self.preference_combobox)
        combobox_h_box.addWidget(self.attach_file_button)
        combobox_h_box.addWidget(self.delete_button)
        combobox_h_box.addWidget(self.edit_button)
        buttons_h_box = QHBoxLayout()
        buttons_h_box.addWidget(self.clear_button)
        buttons_h_box.addWidget(self.send_button)
        v_box = QVBoxLayout()
        v_box.addLayout(combobox_h_box)

        v_box.addLayout(buttons_h_box)
        v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_box.addLayout(v_box)

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.init()
    
    def init(self):
        self.providers = ["--- Choose Provider ---","Office 365", "Microsoft", "Google", "Other"]
        self.providers_combobox = QComboBox()
        self.providers_combobox.setStyleSheet(styles_black_background.combobox_style)
        self.providers_combobox.addItems(self.providers)

        self.providers_combobox.currentIndexChanged.connect(self.changed)

        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email: ")
        self.email_field.setStyleSheet(styles_black_background.login_style)

        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Password: ")
        self.password_field.setStyleSheet(styles_black_background.login_style)
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.provider_server = QLineEdit()
        self.provider_server.setPlaceholderText("SMTP Server Address: (e.g. mail.yoursite.com)")
        self.provider_server.setStyleSheet(styles_black_background.login_style)
        self.provider_server.setVisible(False)

        self.provider_port = QLineEdit()
        self.provider_port.setPlaceholderText("SMTP Port: (default: 587)")
        self.provider_port.setStyleSheet(styles_black_background.login_style)
        self.provider_port.setVisible(False)

        self.save_check = QCheckBox("Save")
        self.save_check.setStyleSheet(styles_black_background.check_style)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(styles_black_background.login_style)

        self.h_box = QHBoxLayout()
        self.h_box.addWidget(self.save_check, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.h_box.addWidget(self.login_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)


        self.main_box = QVBoxLayout()
        self.main_box.addWidget(self.email_field)
        self.main_box.addWidget(self.password_field)
        self.main_box.addWidget(self.providers_combobox, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.main_box.addWidget(self.provider_server)
        self.main_box.addWidget(self.provider_port)
        self.main_box.addLayout(self.h_box)

        self.main_box.addStretch()

        self.setLayout(self.main_box)
    def changed(self):
        self.email_field.clear()
        self.password_field.clear()
        self.provider_server.clear()
        self.provider_port.clear()
        self.provider_server.setVisible(False)
        self.provider_port.setVisible(False)
        if(self.providers_combobox.currentText() == "--- Choose Provider ---"):
            self.email_field.setPlaceholderText("Email: ")
        elif(self.providers_combobox.currentText() == "Office 365"):
            self.email_field.setPlaceholderText("Email: (e.g. example@office365.com)")
        elif(self.providers_combobox.currentText() == "Microsoft"):
            self.email_field.setPlaceholderText("Email: (e.g. example@outlook.com, example@hotmail.com)")
        elif(self.providers_combobox.currentText() == "Google"):
            self.email_field.setPlaceholderText("Email: (e.g. example@gmail.com, example@googlemail.com)")
        elif(self.providers_combobox.currentText() == "Other"):
            self.email_field.setPlaceholderText("Email: (e.g. example@yoursite.com, example@yandex.ru)")
            self.provider_server.setVisible(True)
            self.provider_port.setVisible(True)
            

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStyleSheet("background-color: rgba(255, 255, 255, .1);")
        self.initMenubar()
        if(email == "" or password == ""):
            self.startLoginMenu()
        else:
            self.startMainMenu()

    def startMainMenu(self):
        self.window = Window(self)
        self.setWindowTitle("Mailer GUI")
        self.setCentralWidget(self.window)
        self.showMaximized()
    
    def startLoginMenu(self):
        self.window = LoginWindow(self)
        self.window.login_button.clicked.connect(lambda: self.login(self.window.email_field.text(), self.window.password_field.text(), self.window.providers_combobox.currentText(), self.window.provider_server.text(), self.window.provider_port.text(), self.window.save_check.isChecked()))
        self.setWindowTitle("Login")
        self.setCentralWidget(self.window)
        self.showMaximized()

    def login(self, email_input, password_input, provider_input, provider_server, provider_port_input, is_checked):
        self.all_login_checks(email_input, password_input, provider_input, provider_server, provider_port_input)
        if is_checked:
            config["ACCOUNT"] = {
                "email" : email,
                "password": password,
                "provider": provider,
                "provider_port": provider_port
            }
            with open('account.ini', 'w') as configfile:
                config.write(configfile)
        
        
    def all_login_checks(self, email_input, password_input, provider_input, provider_server, provider_port_input):
        global email
        global password
        global provider
        global provider_port
        if validate(email_input) and password_input!="":
            email = email_input
            password = password_input
            if provider_input == "Office 365":
                provider = "smtp.office365.com"
                provider_port = 587
            elif provider_input == "Microsoft":
                provider = "smtp-mail.outlook.com"
                provider_port = 587
            elif provider_input == "Google":
                provider = "smtp.gmail.com"
                provider_port = 587
            elif provider_input == "Other":
                if provider_server != "":
                    provider = provider_server
                else:
                    message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok,"Error", "SMTP Server Address can not be empty.")
                    return
                try:
                    provider_port_input = int(provider_port_input)
                    if provider_port_input != "":
                        provider_port = provider_port_input
                    else:
                        provider_port = 587
                except ValueError:
                    message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok,"Error", "SMTP port must be an integer value.")
                    return
            else:
                message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok,"Error", "Please choose a provider.")
                return
            try:
                server = smtplib.SMTP(provider, provider_port)
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(email, password)
            except:
                message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "Can't login.")
                return
            self.startMainMenu()
        else:
            message_box(QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok, "Error", "Please enter a valid email or password.")
    def initMenubar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(styles_black_background.menubar_style)

        options_menu = menubar.addMenu("&Options")
        options_menu.setStyleSheet(styles_black_background.menu_style)

        logoutAct = QtGui.QAction(self, text="&Logout")
        logoutAct.setStatusTip('Logout from the account.')
        logoutAct.triggered.connect(logout)

        options_menu.addAction(logoutAct)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())