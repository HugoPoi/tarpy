#!/usr/bin/python2.7

import os
import os.path


#"""""""""""""""""""""""""""""#
#   the main tar class        #
#"""""""""""""""""""""""""""""#


class Tar:
    """handle basic mangement of an basic tar file"""

    fileStream = 0
    fileSize = 0
    dirNumbers = 0

    def __init__(self, tarFileName):

        self.fileName = str(tarFileName)
        self.rootDir = "."
        self.open_tar()
        self.directories = []

#change current directory
    def chdir_tar(self, newCWD):
        try:
            os.chdir(str(newCWD))
            self.rootDir = str(newCWD)
        except BaseException:
            print " the path required does not exist"

# open the tarfile
    def open_tar(self):
        #check if the file exist
        if os.path.isfile(self.fileName) is False:
            print """ the file doesn't exist """
            return
        else:
            Tar.fileStream = open(self.fileName, 'r+b')
            Tar.fileSize = len(Tar.fileStream.read())
            Tar.fileStream.seek(0)
            #self.chdir_tar("/")

# load repertories and files
    def load_OneInstance(self):
        tarInstance = {
            "path":         "",
            "permission":   "",
            "proprietaire": "",
            "gid":          "",
            "size":         "",
            "date":         "",
            "checksum":     "",
            "fileType":  "",
            "lnFile":       "",
            "blockStart":   ""
        }

        #read octet by octet
        tarStruct = [
                [100, "path"],
                [8, "permission"],
                [8, "proprietaire"],
                [8, "gid"],
                [12, "size"],
                [12, "date"],
                [8, "checksum"],
                [1, "fileType"],
                [355, "lnFile"]
        ]

        dataSize = 0
        for j in tarStruct:
            tmp = str(j[1])
            tarInstance[tmp] = tarInstance[tmp]
            tarInstance["blockStart"] = Tar.fileStream.tell()
            if tarInstance["blockStart"] == Tar.fileSize:
                return

            tarInstance[tmp] = Tar.fileStream.read(j[0])
            # FUCK FUCK i do waste one day to find this shit
            tarInstance[tmp] = tarInstance[tmp].replace("\x00", '')
            tarInstance[tmp] = tarInstance[tmp].replace("0", '')

            #check the size of the file
            if j[1] == "size" and tarInstance[tmp] != '':
                dataSize = 512
            #jump utar infos at the end

        Tar.fileStream.read(dataSize)
        #reset dataSize
        return tarInstance

    def load_all_instance(self):
        instance = {"d": "e"}
        f = None
        while instance:
            instance.sort(f=None, key=None, reverse=None)
            for (i, v) in f.items():
                if i == "path" and v == '':
                    return
                else:
                    print "print", i, "=", v

            print "\n"
            instance = self.load_OneInstance()

        return

# close the file
    def close_tar(self):
        try:
            Tar.fileStream.close()
        except IOError:
            print "there is some problem with the closing"

# print the current directory path
    def getpwd_tar(self):
        print os.getcwd()

# return an TarDir object
    def opendir_tar(self):
        pass


#"""""""""""""""""""""""""""""#
#   TarDir class Management   #
#"""""""""""""""""""""""""""""#


class TarDir:
    """handle a directory in a tar file """

# constructor of the directory struct
    def __init__(self, dirNameIn, indexIn=None):
        self.name = str(dirNameIn)
        self.path = ""
        self.permission = 0
        self.gid = 0
        self.size = 0
        self.date = 0
        self.checksum = 0
        self.fileType = 0
        self.lnFile = ""
        self.curPos = 0
        self.blockStart = indexIn
        self.filesIn = []

# add files with TarFile instances
    def addFile(self, tarFileIn):
        self.filesIn.append(tarFileIn)

# show the content of the current directory
    def readdir(self):
        #print os.listdir(".")
        for tmpfile in self.filesIn:
            print tmpfile.name, "    "

#open an file and return an TarFile object
    def fopen(self, filename):
        pass

#close an repertory
    def close(self):
        pass


#"""""""""""""""""""""""""""""#
#   TarFile class Management #
#"""""""""""""""""""""""""""""#


class TarFile:
    """ handle some file in the archieve """

    def __init__(self, filename, fileStream, indexIn=0):
        self.name = str(filename)
        self.path = ""
        self.permission = 0
        self.gid = 0
        self.size = 0
        self.date = 0
        self.checksum = 0
        self.fileType = 0
        self.lnFile = ""
        self.curPos = 0
        self.blockStart = indexIn
        self.stream = fileStream

#read size byte of the file
    def read(self, size):
        if size <= self.size:
            self.stream.seek(self.blockStart + 512)
            datas = self.stream.read(size)
            return datas

#go to the offset
    def seek(self, offset, whence=0):
        self.stream.seek(self.blockStart + offset)

    def close(self):
        pass
