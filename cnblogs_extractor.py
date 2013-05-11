#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    This is a script to extract blogs backed up from cnblogs.com to html files
'''
import sys
import getopt
import xml.dom.minidom as minidom
import os
import os.path
import time
import codecs

outputType = "markdown"
categoriesList = []

class Post(object):
    blogNumber=0
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

    def outputMarkdown(self):
        if not os.path.exists("output"):
            os.mkdir("output")
        shortDate = time.strftime("%Y-%m-%d", self.date)
        outputFileName = "output/%s-blog-%d.markdown" % (shortDate, Post.blogNumber)
        Post.blogNumber += 1
        with codecs.open(outputFileName, "w", "utf-8") as writer:
            outputMarkdownHeader(self.title, self.date, self.author, writer)
            outputMarkdownBody(self.content, writer)
        mtime = time.mktime(self.date)
        os.utime(outputFileName, (mtime, mtime))


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

def outputMarkdownHeader(title, date, author, writer):
    writer.write("---\n")
    writer.write("layout: post\n")
    writer.write("title: %s\n" % title)
    writer.write("date: %s\n" % time.strftime("%Y-%m-%d %H:%m", date))
    writer.write("comments: true\n")
    writer.write("author: %s\n" % author)
    category = inputCategory(title)
    writer.write("categories: %s\n" % category)
    writer.write("---\n")

def outputMarkdownBody(content, writer):
    writer.write("%s" %content)

def inputCategory(title):
    optionNumber = 0
    print "------"
    for category in categoriesList:
        print "%d. %s" % (optionNumber, category)
        optionNumber +=1
    print "Choose one category or input a new one for\n\t%s" % title
    print "Note: you'd better use only alphabet charaters for category name."
    while True:
        _input= raw_input()
        addNewCategory = True
        if _input.isdigit():
            number = int(_input)
            if 0 <= number < len(categoriesList):
                categoryName = categoriesList[number]
                addNewCategory = False
            else:
                categoryName = _input
        else:
            categoryName = _input
        print "You choose: %s" % categoryName
        yesOrNo = raw_input("Is this correct[y/N] [defaut: y]?")
        if yesOrNo == 'n' or yesOrNo == 'N':
            print "Choose once again:"
            continue
        if addNewCategory:
            categoriesList.append(categoryName)
        return categoryName

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
    print "Usage: %s [-h] [--help] [-o html/markdown] [--output html/markdown]\
            input-xml-file" % (sys.argv[0])

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
    if outputType == "markdown":
        post.outputMarkdown()
    else:
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
    inputFileName = ""
    if len(sys.argv) < 2:
        usage()
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help","output"])
            if len(args) != 1:
                usage()
                sys.exit(-1)
            else:
                inputFileName = args[0]
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    usage()
                    sys.exit(0)
                elif opt in ("-o", "--output"):
                    if arg=="html" or arg == "markdown":
                        outputType = arg
                    else:
                        usage()
                        sys.exit(-1)
                else:
                    usage()
                    sys.exit(-1)

        except getopt.GetoptError:
            usage()
            sys.exit(-1)
        try:
            parse(inputFileName)
        except Exception, e:
            print e
            sys.exit(-2)
