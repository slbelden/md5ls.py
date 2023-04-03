#!/usr/bin/env python3

import io
import sys

def main():
    """diff_diff.py - Print non-blank lines that differ between two text files"""

    # Check for number of arguments
    if len(sys.argv) != 3:
        print('2 input files must be given as arguments')
        exit()

    # Read and clean lines from files
    lines1 = strip_lines(get_lines(sys.argv[1]))
    lines2 = strip_lines(get_lines(sys.argv[2]))

    # Print lines that are only in either file, not in both
    unique_lines = set(lines1) ^ set(lines2)
    for line in unique_lines:
        print(line)


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


if __name__ == "__main__":
    main()
