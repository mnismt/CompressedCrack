import zipfile
import rarfile
import os
import sys
from threading import Thread
import argparse
from itertools import product
import time

parser = argparse.ArgumentParser(description='CompressedCrack', epilog='Use the -h for help')
parser.add_argument('-i','--input', help='Insert the file path of compressed file', required=True)
parser.add_argument('rules', nargs='*', help='<min> <max> <character>')

# Const Character
CHARACTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/"

class Check:
    def __init__(self, Arg):
        self.type = None
        self.rules = False
        self.startLength = None
        self.maxLength = None
        self.character = None
        # Check Rules
        if len(Arg) >= 4:
            self.getData(Arg)
            self.rules = True
        elif len(Arg) == 0 or len(Arg) > 2:
            parser.print_help()
            parser.exit()
        # Check File Exist
        if (self.CheckFileExist(Arg)):
            self.getType(Arg)
        else:
            print ('No such file or directory: ',Arg[1])
            parser.exit()

    def CheckFileExist(self, Arg):
        if (os.path.isfile(Arg[1])):
            return True
        else:
            return False

    def getData(self, Arg):
        try:
            self.startLength = int(Arg[2])
            self.maxLength = int(Arg[3])
        except ValueError:
            print ('Value Error')
            parser.exit()
        if self.startLength > self.maxLength:
            print ('Length Error')
            parser.exit()
        if len(Arg) == 5:
            self.character = Arg[4]
    
    def getType(self, Arg):
        if os.path.splitext(Arg[1])[1] == ".rar" or os.path.splitext(Arg[1])[1]==".zip":
            self.type = os.path.splitext(Arg[1])[1]
        else:
            print ('Extension Error')
            parser.exit()

class Handler:
    def __init__(self, rules, typeCompress, startLength, maxLength, character):
        self.rules = rules
        self.location = sys.argv[2]
        self.type = typeCompress
        self.startLength = startLength
        self.maxLength = maxLength
        if not character:
            self.character = CHARACTER
        else:
            self.character = character
        self.result = False

        self.GetFile()
        self.CheckRules()

    def GetFile(self):
        # Khai báo file
        if self.type == '.zip':
            self.FileCrack = zipfile.ZipFile(self.location)
        else:
            self.FileCrack = rarfile.RarFile(self.location)

    def Brute(self,password):
        try:
            if self.type == '.zip':
                tryPass = password.encode()
            else:
                tryPass = password
            print (tryPass)
            self.FileCrack.extractall(pwd=tryPass)
            print ('Complete')
            print('Time:',time.process_time() - self.start_time,'s')
            print ('Password:',password)
            self.result = True
        except:
            pass

    def CheckRules(self):
        self.start_time = time.process_time()
        print ('Cracking...')
        if not self.rules:
            length = 1
            while True:
                self.SendRequest(length)
                if self.result:
                    return
                length += 1
        else:
            for length in range(self.startLength, self.maxLength + 1):
                self.SendRequest(length)
                if self.result:
                    return
            if not self.result:
                print ('Cannot find password with this rules')
                return

    def SendRequest(self,length):
        listPass = product(self.character, repeat=length)
        for Pass in listPass:
            tryPass = ''.join(Pass)
            # Multi Thread:
            # nThread = Thread(target=self.Brute, args=(tryPass, ))
            # nThread.start()

            # Single Thread: 
            self.Brute(tryPass)
            if self.result:
                return
def main():
    check = Check(sys.argv[1:])
    args = parser.parse_args()
    rarfile.UNRAR_TOOL = "UnRAR.exe"
    Handling = Handler(check.rules, check.type, check.startLength, check.maxLength, check.character)
if __name__ == '__main__':
    main()
