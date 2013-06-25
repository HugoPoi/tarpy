#!/usr/bin/python2.7

import argparse,sys

class CmdTar:

  currentPath = ""
  
  def __init__(self):
    
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
    print lsArgs.path
    
  def exit(self, args):
    exit(0)
  def quit(self, args):
    exit(0)




    
main = CmdTar()