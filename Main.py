# -*- coding: utf-8 -*- 
from GmailCommunication import GmailCommunication
from TestWrapper import TestWrapper
import time, sys, os, inspect

def main(testFile, downloadsFolder, reportsFolder):
    gmail = GmailCommunication()
    oldMessages = []
    while True:
        messages = gmail.getMessages()
        for m in messages:
            if m['id'] not in oldMessages:
                message = gmail.getMessage(m['id'])
                msgFromMail = gmail.getHeaderFrom(message)
                msgFromName = gmail.getStudentByMail(msgFromMail)
                msgAtt = gmail.getAttachments(message, downloadsFolder, msgFromName)
                reportFile = os.path.join(reportsFolder, msgFromName + ".html")
                if msgAtt != "":
                    t = TestWrapper(testFile, msgAtt, reportFile)
                    t.runTests()
                    gmail.createAndSendMessage(msgFromMail, reportsFolder, msgFromName + ".html")

                oldMessages.append(m['id'])
                
        time.sleep(60)

directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if len(sys.argv) > 1:
    directory = sys.argv[0]

reportsFolder = os.path.join(directory, "Reports")
sourceCodeFolder = os.path.join(directory, "Attachments")
testFile = os.path.join(directory, "Test.py")
os.mkdir(reportsFolder)
os.mkdir(sourceCodeFolder)


main(testFile, sourceCodeFolder, reportsFolder)