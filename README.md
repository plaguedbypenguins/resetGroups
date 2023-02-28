# resetGroups

`resetGroups` is a script to sweep over a large [Lustre](https://www.lustre.org/) filesystem and reset group ownership of files and dirs to match the project name.

only correct files and dirs that are incorrect. add setgid on dirs if they're missing.

detect hard-linked files that might reside in multiple projects so that they aren't flip-flop'd between multiple groups on every sweep.

files with weird names (spaces, unicode, etc.) are handled correctly.

Setup
-----
edit paths and things at the top of `resetGroups` for your filesystem.

all our project directories start with 'oz' (eg. oz777) and that is hard-coded in a bunch of places in the main `resetGroups` script and also once in `findMultiplyLinkedFiles.py`. change that to match whatever your projects are called.

this script assumes that the project directory name is the same as the unix group name. if that isn't true for you then maybe add code to grab the group name from the project dir.

Running
-------
the script runs on one Lustre client. by default it does operations on 10 to 15 things at a time. load on the client is low.

the time that the script takes to run will vary a lot depending upon filesystem speed, load, size, how many crazy dirs with 100M files in them you have, and the number of files/dirs that need correcting.

for us it can usually scan 500M files and correct permissions on approx 4M of them in less than 24 hours. we run it about once a month.

Alternatives
------------
presumably this is the type of thing people setup [RobinHood](https://github.com/cea-hpc/robinhood/wiki) to help with, but we've never got around to it.


Robin Humble, 2023
