#!/usr/bin/env python

# Imported libraries
import sys

# Constants for the program
TLB_ENTRIES = 16
PAGE_TABLE_ENTRIES = 256
DEFAULT_FRAMES = 256
DEFAULT_TLB = 'fifo'
BIN = 'BACKING_STORE.bin'
MASK = 255
BYTE = 8

# Define all classes here

# Would like to implement a HashMap here in order to get keys
# and their frame values
class TLB:
   def __init__(self):
      self.dict = {}
      self.hits = 0
      self.miss = 0
      self.page = 0
      self.index = 0
   def add(self, page):
      newDict = {self.index: page}
      self.dict.update(newDict)
      self.index += 1

class Page:
   def __init__(self):
      self.frame = -1
      self.loaded = False
   def set(self, frame):
      self.frame = frame
   def get(self):
      return frame
   def load(self):
      self.loaded = True
   def unLoad(self):
      return self.loaded

# We want to make an array of PageEnties
class PageTable:
   def __init__(self):
      self.table = [None] * PAGE_TABLE_ENTRIES 
      self.entries = 0
   def add(self, pageNum, page):
      self.table[pageNum] = page
      self.entries += 1
   def __len__(self):
      return self.entries

#class PhysicalMem:
#   def __init__(self, frames):
#      self.table = [None] * frames
#   def set(self, index, content):
#      self.table[index] = content

# How to order the frames and indexes of logical and physical memory
class VirtualInfo:
   def __init__(self, address):
      self.address = address
      self.page = 0
      self.offset = 0
   def getInfo(self):
      temp = self.address
      page = self.page
      page = MASK << BYTE
      page = temp & page
      self.page = page >> BYTE
      self.offset = MASK & temp

# This class is so we will be able to treat variables as pointers
# This is a psudo pointer class
class Ref:
   def __init__(self, obj):
      self.obj = obj
   def get(self):
      return self.obj
   def set(self, obj): 
      self.obj = obj

# All Functions will be here
def ProcessArgs(arguments, frames, pra):
   if len(arguments) == 3:
      frames.set(arguments[1])
      pra.set(arguments[2])
   elif len(arguments) == 2:
      if arguments[1].isdigit():
         frames.set(arguments[1])
      else:
         pra.set(arguments[1])

#return the value from the specified address with the specified offset
def GetValue(binFile, virtual):
   truOff = (virtual.page * PAGE_TABLE_ENTRIES) + virtual.offset
   binFile.seek(truOff)
   val = binFile.read(1)
   intVal = ord(val)
   if intVal > ((PAGE_TABLE_ENTRIES /2) + 1):
      intVal = intVal - 256
   return intVal  
    
# Gets the 256 bytes from the frame and converts it to hex
def GetContent(binFile, virtual):
   traverse = virtual.page * PAGE_TABLE_ENTRIES  
   bin = binFile
   bin.seek(traverse)
   content = binFile.read(256)
   content = content.encode('hex').upper()
   return content

# Prints all the data we need to print to stdout
def PrintData(pageTable): 
   print('Number of Translated Addresses = %d' %(len(pageTable))) 
   print('Page Faults = %d' %(0))
   print('Page Fault Rate = %.3f' %(3.1456))
   print('TLB Hits = %d' %(111))
   print('TLB Misses = %d' %(111))
   print('TLB Miss Rate = %.3f' %(3.1456))

# Main method 
def main():
   arguments = sys.argv[1:]
   buffer = TLB()
   pageTable = PageTable()

   if len(arguments) > 0:
      filename = arguments[0]
      frames = Ref(DEFAULT_FRAMES)
      pra = Ref(DEFAULT_TLB)
      
      ProcessArgs(arguments, frames, pra)
 #     physicalMem = PhysicalMem(frames)

      binFile = open(BIN)
      textFile = open(filename)

      line = textFile.readline()
      if (line):
         virtual = VirtualInfo(int(line))
         virtual.getInfo()
 
      while line:
         print 'Address: %d' %virtual.address
         print GetContent(binFile, virtual)

         line = textFile.readline()

         try:
            virtual = VirtualInfo(int(line))
            virtual.getInfo()
         except ValueError:
            virtual = 0
      
      PrintData(pageTable)

# Runs the main method      
if __name__ == "__main__":
   main()

# end of code
