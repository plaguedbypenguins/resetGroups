#!/usr/bin/python

# rjh; Thu Sep 29 20:27:06 AEST 2022
#
# like split -l, but with \0 delimiting lines.

from __future__ import print_function
import sys, os

# split into N parts
def usage():
    print(sys.argv[0], 'N prefix 0|n')
    print(' where      N - number of chunks to break up stdin into')
    print('       prefix - output filename prefix')
    print('          0|n - \\0 or \\n delimiter in output')
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

if len(sys.argv) != 4:
   usage()

N=int(sys.argv[1])
prefix=sys.argv[2]

delim=sys.argv[3]
if delim == '0':
   delim='\0'
elif delim == 'n':
   delim='\n'
else:
   usage()

a = []
for i in fileLineIter(sys.stdin, inputNewline='\0', outputNewline='', readSize=1024*1024):
   a.append(i)
la=len(a)
print('input items', la)

chunk=(la+N-1)/N
print('chunk', chunk)
cnt=chunk+1
chunknum=0
totalcnt=0
o=None
for i in a:
   if cnt >= chunk:
      if o != None:
         o.close()
         o = None
         print('wrote', cnt, 'to', prefix+'%d' % (chunknum-1))
      if totalcnt != la:
         o = open(prefix + '%d' % chunknum, 'wb')
      cnt=0
      chunknum+=1
   o.write(i+delim)
   cnt+=1
   totalcnt+=1
if o != None:
   print('wrote', cnt, 'to', prefix+'%d' % (chunknum-1))
   o.close()
