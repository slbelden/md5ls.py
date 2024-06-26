#!/usr/bin/env python3

import argparse
import hashlib
import io
import os
import sys
from multiprocessing import Pool

def create(args):
    """md5ls.create - List files and their MD5 sums"""

    # Work around bug in PowerShell 5. See function definition for more info.
    root_dir = validate_dir_path(args.root_dir)

    # Walk file tree from root dir, collect all files found, ignore empty dirs
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            file_list.append(os.path.join(root, name))
    
    # Completely disable multithreading for compatibility and stability if -j 1
    if (args.num_jobs <= 1):
        hash_list = map(get_hash_for_file, file_list)
    else:
        # Generate hashes using parallel workers for -j > 1
        pool = Pool(args.num_jobs)
        hash_list = pool.map(get_hash_for_file, file_list)

    # Transform full filepaths into relative paths
    result_list = []
    for hash, path in hash_list:
        pretty_path = os.path.relpath(path, root_dir).replace(os.sep, '/')
        result_list.append((hash, pretty_path)) 

    # Sort list to produce a consistent manifest output
    if args.k1:
        # Sort by 1st element of tuple, the MD5 sum (eq: sort -k1)
        result_list.sort()
    else:
        # Sort by 2nd element of tuple, the filepath (eq: sort -k2)
        result_list.sort(key=lambda a: a[1])

    # Output
    delim = '  ./'  # Match output of md5sum command: 'hash  ./filepath'
    if(args.out_file is not None):
        # UTF-8 encoding must be specified or Windows will use cp1252
        # Unix-style newlines are used regardless of platform for consistency
        with io.open(args.out_file, 'w', encoding='utf8', newline='\n') as f:
            for row_tuple in result_list:
                try:
                    f.write(row_tuple[0] + delim + row_tuple[1])
                    f.write('\n')
                except UnicodeEncodeError:
                    print("ABORT: Filepath contains characters that can't be "
                          + "encoded to UTF-8: " + row_tuple[1])
                    exit()
    else:
        for row_tuple in result_list:
            print(row_tuple[0] + delim + row_tuple[1])


def get_hash_for_file(filepath):
    """Return 2-tuple: (md5sum, relative_filepath) for file at 'filepath'."""
    hash = hashlib.md5()
    try:
        # Open file as read-only, using binary mode to avoid OS newline conversions 
        with open(filepath, 'rb') as in_file:
            # Update hash in 32kb chunks until end of file.
            # 32kb is a decent compromise between two competing speed goals:
            #     * A few large files benefit from fewer reads with larger chunks
            #     * Many small files benefit from lower overhead of smaller chunks
            # Speed testing showed 16-64kb to be optimal depending on file sizes
            for chunk in iter(lambda: in_file.read(32768), b''):
                hash.update(chunk)
    except PermissionError:
        print("WARN: Permission denied opening " + filepath)
    return (hash.hexdigest(), filepath)


def validate_dir_path(string):
    """
    Works around a bug in PowerShell 5 that appends a double-quote to paths
    containing spaces passed as arguments. This only works when the path is
    passed as the last argument. Put -r <path> at the end of your command on
    PowerShell 5.
    
    https://github.com/python/cpython/issues/84026

    :param string: The path that needs to be validated
    :return: The validated path
    """
    if sys.platform.startswith('win') and string.endswith('"'):
        string = string[:-1]
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
