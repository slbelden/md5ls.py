"""
md5ls.py - List files and their MD5 sums

Python implementation of the Bash one-liner:
'find . -type f -exec md5sum {} + | LC_ALL=C sort -k2'
with some quality-of-life additions.

help: md5ls.py -h
"""

__version__ = "0.1"
