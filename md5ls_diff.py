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

    # Output lists
    # TODO: changed = []
    moved = []
    unique_left = []
    unique_right = []

    # Compare left to right. Don't loop over dictionary being modified.
    for md5sum in list(dict1.keys()):
        # Unique hash in left only
        if md5sum not in dict2:
            for filepath in dict1[md5sum]:
                unique_left.append("< " + md5sum + "  " + filepath)
            # Done with hash in left only
            del dict1[md5sum]

        # Matching hash, different path
        elif dict1[md5sum] != dict2[md5sum]:
            # Filepaths in dict1 that are not in dict2
            for filepath in dict1[md5sum]:
                if filepath not in dict2[md5sum]:
                    moved.append("< " + md5sum + "  " + filepath)
            # Filepaths in dict2 that are not in dict1
            for filepath in dict2[md5sum]:
                if filepath not in dict1[md5sum]:
                    moved.append("> " + md5sum + "  " + filepath)
            # Done with this hash in both lists
            del dict1[md5sum]
            del dict2[md5sum]

        # Hash exists in both lists AND paths are identical
        else:
            # Done with this hash in both lists
            del dict1[md5sum]
            del dict2[md5sum]

    # The only items left in right list will be hashes unique to that list
    for md5sum in dict2:
        for filepath in dict2[md5sum]:
            unique_right.append("> " + md5sum + "  " + filepath)
        # Done with hash in left only
        del dict2[md5sum]

    # Sanity checks
    error_flag = False
    if(len(dict1) != 0):
        print("INTERNAL ERROR: After parsing, the left dict is not empty:")
        print(dict1)
        print()
        error_flag = True
    if(len(dict2) != 0):
        print("INTERNAL ERROR: After parsing, the right dict is not empty:")
        print(dict2)
        print()
        error_flag = True
    if(error_flag):
        exit()

    # Print results
    print_if_not_empty(unique_left, str(len(unique_left))
                                    + " files found only in the 1st manifest, "
                                    + sys.argv[1])
    print_if_not_empty(unique_right, str(len(unique_right))
                                    + " files found only in the 2nd manifest, "
                                    + sys.argv[2])
    print_if_not_empty(moved, str(len(moved)) + " files which have the same "
                            + "hash, but have been moved to a different path")


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
    """Return dict of {md5sum:[filepaths]} from md5ls_lines"""
    HASH_END_INDEX = 32
    PATH_START_INDEX = 34

    md5_dict = {}

    for line in md5ls_lines:
        hash = line[:HASH_END_INDEX]
        path = line[PATH_START_INDEX:]
        if hash in md5_dict:
            md5_dict[hash].append(path)
        else:
            md5_dict[hash] = [path]

    return md5_dict


def print_if_not_empty(list, heading):
    """Print heading once, then each string in list, if list isn't empty"""
    if(len(list) > 0):
        print(heading)
        for line in list:
            print(line)
        print()


if __name__ == "__main__":
    main()
