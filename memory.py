#! /usr//localbin/python

import re
from math import ceil

alpha = set([ x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" ])

class Memory:
    n_block = 128
    internal = "."*n_block
    block_size = 4096
    blocksPerLine = 32


    def printRep(self):
        print self

    def __str__(self):
        returnvalue =  "="*self.blocksPerLine+"\n"
        for i in range(int(ceil(self.n_block/self.blocksPerLine))):
            returnvalue += self.internal[self.blocksPerLine*i:self.blocksPerLine*(i+1)]+"\n"
        returnvalue += "="*self.blocksPerLine+"\n"
        return returnvalue


    def alloc(self, filename, size):
        filesInUse = set(self.internal)
        assert(len(filesInUse) < 26) #We should never try to add a new file when we have 24 allocated.
        assert(not filename in filesInUse)

        #newChar = (alpha - filesInUse).pop() #THe better way.
        newChar = sorted(list(alpha - filesInUse))[0] #Since I like alphabetic order.
        numBlocks = int(ceil(float(size)/self.blockSize))
        numClusters = 0

        if (self.internal.count(".") >= numBlocks):
            self.internal = self.internal.replace(".", newChar, numBlocks)
            numClusters = len([ x for x in re.split("[^"+newChar+"]*", self.internal) if len(x) ]) 
            return newChar, size, numBlocks, numClusters 

        else:
            return 0, 0, 0, 0


    def delete(self, fileChar):
        assert(fileChar in self.internal)
        blocksFreed = self.internal.count(fileChar)
        self.internal = self.internal.replace(fileChar, ".")
        return fileChar, blocksFreed


    def read(self, fileChar, size):
        pass


    def __init__(self, n_block=128, blockSize=4096, blocksPerLine=32):
        self.n_block = n_block
        self.blockSize = blockSize
        self.blocksPerLine = blocksPerLine
        self.internal = "."*self.n_block
