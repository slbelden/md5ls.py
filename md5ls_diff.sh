#!/usr/bin/env bash

# Removes all lines from list2 which have a matching md5sum present in list1.
# List1 will remain unchanged.
# List2 will be altered in-place.
#
# List1 and List2 must be the output of the md5ls bash command chain:
# https://gist.github.com/slbelden/3653c9d50be88011a273beb48406b7a3


# For each line in file1,
#     Extract the md5sum (first 32 chars)
#     Remove lines in file 2 containing that md5sum


while IFS= read -r line || [[ -n "$line" ]]
do
	sed -i "/${line:0:32}/d" $2
done < "$1" 
