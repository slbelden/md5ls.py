#!/usr/bin/env python3

import argparse

from md5ls.create import create
from md5ls.diff import diff

def main():
    # top-level
    parser = argparse.ArgumentParser(
        prog='md5ls',
        description='Tools for verifying files with hash-list manifests')
    subparsers = parser.add_subparsers(
        help='use "md5ls <subcommand> -h" for detailed help')

    # subcommand: create
    parser_create = subparsers.add_parser(
        'create',
        help='create a new list of hashes and files')
    parser_create.add_argument(
        '-r',
        '--rootDir',
        action='store',
        default='.',
        dest='root_dir',
        help='root directory to walk (default: "."). '
            +'Output filepaths will be relative to this directory.')
    parser_create.add_argument(
        '-o',
        '--outFile',
        action='store',
        dest='out_file',
        help='write output to a file instead of stdout. '
            +'Specifying an output file is highly recommended over using '
            +'terminal output redirection, as terminal output may have '
            +'OS-dependent newlines or character set encoding. '
            +'No checks are performed! Will overwrite OUT_FILE if it exists!')
    parser_create.add_argument(
        '-j',
        '--jobs',
        action='store',
        type=int,
        default=1,
        choices=range(1,61), # prevents wait() handles exceeding limit
        metavar="[1-60]",
        dest='num_jobs',
        help='number of worker processes to use (default: 1). '
            +'Set to 2 or greater to enable multithreading. '
            +'Recommended value = number of physical CPU cores available. '
            +"Experimental. Huge performance gains, but doesn't like CTRL-C.")
    parser_create.add_argument(
        '-k1',
        '--k1',
        action='store_true',
        help='sort output list by MD5 sum instead of by filepath. '
            +'Useful for grouping duplicate files together in the output.'
    )
    parser_create.set_defaults(func=create)

    # subcommand: diff
    parser_diff = subparsers.add_parser(
    'diff',
    help='compare two existing lists of hashes')
    parser_diff.add_argument(
        'left_file',
        help='first of two files to compare')
    parser_diff.add_argument(
        'right_file',
        help='second of two files to compare')
    parser_diff.add_argument(
        '-s',
        '--summary',
        action='store_true',
        help='output a summary of changes only, no hashes or paths will be '
            +'printed.')
    parser_diff.add_argument(
        '-o',
        '--outFile',
        action='store',
        dest='out_file',
        help='write output to a file instead of stdout. '
            +'Specifying an output file is highly recommended over using '
            +'terminal output redirection, as terminal output may have '
            +'OS-dependent newlines or character set encoding. '
            +'No checks are performed! Will overwrite OUT_FILE if it exists!')
    parser_diff.set_defaults(func=diff)
    
    # run selected subcommand
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        parser.exit()


if __name__ == "__main__":
    main()
