#!/usr/bin/python

# rjh; Mon Oct  3 00:33:48 AEDT 2022
#
# read \0 delimited list of files (must be files and not dirs or other) and stat each.
# output \0 delimited list of those with 1 hard-links to stdout.
#
# also output those multiply linked files that aren't in an 'oz' prefix group.
#  - this takes care of the case where files could be owned by group eg. 'sut' and not quota'd to any oz* group
#  - it doesn't mean that they're in the correct oz* group that matches this path, but at least they're in one of them and a quota will be applied somewhere

from __future__ import print_function
import sys, os, grp

def usage():
    print(sys.argv[0], 'prefix < in > out')
    print('    eg.', sys.argv[0], '/fred < infiles > singlylinkedfiles')
    sys.exit(0)

# see http://bugs.python.org/issue1152248
def fileLineIter(inputFile,
                 inputNewline="\n",
                 outputNewline=None,
                 readSize=8192):
   """Like the normal file iter but you can set what string indicates newline.
   
   The newline string can be arbitrarily long; it need not be restricted to a
   single character. You can also set the read size and control whether or not
   the newline string is left on the end of the iterated lines.  Setting
   newline to '\0' is particularly good for use with an input file created with
   something like "os.popen('find -print0')".
   """
   if outputNewline is None: outputNewline = inputNewline
   partialLine = ''
   while True:
       charsJustRead = inputFile.read(readSize)
       if not charsJustRead: break
       partialLine += charsJustRead
       lines = partialLine.split(inputNewline)
       partialLine = lines.pop()
       for line in lines: yield line + outputNewline
   if partialLine: yield partialLine

if len(sys.argv) != 2:
   usage()

prefix=sys.argv[1]

for i in fileLineIter(sys.stdin, inputNewline='\0', outputNewline='', readSize=1024*1024):
   try:
      s = os.stat(prefix + '/' + i)
   except:
      continue
   if s.st_nlink == 1:
      sys.stdout.write(i + '\0')
   else:
      # lookup group name from gid
      g = grp.getgrgid(s.st_gid).gr_name
      if g[:2] != 'oz':
         sys.stdout.write(i + '\0')
