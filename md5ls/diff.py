#!/usr/bin/env python3

import argparse
import io
import sys

def diff(args):
    """md5ls.diff - Compare two md5ls files
    
    Designed for use with output of md5ls.create
    """

    # Read and clean lines from files
    lines1 = strip_lines(get_lines(args.left_file))
    lines2 = strip_lines(get_lines(args.right_file))

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
    for md5sum in list(dict2.keys()):
        for filepath in dict2[md5sum]:
            unique_right.append("> " + md5sum + "  " + filepath)
        # Done with hash in right only
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
        exit(-1)

    # Build summary strings
    left_heading = (str(len(unique_left))
                    + " files found only in the left manifest, "
                    + sys.argv[2])
    right_heading = (str(len(unique_right))
                    + " files found only in the right manifest, "
                    + sys.argv[3])
    moved_heading = (str(int(len(moved) / 2)) + " files which have the same "
                    + "hash, but have been moved to a different path")
    
    # If outFile is not given, print to console
    if(args.out_file is None):
        if(args.summary):
            print(left_heading)
            print(right_heading)
            print(moved_heading)
        else:
            print_if_not_empty(unique_left, left_heading)
            print_if_not_empty(unique_right, right_heading)
            print_if_not_empty(moved, moved_heading)

    # Write the same output to the file instead of the console
    else:
        # UTF-8 encoding must be specified or Windows will use cp1252
        # Unix-style newlines are used regardless of platform for consistency
        with io.open(args.out_file, 'w', encoding='utf8', newline='\n') as f:
            if(args.summary):
                f.write(left_heading + '\n')
                f.write(right_heading + '\n')
                f.write(moved_heading + '\n')
            else:
                write_if_not_empty(unique_left, left_heading, f)
                write_if_not_empty(unique_right, right_heading, f)
                write_if_not_empty(moved, moved_heading, f)
        


def get_lines(filename):
    """Return list of lines from the text file at filename"""
    with io.open(filename, encoding='utf-8') as f:
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


def write_if_not_empty(list, heading, out_file):
    """Write heading once, then each string in list, if list isn't empty"""
    if(len(list) > 0):
        out_file.write(heading + '\n')
        for line in list:
            out_file.write(line + '\n')
        out_file.write('\n')
    