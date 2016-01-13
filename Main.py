# -*- coding: utf-8 -*-
from GmailCommunication import GmailCommunication
from TestWrapper import TestWrapper
from oauth2client import tools
import time, os, inspect, sys, shutil, argparse

def setupFilesAndFolders(thisDirectory, newDirectory):
    reportsFolder = os.path.join(newDirectory, "Reports")
    sourceCodeFolder = os.path.join(newDirectory, "Attachments")
    pytestConfig = os.path.join(thisDirectory, "conftest.py")
    newpytestConfig = os.path.join(newDirectory, "conftest.py")

    if not os.path.exists(newDirectory):
        os.mkdir(newDirectory)
    if not os.path.exists(reportsFolder):
        os.mkdir(reportsFolder)
    if not os.path.exists(sourceCodeFolder):
        os.mkdir(sourceCodeFolder)

    shutil.copyfile(pytestConfig, newpytestConfig)
    return sourceCodeFolder, reportsFolder

def main(args):
    prevDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    currentDir = args.directory
    testFile = args.testFile

    if currentDir == None:
        currentDir = prevDir
    if testFile == None:
        testFile = os.path.join(currentDir, "Test.py")

    downloadsFolder, reportsFolder = setupFilesAndFolders(prevDir, currentDir)

    gmail = GmailCommunication(args)

    if args.alreadyExistingModules:
        modules = []
        for f in os.listdir(currentDir):
            pathToFile = os.path.join(currentDir,f)
            head, extension = os.path.splitext(pathToFile)
            if os.path.isfile(pathToFile) and extension == ".py" \
            and f != "conftest.py" and not f.lower().startswith("test"):
                modules.append(pathToFile)
        print modules
        for module in modules:
            moduleName = os.path.splitext(os.path.split(module)[1])[0]
            reportFile = os.path.join(reportsFolder, moduleName + ".html")
            print testFile, module, reportFile
            t = TestWrapper(testFile, module, reportFile)
            t.runTests()

    oldMessages = []
    while True:
        print "Recibiendo mensajes"
        messages = gmail.getMessages()
        for m in messages:
            if m['id'] not in oldMessages:
                message = gmail.getMessage(m['id'])
                msgFromMail = gmail.getHeaderFrom(message)
                msgFromName = gmail.getStudentByMail(msgFromMail)
                msgAttachment = gmail.getAttachments(message, downloadsFolder, msgFromName)
                reportFile = os.path.join(reportsFolder, msgFromName + ".html")
                if msgAttachment != "":
                    t = TestWrapper(testFile, msgAttachment, reportFile)
                    t.runTests()
                    gmail.createAndSendMessage(msgFromMail, reportsFolder, msgFromName + ".html")

                oldMessages.append(m['id'])

        time.sleep(60)


if __name__ == '__main__' :

    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument("--dir", dest="directory", help="Directorio donde se trabajará")
    parser.add_argument("--test", dest="testFile", help="Archivo .py con los tests a ejecutar")
    parser.add_argument("--modules", dest="alreadyExistingModules", default=False, help="Asume que existen modulos a testear en la carpeta")

    args = parser.parse_args()
    print args
    print args.directory
    main(args)
