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
    headers = []
    roots = []

    def __init__(self, tarFileName):

        self.fileName = str(tarFileName)
        self.rootDir = "."
        self.open_tar()
        self.directories = []
        self.loadAllHeader()
        self.findRoot()

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

# load repertories and files
    def loadHeader(self):
        tarHeader = {
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
            tarHeader[tmp] = tarHeader[tmp]
            tarHeader["blockStart"] = Tar.fileStream.tell()
            if tarHeader["blockStart"] == Tar.fileSize:
                return False

            tarHeader[tmp] = Tar.fileStream.read(j[0])
            # FUCK FUCK i do waste one day to find this shit
            tarHeader[tmp] = tarHeader[tmp].replace("\x00", '')
            tarHeader[tmp] = tarHeader[tmp].replace("0", '')

            #check the size of the file
            if j[1] == "size" and tarHeader[tmp] != '':
                dataSize = 512
            #jump utar infos at the end

        Tar.fileStream.read(dataSize)
        #reset dataSize
        return tarHeader

    def loadAllHeader(self):
        currentHeader = self.loadHeader()
        while currentHeader["path"] != "":
            self.displayHeader(currentHeader)
            self.headers.append(currentHeader)
            currentHeader = self.loadHeader()
        return

    def displayHeader(self,header):
      for data in header.items():
        print data[0],"=",data[1]

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

    def findRoot(self):
      #TODO parcourir les TarDir a la place des headers ... oupas
      for header in self.headers:
        #if header["fileType"] == "5":
          path = header["path"].rsplit("/",1)
          print path
          if not any(path[0].startswith(root) for root in self.roots):
            #path[0]+="/"
            self.roots.append(path[0])
      print self.roots
      
    def search(self,path):
      out = []
      for header in self.headers:
        if header["path"].startswith(path) and not "/" in header["path"][:-1].rsplit(path,1)[1]:
          out.append(header)
      return out

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
        self.dirsIn = []

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
