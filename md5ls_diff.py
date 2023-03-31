#!/usr/bin/env python3

import io
import sys

def main():
    """md5ls_diff.py - Compare two md5ls files
    
    Designed for use with output of md5ls.py
    """

    # Check for number of arguments
    if len(sys.argv) != 3:
        print('2 input files must be given as arguments')
        exit()

    # Read and clean lines from files
    lines1 = strip_lines(get_lines(sys.argv[1]))
    lines2 = strip_lines(get_lines(sys.argv[2]))

    # Convert lines into dictionaries
    dict1 = md5ls_to_dict(lines1)
    dict2 = md5ls_to_dict(lines2)

    # For every md5 in list2, if the md5 isn't in list1, print it
    for md5sum in dict2:
        if md5sum not in dict1:
            print(md5sum + '  ' + dict2[md5sum])


def get_lines(filename):
    """Return list of lines from the text file at filename"""
    with io.open(filename) as f:
        lineList = f.readlines()

    return lineList


def strip_lines(line_list):
    """Return list of non-blank lines without newlines from line_list"""
    stripped_lines = []

    for line in line_list:
        if line != '\n':
            stripped_lines.append(line.strip())

    return stripped_lines


def md5ls_to_dict(md5ls_lines):
    """Return (key:value pairs of md5sums and filepaths from md5ls_lines"""
    md5_dict = {}

    for line in md5ls_lines:
        md5_dict[line[:32]] = line[34:]

    return md5_dict


if __name__ == "__main__":
    main()
