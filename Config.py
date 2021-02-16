from ftplib import FTP
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from configwindow import Ui_MainWindow
import sys
import os
import configparser
import json



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.saveConfigButton.clicked.connect(self.saveConfig)
        self.clearButton.clicked.connect(self.clearList)
        self.addFilesButton.clicked.connect(self.fileDialog)
        self.saveFileButton.clicked.connect(self.saveFileList)
        self.ftpUploadButton.clicked.connect(self.ftpUploadFiles)
        self.file_list = []

        if os.path.isfile("./settings.ini"):
            self.readConfig()

        if os.path.isfile("./filelist.json"):
            with open("filelist.json", "r") as filehandle:
                self.file_list = json.load(filehandle)
            self.fileListWindow.addItems(self.file_list)

        

    def fileDialog(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        selected_files = dlg.getOpenFileNames(self)
        for x in selected_files[0]:
            if x not in self.file_list:
                self.file_list.append(x)
        self.fileListWindow.clear()
        self.fileListWindow.addItems(self.file_list)


    def saveFileList(self):
        with open("filelist.json", "w") as filehandle:
            json.dump(self.file_list, filehandle)


    def clearList(self):
        self.file_list = []
        self.fileListWindow.clear()
        

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        ipaddress = config["FTP Settings"]["ipaddress"]
        port = config["FTP Settings"]["port"]
        username = config["FTP Settings"]["username"]
        password = config["FTP Settings"]["password"]
        self.IPtextbox.setText(f"{ipaddress}")
        self.portTextbox.setText(f"{port}")
        self.usernameTextbox.setText(f"{username}")
        self.passwordTextbox.setText(f"{password}")


    def saveConfig(self):
        ipaddress = self.IPtextbox.text()
        port = self.portTextbox.text()
        username = self.usernameTextbox.text()
        password = self.passwordTextbox.text()
        config = configparser.ConfigParser()
        config["FTP Settings"] = {
            "IPaddress": ipaddress,
            "Port": port,
            "Username": username,
            "Password": password,
        }
        with open("settings.ini", "w") as configfile:
            config.write(configfile)


    def ftpUploadFiles(self):
        ipaddress = self.IPtextbox.text()
        port = self.portTextbox.text()
        username = self.usernameTextbox.text()
        password = self.passwordTextbox.text()
        ftp = FTP()
        ftp.connect(ipaddress, int(port))
        ftp.login(username, password)
        for x in self.file_list:
            name = os.path.basename(x)
            file = open(f"{x}", "rb")
            ftp.storbinary(f"STOR {name}", file)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())