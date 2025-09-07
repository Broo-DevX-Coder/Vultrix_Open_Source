import asyncio
import os
import re
import sys

from PySide2.QtWidgets import *
import qasync
from numpy import random

from Data import ASSETS_ICONS_ICO

from .utils import QSS_BINANCE_STYLE
from Data import CipherUserData,USERS_FILE,get_account_info,set_user_data
from web_pages import pup_message
from Data import logs
import logging
from PySide2.QtGui import QIcon

logging.info("The program started, ready to login/register/without-login")

class OpenProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.size_ = [350, 290, 130, 170]
        self.setFixedSize(self.size_[0], self.size_[2])
        self.setWindowTitle("Veltrix")
        self.setStyleSheet(QSS_BINANCE_STYLE)
        self.setWindowIcon(QIcon(os.path.join(ASSETS_ICONS_ICO,"main.ico")))

        # --- set stack -----
        self.stacked = QStackedWidget(self)
        self.stacked.setGeometry(0, 0, self.size_[0], self.size_[1])

        # ---- set Pages -----
        self.home_Page = {'w': QWidget(), "items": {}}
        self.Login_Page = {'w': QWidget(), "items": {}}
        self.Register_Page = {'w': QWidget(), "items": {}}

        # === Home Page ===
        self.home_Page["items"]["login_button"] = QPushButton("Log In", self.home_Page["w"])
        self.home_Page["items"]["register_button"] = QPushButton("Register", self.home_Page["w"])
        self.home_Page["items"]["continue_button"] = QPushButton("Continue without LogIn", self.home_Page["w"])

        # Position buttons manually
        self.home_Page["items"]["login_button"].setGeometry(5, 10,self.size_[0]-10,35)
        self.home_Page["items"]["register_button"].setGeometry(5, 50,self.size_[0]-10,35)
        self.home_Page["items"]["continue_button"].setGeometry(5, 90,self.size_[0]-10,35)

        # === Login Page ===
        self.Login_Page["items"]["true_v"] = {"user_name":False,"password":False}
        self.Login_Page["items"]["back_button"] = QPushButton("Home", self.Login_Page["w"])
        self.Login_Page["items"]["sub_button"] = QPushButton("Login", self.Login_Page["w"])
        self.Login_Page["items"]["user_name"] = QLineEdit(self.Login_Page["w"])
        self.Login_Page["items"]["password"] = QLineEdit(self.Login_Page["w"])
        self.Login_Page["items"]["forgot_password"] = QPushButton("Forgot Password?", self.Login_Page["w"])

        self.Login_Page["items"]["password"].setPlaceholderText("Password")
        self.Login_Page["items"]["user_name"].setPlaceholderText("User name")
        self.Login_Page["items"]["password"].setEchoMode(QLineEdit.Password)
        
        self.Login_Page["items"]["Y_first_item"] = 10
        self.Login_Page["items"]["user_name"].setGeometry(5,self.Login_Page["items"]["Y_first_item"],self.size_[0]-10,35)
        self.Login_Page["items"]["password"].setGeometry(5,self.Login_Page["items"]["Y_first_item"] + 40,self.size_[0]-10,35)
        self.Login_Page["items"]["sub_button"].setGeometry(5,self.Login_Page["items"]["Y_first_item"] + 80,self.size_[0]-10,35)
        self.Login_Page["items"]["back_button"].setGeometry(5, self.size_[3]-40,int(self.size_[0]/2)-10,35)
        self.Login_Page["items"]["forgot_password"].setGeometry(int(self.size_[0]/2)+5, self.size_[3]-40,int(self.size_[0]/2)-10,35)


        # === Register Page ===
        self.Register_Page["items"]["status"] = "normal"
        self.Register_Page["items"]["true_v"] = {"user_name":False,"API_key":False,"API_secreat":False,"password":False,"password-conf":False,"password_confirmed":True}
        self.Register_Page["items"]["back_button"] = QPushButton("Home", self.Register_Page["w"])
        self.Register_Page["items"]["have_accont"] = QPushButton("Have Accont?", self.Register_Page["w"])
        self.Register_Page["items"]["user_name"] = QLineEdit(self.Register_Page["w"])
        self.Register_Page["items"]["API_key"] = QLineEdit(self.Register_Page["w"])
        self.Register_Page["items"]["API_secreat"] = QLineEdit(self.Register_Page["w"])
        self.Register_Page["items"]["password"] = QLineEdit(self.Register_Page["w"])
        self.Register_Page["items"]["password-conf"] = QLineEdit(self.Register_Page["w"])
        self.Register_Page["items"]["sub_button"] = QPushButton("Register", self.Register_Page["w"])

        self.Register_Page["items"]["user_name"].setPlaceholderText("Set User name")
        self.Register_Page["items"]["API_key"].setPlaceholderText("Binance API-key")
        self.Register_Page["items"]["API_secreat"].setPlaceholderText("Binance API-secreat (HMAC SHA256)")
        self.Register_Page["items"]["password"].setPlaceholderText("Set Password")
        self.Register_Page["items"]["password-conf"].setPlaceholderText("Confirm Password")

        self.Register_Page["items"]["password"].setEchoMode(QLineEdit.Password)
        self.Register_Page["items"]["password-conf"].setEchoMode(QLineEdit.Password)

        self.Register_Page["items"]["Y_first_item"] = 10
        self.Register_Page["items"]["user_name"].setGeometry(5,self.Register_Page["items"]["Y_first_item"],self.size_[0]-10,35)
        self.Register_Page["items"]["API_key"].setGeometry(5,self.Register_Page["items"]["Y_first_item"] + 40,self.size_[0]-10,35)
        self.Register_Page["items"]["API_secreat"].setGeometry(5,self.Register_Page["items"]["Y_first_item"] + 80,self.size_[0]-10,35)
        self.Register_Page["items"]["password"].setGeometry(5,self.Register_Page["items"]["Y_first_item"] + 120,self.size_[0]-10,35)
        self.Register_Page["items"]["password-conf"].setGeometry(5,self.Register_Page["items"]["Y_first_item"] + 160,self.size_[0]-10,35)
        self.Register_Page["items"]["sub_button"].setGeometry(5,self.Register_Page["items"]["Y_first_item"] + 200,self.size_[0]-10,35)
        self.Register_Page["items"]["back_button"].setGeometry(5, self.size_[1]-40,int(self.size_[0]/2)-10,35)
        self.Register_Page["items"]["have_accont"].setGeometry(int(self.size_[0]/2)+5, self.size_[1]-40,int(self.size_[0]/2)-10,35)

        self.Register_Page["items"]["sub_button"].setEnabled(False)
        self.Login_Page["items"]["sub_button"].setEnabled(False)

        # Add all pages to stacked widget
        self.stacked.addWidget(self.home_Page['w'])      # index 0
        self.stacked.addWidget(self.Login_Page['w'])     # index 1
        self.stacked.addWidget(self.Register_Page['w'])  # index 2

        # Show Home Page by default
        self.stacked.setCurrentIndex(0)

        # === Button Connections ===
        self.home_Page["items"]["login_button"].clicked.connect(self.go_to_login)
        self.home_Page["items"]["register_button"].clicked.connect(self.go_to_register)
        self.home_Page["items"]["continue_button"].clicked.connect(self.continue_without_login)

        self.Login_Page["items"]["back_button"].clicked.connect(self.go_to_home)
        self.Register_Page["items"]["back_button"].clicked.connect(self.go_to_home)
        self.Login_Page["items"]["forgot_password"].clicked.connect(lambda: self.go_to_register(from_p="Login") )
        self.Register_Page["items"]["have_accont"].clicked.connect(self.go_to_login)

        # =========== Rigister and Login Button enabling (signals) =========================

        self.Register_Page["items"]["user_name"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'user_name'))
        self.Register_Page["items"]["API_key"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'API_key'))
        self.Register_Page["items"]["API_secreat"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'API_secreat'))
        self.Register_Page["items"]["password"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'password'))
        self.Register_Page["items"]["password-conf"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'password-conf'))
        
        self.Login_Page["items"]["user_name"].textChanged.connect(lambda x: self.login_texts_slot(x,'user_name'))
        self.Login_Page["items"]["password"].textChanged.connect(lambda x: self.login_texts_slot(x,'password'))

        # Login and rigister connection ============
        self.Login_Page["items"]["sub_button"].clicked.connect(self.login)
        self.Register_Page["items"]["sub_button"].clicked.connect(self.register)

    def continue_without_login(self):
        from .show_sharts import ChowSharts
        w = ChowSharts()
        w.run()
        self.close()

    # Button go to login clicked
    def go_to_login(self):
        self.setFixedSize(self.size_[0], self.size_[3])
        self.stacked.setCurrentIndex(1)
        self.setWindowTitle("Veltrix - Login")

    # Button go to Register clicked
    def go_to_register(self,from_p=None):
        if from_p == "Login":
            self.Register_Page["items"]["user_name"].setPlaceholderText("Your User name")
            self.Register_Page["items"]["user_name"].setText(self.Login_Page["items"]["user_name"].text())
            self.Register_Page["items"]["API_key"].setPlaceholderText("New Binance API-key (Frm the same Binance Acccont)")
            self.Register_Page["items"]["API_secreat"].setPlaceholderText("New Binance API-secreat (HMAC SHA256)")
            self.Register_Page["items"]["password"].setPlaceholderText("Set New Password")
            self.Register_Page["items"]["password-conf"].setPlaceholderText("Confirm new Password")
            self.Register_Page["items"]["have_accont"].setText("Back")
            self.Register_Page["items"]["sub_button"].setText("Reset info")
            self.setWindowTitle("Veltrix - Reset Password")
            self.Register_Page["items"]["status"] = 'reset_accont'
        else:
            self.setWindowTitle("Veltrix - Register")
            self.Register_Page["items"]["status"] = "normal"
            self.Register_Page["items"]["user_name"].setText('')
            self.Register_Page["items"]["user_name"].setPlaceholderText("Set User name")
            self.Register_Page["items"]["API_key"].setPlaceholderText("Binance API-key")
            self.Register_Page["items"]["API_secreat"].setPlaceholderText("Binance API-secreat (HMAC SHA256)")
            self.Register_Page["items"]["password"].setPlaceholderText("Set Password")
            self.Register_Page["items"]["password-conf"].setPlaceholderText("Confirm Password")
            self.Register_Page["items"]["have_accont"].setText("Have Accont?")
            self.Register_Page["items"]["sub_button"].setText("Register")

        self.setFixedSize(self.size_[0], self.size_[1])
        self.stacked.setCurrentIndex(2)

    # Button go to Home clicked
    def go_to_home(self):
        self.setFixedSize(self.size_[0], 130)
        self.stacked.setCurrentIndex(0)
        self.setWindowTitle("Veltrix")

    # ======= Rigister button enabling (slot) ================
    def rigister_texts_slot(self,text:str,slot:str):
        self.Register_Page["items"]["true_v"][slot] = True if text and str(text).strip() and text is not None else False
        if slot == "password" or slot == "password-conf":
            self.Register_Page["items"]["true_v"]["password_confirmed"] = True if self.Register_Page["items"]["password"].text() == self.Register_Page["items"]["password-conf"].text() else False
        self.Register_Page["items"]["sub_button"].setEnabled(True if all(self.Register_Page["items"]["true_v"].values()) else False)

    # ======= Login button enabling (slot) ================
    def login_texts_slot(self,text:str,slot:str):
        self.Login_Page["items"]["true_v"][slot] = True if text and str(text).strip() and text is not None else False
        self.Login_Page["items"]["sub_button"].setEnabled(True if all(self.Login_Page["items"]["true_v"].values()) else False)

    # Go To main window
    def go_to_main_window(self,data:dict):
        set_user_data(data)
        from .window import MainWindow
        w = MainWindow()
        w.run()
        self.close()


    # On login ========================
    def login(self):
        cipher = CipherUserData()
        un = self.Login_Page["items"]["user_name"].text()
        pwd = self.Login_Page["items"]["password"].text()
        data = cipher.get_local_user(pwd,un)
        if data[0] == True:

            accont_info_api = get_account_info(data[1].get("api-key"),data[1].get("api-secreat"))
            if accont_info_api[0] == False:
                if accont_info_api[1] == "INVALID_API_KEY":
                    pup_message("API Key Error","The saved API Key invalide or has not the correct permitions\nPlease try to reset your user data with correct info\nApi type: HMAC-SHA256\nPermitions neded: Any IP Adress + Read Only",None,"error")
                else:
                    pup_message("API Secreat Error","The saved secreat key is not acceptable with his API Key\nPlease try to reset your user data with correct info",None,"error")
                return
            else:
                pup_message("Seccess",f"You loged in\nClick ok to enter the program",lambda: self.go_to_main_window(data[1]),"info")

        elif data[0] == False and data[1] == "incorrect_info":
            pup_message("Incorrect password","User founded but incorrect password or incorrect user encrypt file",None,"warning")
        elif data[0] == False and data[1] == "user_not_found":
            pup_message("User not fond","user not fond in this device",self.go_to_register,"warning")

    def register(self):
        cipher = CipherUserData()
        user_name = self.Register_Page["items"]["user_name"].text()
        API_key = self.Register_Page["items"]["API_key"].text()
        API_secreat = self.Register_Page["items"]["API_secreat"].text()
        password = self.Register_Page["items"]["password"].text()
        
        if self.Register_Page["items"]["status"] == 'reset_accont':
            file_path = os.path.join(USERS_FILE,f"{user_name}.enc")
            if os.path.exists(file_path):
                os.remove(file_path)

        accont_info_api = get_account_info(API_key,API_secreat)

        if len(password) < 8: 
            pup_message("Password Error","The password should be more then 8 degets",None,"error")
            return
        elif self.is_valid_string(user_name) == False:
            pup_message("UserName Error","The user name shoud be just a digets or numbers or _",None,"error")
            return
        elif accont_info_api[0] == False:
            if accont_info_api[1] == "INVALID_API_KEY":
                pup_message("API Key Error","This API Key invalide or has not the correct permitions\nApi type: HMAC-SHA256\nPermitions neded: Any IP Adress + Read Only",None,"error")
            else:
                pup_message("API Secreat Error","The secreat key is not acceptable with this API Key",None,"error")
            return

        else:
            us_id = random.randint(10_000_000,99_999_999)
            data = {
                "id":us_id,
                "user_name" : user_name,
                "api-key" : API_key,
                "api-secreat" : API_secreat,
                "auther":{
                    "UID" : str(accont_info_api[1].get("uid")),
                    "accountType":str(accont_info_api[1].get("accountType"))
            }}
            created = cipher.save_new_local_user(password,data)
            if created:
                pup_message("Seccess",f"User Created By user name:{user_name}\nClick ok to enter the program",lambda: self.go_to_main_window(data),"info")
            else:
                pup_message("Repeated user name","This username used in this device",None,"error")

    # ======= Helpers ======================
    def is_valid_string(self,s: str) -> bool: 
        return bool(re.fullmatch(r"[A-Za-z0-9_]+", s))
    
    def closeEvent(self, event):
        logging.info("Close the l/r window")
        event.accept()