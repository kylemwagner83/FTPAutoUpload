from ftplib import FTP
import os
import configparser
import json



if os.path.isfile("./settings.ini") and os.path.isfile("./filelist.json"):

    config = configparser.ConfigParser()
    config.read("settings.ini")
    ipaddress = config["FTP Settings"]["ipaddress"]
    port = config["FTP Settings"]["port"]
    username = config["FTP Settings"]["username"]
    password = config["FTP Settings"]["password"]

    with open("filelist.json", "r") as filehandle:
        file_list = json.load(filehandle)

    ftp = FTP()
    ftp.connect(ipaddress, int(port))
    ftp.login(username, password)
        
    for x in file_list:
        name = os.path.basename(x)
        file = open(f"{x}", "rb")
        ftp.storbinary(f"STOR {name}", file)

else:
    print("Settings not found or incomplete, use config tool to set FTP info and select files for transfer")