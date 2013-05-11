#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    This is a script to extract blogs backed up from cnblogs.com to html files
'''
import sys
import xml.dom.minidom as minidom
import os
import os.path
import time
import codecs

class Post(object):
    def setTitle(self, title):
        self.title = title
    def setAuthor(self, author):
        self.author = author
    def setDate(self, date):
        self.date = date
    def setContent(self, content):
        self.content = content
    def outputHTML(self):
        if not os.path.exists("output"):
            os.mkdir("output")
        with codecs.open("output/"+self.title+".html", "w", "utf-8") as writer:
            outputHTMLHeader(self.title, self.author, writer)
            outputHTMLBody(self.title, self.date, self.content, writer)

def outputHTMLHeader(title, author, writer):
    writer.write('<!DOCTYPE html>')
    writer.write('<html>')
    writer.write('<head>')
    writer.write('  <meta charset="utf-8">')
    print title
    writer.write('  <title>%s</title>' % (title))
    writer.write('  <meta name="author" content="%s">' % (author))
    writer.write('</head>')

def outputHTMLBody(title, date, content, writer):
    writer.write('<body>')
    writer.write('<h1>%s</h1>' % (title))
    writer.write('<div class="date">%s</div>' % (time.strftime("%Y-%m-%d", date)))
    writer.write('<div class="content">%s</div>' % (content))
    writer.write('</body></html>')

def checkXMLFile(filePath):
    '''Check the input file'''
    if os.path.exists(filePath):
        if filePath[-4:].lower() == ".xml":
            return True
        else:
            print "'%s' is not a XML file" % (filePath)
            return False
    else:
        print "'%s' does not exist" % (filePath)
        return False

def usage():
    ''' Print the usage of the script'''
    print "Usage: %s <input-xml-file>" % (sys.argv[0])

def parse(filePath):
    ''' Parse the xml file'''
    if not checkXMLFile(filePath):
        return
    dom = minidom.parse(filePath)
    chanel = dom.childNodes[0].childNodes[0]
    itemList = chanel.getElementsByTagName("item")
    for item in itemList:
        parseItem(item)

def parseItem(item):
    post = Post()
    titleName = getItemMemberText(item, "title")
    post.setTitle(titleName)
    authorName = getItemMemberText(item, "author")
    post.setAuthor(authorName)
    dateString = getItemMemberText(item, "pubDate")
    date = time.strptime(dateString, "%a, %d %b %Y %H:%M:%S GMT")
    post.setDate(date)
    content = getItemMemberText(item, "description")
    post.setContent(content)
    post.outputHTML()

def getItemMemberText(item, memberName):
    member = item.getElementsByTagName(memberName)[0]
    return getText(member.childNodes)

def getText(nodeList):
    rc = []
    for node in nodeList:
        if node.nodeType == node.TEXT_NODE\
                or node.nodeType == node.CDATA_SECTION_NODE:
            rc.append(node.data)
    return "".join(rc)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        try:
            parse(sys.argv[1])
        except Exception, e:
            print e
