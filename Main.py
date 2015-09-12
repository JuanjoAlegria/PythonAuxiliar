# -*- coding: utf-8 -*- 
from GmailCommunication import GmailCommunication
from TestWrapper import TestWrapper
import time


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
                reportFile = reportsFolder + msgFromName + ".html"
                if msgAtt != "":
                    t = TestWrapper(testFile, msgAtt, reportFile)
                    t.runTests()
                    gmail.createAndSendMessage(msgFromMail, reportsFolder, msgFromName + ".html")

                oldMessages.append(m['id'])
                
        time.sleep(60)

codeFolder = "/home/juanjo/Proyectos/Auxiliar/Attachments/"
reportsFolder = "/home/juanjo/Proyectos/Auxiliar/Reports/"
testFile = "/home/juanjo/Proyectos/Auxiliar/testPy.py"
main(testFile, codeFolder, reportsFolder)