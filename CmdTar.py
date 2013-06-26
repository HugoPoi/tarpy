#!/usr/bin/python2.7

import argparse,sys,DivineTar

class CmdTar:

  currentPath = ""
  
  def __init__(self):
    
    self.currentTar = DivineTar.Tar(sys.argv[1])
    
    line = sys.stdin.readline()
    
    while(True):
      command = line.split()[0]
      args = line.split()
      del args[0]
      try:
        getattr(self,command)(args)
      except AttributeError:
        print "Command not found"
      line = sys.stdin.readline()
    
  def ls(self, args):
    lsParser = argparse.ArgumentParser()
    lsParser.add_argument("path", nargs='?',metavar="PATH", type=str)
    lsArgs = lsParser.parse_args(args)
    if lsArgs.path != None:
      list = self.currentTar.search(lsArgs.path)
      for ele in list:
        print "    ",ele["path"]
    
  def exit(self, args):
    exit(0)
  def quit(self, args):
    exit(0)




#try:
main = CmdTar()
#except:
#  exit(0)