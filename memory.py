#! /usr/bin/env python

import re
from math import ceil

alpha = set([ x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" ])

class Memory:
    n_block = 128
    internal = "."*n_block
    block_size = 4096
    blocksPerLine = 32
    lookupTable = dict()


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
        assert(not filename in self.lookupTable.keys())
        #newChar = (alpha - filesInUse).pop() #THe better way.
        newChar = sorted(list(alpha - filesInUse))[0] #Since I like alphabetic order.
        numBlocks = int(ceil(float(size)/self.blockSize))
        numClusters = 0
        if (self.internal.count(".") >= numBlocks):
            self.lookupTable[filename] = newChar
            self.internal = self.internal.replace(".", newChar, numBlocks)
            numClusters = len([ x for x in re.split("[^"+newChar+"]*", self.internal) if len(x) ]) 
            return newChar, size, numBlocks, numClusters 
        else:
            return 0, 0, 0, 0


    def deleteBlocks(self, fileChar):
        assert(fileChar in self.internal)
        blocksFreed = self.internal.count(fileChar)
        self.internal = self.internal.replace(fileChar, ".")
        return fileChar, blocksFreed

    def deleteFile(self, filename):
        assert(filename in self.lookupTable.keys())
        fileChar = self.lookupTable[filename]
        del self.lookupTable[filename]
        return self.deleteBlocks(fileChar)


    def read(self, filename, offset, size):
        #I don't remmeber how big each file is, this could be a problem if we don't fill an entire block.....
        assert(filename in self.lookupTable.keys())
        newChar = self.lookupTable[filename]
        clusters = [ x for x in re.split("[^"+newChar+"]*", self.internal) if len(x) ]
        numClusters = 0; numBlocks = 0
        curOffset = 0; curSize = 0
        for cluster in clusters:
            numClusters += 1
            for block in cluster:
                if curOffset < offset:
                    curOffset += self.block_size
                    continue

                else:
                    if (curOffset > offset): #Record the remainin data from the block after the offset is accounted for.
                        numBlocks += 1
                        curSize += curOffset - offset
                        curOffset = offset

                    if curSize < size:
                        numBlocks += 1
                        curSize += self.block_size

                    else:
                        return newChar, curOffset, min(curSize, size), numBlocks

        #Edge case, offset takes us to the last block.
        if (curOffset > offset): #Record the remainin data from the block after the offset is accounted for.
            numBlocks += 1
            curSize += curOffset - offset
            curOffset = offset

        #TODO: Add check for our of bounds errors.
        #assert(curSize <= size)
        return newChar, curOffset, min(curSize, size), numBlocks


    def __init__(self, n_block=128, blockSize=4096, blocksPerLine=32):
        self.n_block = n_block
        self.blockSize = blockSize
        self.blocksPerLine = blocksPerLine
        self.internal = "."*self.n_block
