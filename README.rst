=====
md5ls
=====

Tools for verifying files with hash-list manifests.

Motivation
==========
To verify that my backups restore without errors, I was using `this classic Bash
one-liner <https://gist.github.com/slbelden/3653c9d50be88011a273beb48406b7a3>`_:

    ``find . -type f -exec md5sum {} + | LC_ALL=C sort -k2``

Eventually the limitations of this approach became burdensome, so I created a
one-to-one python implementation. When run without arguments, the command:

    ``md5ls create``

produces output identical to the bash command (on all tested systems).

The project has grown to include many quality-of-life improvements and
additional features.

Benefits
========
If all you need is the behavior of the original Bash command, here are some
quality-of-life features that make this Python version worth using:

Speed
-----
Use multithreading to greatly improve performance:

    ``md5ls create -j 8``
    
where 8 can be replaced with the number of CPU cores available to you. Just 6
threads can produce a 10x performance improvement over the bash version in my
testing.

Ease of Use
-----------
The Bash version requires that you ``cd`` into the directory you are generating
a manifest for, since ``find .`` must use the current working directory as its
root to get consistent relative filepaths in the output. The ``-r`` option
allows you to run the command from anywhere by specifying the directory:

    ``md5ls create -r /path/dir/folder/``

Cross-Platform Support
----------------------
Use the -o flag to generate a consistent manifest on all* systems:

    ``md5ls create -o /folder/file.out``

The file will always have unix-style line endings, and use unix-style folder
separators, even when run on Windows. This allows easy ``diff`` comparisons
between two manifests, even between different platforms.

\*tested on Windows 10 & 11, Ubuntu 22.04

Better diff
-----------
You can use a basic ``diff`` command to compare two manifests:

    ``diff file1.out file2.out``

but the output can be hard to read, especially if there are many differences.
Instead, I've created ``md5ls diff`` to produce more human-readable output.
By default, the output adds headings and sorts changes into sections:

    ``md5ls diff file1.out file2.out``

Generate only a summary of changes, without the full list of lines with ``-s``:

    ``md5ls diff file1.out file2.out -s``

Usage
=====
md5ls is intended to by run at the command line as a module:

    ``python3 -m md5ls``

Get basic usage help with ``-h``:

    ``python3 -m md5ls -h``

And subcommand help in the same manner:

    ``python3 -m md5ls create -h``
