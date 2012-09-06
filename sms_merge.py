#!/usr/bin/env python

import sys
import pdb
import re


def main(args):
    if len(args) < 2:
        print "Usage: %s <ARG1>" % (args[0])
        exit(1)

    allXML = []

    fp = open(args[1], "r")
    numThreads = 0
    numMsgs = 0
    try:
        while True:
            line = fp.next()
            if line.startswith(r"<?xml"):
                print "Parsing new XML root"
                curXML = XMLObj(line)
                allXML.append(curXML)

            elif line.startswith(r'<threads'):
                start = len('<threads count="')
                stop = -len('" xmlns="http://www.titaniumtrack.com/ns/titanium-backup/messages">') - 1
                totalThreads =  int(line[start:stop])
                print "Parsing %s threads" % (totalThreads)

            elif line.startswith(r'<thread '):
                #print line
                start = len('<thread address="')
                stop = -1 - len('">')
                addr = line[start:stop]
                print "Parsing single thread %s:" % (addr),
                curXML.addThread(addr)
            elif line.startswith(r'</thread>'):
                numThreads += 1
                print "thread Done"

            elif line.startswith(r'<mms'):
                sys.stdout.write("!")
                msg = line
                while not line.endswith("</mms>\n"):
                    line = fp.next()
                    msg += line
                numMsgs += 1
                curXML.addMsg(msg)

            elif line.startswith(r'<sms'):
                sys.stdout.write(".")
                msg = line
                while not line.endswith("</sms>\n"):
                    line = fp.next()
                    msg += line
                numMsgs += 1
                curXML.addMsg(msg)
            else:
                print line[:50]
    except StopIteration as e:
        print "File finished"
        print e

    print "Parsed %s threads" % (numThreads)
    print "Parsed %s messages" % (numMsgs)
    assert(numThreads == totalThreads)
    curXML.saveToFile("out.xml")



class XMLObj(object):
    threadsLine = ('<threads count="','" xmlns="http://www.titaniumtrack.com/ns/titanium-backup/messages">')

    def __init__(self, header):
        self.header = header
        self.threads = {} #A dict keyed by address of msg lines keyed by date
        self.curThread = None
        self.duplicates = 0

    def addThread(self, address):
        self.curThread = self.threads.setdefault(address, {})

    def addMsg(self, msg):
        date = re.findall(r'date="([-\d:.TZ]+)"', msg)[0]
        if date in self.curThread:
            self.duplicates += 1
            if msg != self.curThread[date]:
                print "\nDUPLICATING MESSAGE %s" % (date)
                self.curThread[date]+= "\n" + msg
        else:
            self.curThread[date] = msg

    def saveToFile(self, fname):
        fp = open(fname, "w")
        print >> fp, self.header
        print >>fp, "%s%d%s" % (XMLObj.threadsLine[0], len(self.threads), XMLObj.threadsLine[1])
        for addr in self.threads:
            printThread(fp, addr, self.threads[addr])
        print>> fp, "</threads>"

def printThread(fp, addr, thread):
    print >>fp, '<thread address="%s">' % (addr)
    for msg in thread.values():
        printMsg(fp, msg)
    print >>fp, '</thread>'

def printMsg(fp, msg):
    print >> fp, msg,
    

if __name__ == "__main__":
    main(sys.argv)
    exit(0)
