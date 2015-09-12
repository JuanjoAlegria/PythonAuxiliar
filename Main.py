# -*- coding: utf-8 -*- 
from GmailCommunication import GmailCommunication
from TestWrapper import TestWrapper
import time, os, inspect, sys, shutil

def main(testFile, downloadsFolder, reportsFolder):
    gmail = GmailCommunication()
    oldMessages = []
    while True:
        print "Recibiendo mensajes"
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


def helpMessage():
    s = 'Obtiene modulos a testear desde una cuenta de Gmail los testea y luego envía un reporte\n'
    s+= 'Argumentos opcionales:\n'
    s+= '\t --dir \t [DIRECTORIO] \t Directorio donde se trabajará\n'
    s+= '\t --test \t [TESTFILE] \t Archivo .py con los tests a ejecutar\n'
    return s

if __name__ == '__main__' :
    thisDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = ""
    testFile = ""

    if len(sys.argv) > 1 and sys.argv[1] == "--h":
        print helpMessage()
        sys.exit(0)

    for arg in sys.argv:
        if arg.startswith("--dir"):
            directory = arg[6:]
        if arg.startswith("--test"):
            testFile = arg[11:]

    if directory == "":
        directory = thisDirectory
    if testFile == "":
        testFile = os.path.join(directory, "Test.py")

    reportsFolder = os.path.join(directory, "Reports")
    sourceCodeFolder = os.path.join(directory, "Attachments")
    pytestConfig = os.path.join(thisDirectory, "conftest.py")
    newpytestConfig = os.path.join(directory, "conftest.py")

    if not os.path.exists(reportsFolder):
        os.mkdir(reportsFolder)
    if not os.path.exists(sourceCodeFolder):
        os.mkdir(sourceCodeFolder)  

    shutil.copyfile(pytestConfig, newpytestConfig)
    main(testFile, sourceCodeFolder, reportsFolder)