#!/usr/bin/env python

# Imported libraries
import sys
from sys import stdout

# Constants for the program
TLB_ENTRIES = 16
PAGE_TABLE_ENTRIES = 256
DEFAULT_FRAMES = 256
DEFAULT_TLB = 'fifo'
BIN = 'BACKING_STORE.bin'
MASK = 255
BYTE = 8
FIFO = 0
IRU = 1
OPT = 2

# Define all classes here

# Would like to implement a HashMap here in order to get keys
# and their frame values
class TLB:
   def __init__(self, type):
      self.table = [None] * TLB_ENTRIES
      self.hits = 0
      self.miss = 0
      self.type = type
      self.index = 0
   def check(self, pageNum):
      status = False

      for num in xrange(TLB_ENTRIES):
         if self.table[num] is not None:
            if self.table[num].getN() == pageNum:
              status = True
              self.hits += 1

      return status
   def add(self, pageTemp):
      self.miss += 1

      if self.type == OPT:
         print 'got in OPT'
      elif self.type == IRU:
         print 'got in IRU'
      else:
         self.table[self.index] = pageTemp

         if self.index == TLB_ENTRIES - 1:
            self.index = 0
         else:
            self.index += 1
   def getF(self, pageNum):
     frame = -1
     for num in xrange(TLB_ENTRIES):
        if self.table[num] is not None:
          if self.table[num].getN() == pageNum:
              frame = self.table[num].getF()
     return frame

# a basic page class
class Page:
   def __init__(self):
      self.frame = -1
      self.name = -1
      self.loaded = False
   def set(self, pageNum, frame):
      self.frame = frame
      self.name = pageNum
      self.loaded = True
   def getF(self):
      return self.frame
   def getN(self):
      return self.name
   def unLoad(self):
      self.loaded = False

# We want to make an array of PageEnties
class PageTable:
   def __init__(self):
      self.table = [None] * PAGE_TABLE_ENTRIES 
      self.faults = 0
   def add(self, pageTemp):
      self.table[pageTemp.getN()] = pageTemp
      self.faults += 1
   def __len__(self):
      return self.entries
   def check(self, pageNum):
      status = False
      if self.table[pageNum] is not None:
        status = True
      return status
   def getP(self, pageNum):
      self.table[pageNum]

# an array of page data in physical memory
class PhysicalMem:
   def __init__(self, frames):
      self.table = [None] * frames
      self.maxFrames = frames
      self.frameCount = 0
   def set(self, index, content):
      # if self.frameCount == self.maxFrames
      self.table[index] = content

      self.frameCount += 1;
   def get(self, index):
      return self.table[index]

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
def GetValue(content, virtual):
   cont = content.decode('hex')
   val = ord(cont[virtual.offset])
   if val > ((PAGE_TABLE_ENTRIES /2) + 1):
     val = val - 256
   return val
    
# Gets the 256 bytes from the frame and converts it to hex
def GetContent(binFile, virtual):
   traverse = virtual.page * PAGE_TABLE_ENTRIES  
   bin = binFile
   bin.seek(traverse)
   content = binFile.read(256)
   content = content.encode('hex').upper()
   return content

# Prints all the data we need to print to stdout
def PrintData(pageTable, tlb, leng): 
   faults = pageTable.faults

   print('Number of Translated Addresses = %d' %leng) 
   print('Page Faults = %d' %faults)
   print('Page Fault Rate = %.3f' %(float(faults) / float(leng)))
   print('TLB Hits = %d' %(tlb.hits))
   print('TLB Misses = %d' %(tlb.miss))
   print('TLB Miss Rate = %.3f' %(float(tlb.miss) / (float(tlb.hits) + float(tlb.miss))))

# Main method 
def main():
   arguments = sys.argv[1:]
   tlb = TLB(FIFO)
   pageTable = PageTable()

   pageCounter = 0
   frameCounter = 0

   if len(arguments) > 0:
      filename = arguments[0]
      frames = Ref(DEFAULT_FRAMES)
      pra = Ref(DEFAULT_TLB)
      
      ProcessArgs(arguments, frames, pra)
      physicalMem = PhysicalMem(frames.get())

      binFile = open(BIN)
      textFile = open(filename)

      line = textFile.readline()
      if (line):
         virtual = VirtualInfo(int(line))
         virtual.getInfo()
 
      while line:
         # check here if page is in TLB
          # if so
            # grab frame number and go straight to physicalMem to get data
            # DO NOT increment page or frame Counter
          # if not in TLB
         #else:
         if not(tlb.check(virtual.page)):
         # check if page is in pageTable
            
            if pageTable.check(virtual.page):
              # if yes 
              # add page to TLB
               pageTemp = pageTable.getP(virtual.page)
               tlb.add(pageTemp)
               # grab frame number and go to physicalMem to get data
               # DO NOT increment
               # if not in pageTable
            else:
               # add and set new frame in physicalMem
               # create a new page with number and frame
               # set new page in pageTable
               # add page to TLB
               # grab frame number and go to physicalMem to get data
               # only time you increment
               physicalMem.set(frameCounter, GetContent(binFile, virtual))
               pageTemp = Page()
               pageTemp.set(virtual.page, frameCounter)
               pageTable.add(pageTemp)
               tlb.add(pageTemp)

               frameCounter += 1

         pageCounter += 1
         frameNum = tlb.getF(virtual.page)
         
         stdout.write('%d, ' %virtual.address)
         stdout.write('%d, ' %GetValue(physicalMem.get(frameNum), virtual))
         stdout.write('%d, ' %(physicalMem.frameCount - 1))
         stdout.write(physicalMem.get(frameNum))
         stdout.flush()
         stdout.write('\n')
         
         line = textFile.readline()

         try:
            virtual = VirtualInfo(int(line))
            virtual.getInfo()
         except ValueError:
            virtual = 0
      
      PrintData(pageTable, tlb ,pageCounter)

# Runs the main method      
if __name__ == "__main__":
   main()

# end of code
