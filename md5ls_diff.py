#!/usr/bin/env python3

# For argument access
import sys

# Function returns list of lines from a text file
def getLines(filename):
    openFile = open(filename)
    lineList = openFile.readlines()
    openFile.close()

    return lineList

# Function returns list of non-blank lines without newlines
def stripLines(lineList):
    strippedLines = []

    for line in lineList:
        if line != '\n':
            strippedLines.append(line.strip())

    return strippedLines

# Function returns (key:value pairs of md5sums and filepaths
# when given a md5ls output as argument
def md5lsToDict(md5lsLines):
    md5dict = {}

    for line in md5lsLines:
        md5dict[line[:32]] = line[34:]

    return md5dict



# Check for number of arguments
if len(sys.argv) != 3:
    print('2 input files must be given as arguments')
    exit()

# Read and clean lines from files
lines1 = stripLines(getLines(sys.argv[1]))
lines2 = stripLines(getLines(sys.argv[2]))

# Convert lines into dictionaries
dict1 = md5lsToDict(lines1)
dict2 = md5lsToDict(lines2)

# For every md5 in list2, if the md5 isn't in list1, print it
for md5sum in dict2:
    if md5sum not in dict1:
        print(md5sum + '  ' + dict2[md5sum])
