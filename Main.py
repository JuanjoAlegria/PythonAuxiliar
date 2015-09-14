# -*- coding: utf-8 -*- 
from GmailCommunication import GmailCommunication
from TestWrapper import TestWrapper
import time, os, inspect, sys, shutil

def setupFilesAndFolders(thisDirectory, newDirectory):
    reportsFolder = os.path.join(newDirectory, "Reports")
    sourceCodeFolder = os.path.join(newDirectory, "Attachments")
    pytestConfig = os.path.join(thisDirectory, "conftest.py")
    newpytestConfig = os.path.join(newDirectory, "conftest.py")

    if not os.path.exists(reportsFolder):
        os.mkdir(reportsFolder)
    if not os.path.exists(sourceCodeFolder):
        os.mkdir(sourceCodeFolder)  

    shutil.copyfile(pytestConfig, newpytestConfig)
    return sourceCodeFolder, reportsFolder

def main(testFile, prevDir, currentDir, alreadyExistingModules = False):

    downloadsFolder, reportsFolder = setupFilesAndFolders(prevDir, currentDir)

    gmail = GmailCommunication()

    if alreadyExistingModules:
        modules = []
        for f in os.listdir(currentDir):
            pathToFile = os.path.join(currentDir,f)
            head, extension = os.path.splitext(pathToFile)
            if os.path.isfile(pathToFile) and extension == ".py" \
            and f != "conftest.py" and not f.lower().startswith("test"):
                modules.append(f)
        print modules
        for module in modules:
            moduleName = os.path.splitext(os.path.split(module)[1])[0]
            reportFile = os.path.join(reportsFolder, moduleName + ".html")
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


def helpMessage():
    s = 'Obtiene modulos a testear desde una cuenta de Gmail los testea y luego envía un reporte\n'
    s+= 'Argumentos opcionales:\n'
    s+= '\t --dir \t [DIRECTORIO] \t Directorio donde se trabajará\n'
    s+= '\t --test \t [TESTFILE] \t Archivo .py con los tests a ejecutar\n'
    s+= '\t --modules Asume que existen modulos a testear en la carpeta\n'
    return s

if __name__ == '__main__' :
    thisDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = ""
    testFile = ""
    alreadyExistingModules = False

    if len(sys.argv) > 1 and sys.argv[1] == "--h":
        print helpMessage()
        sys.exit(0)

    for arg in sys.argv:
        if arg.startswith("--dir"):
            directory = arg[6:]
        if arg.startswith("--test"):
            testFile = arg[11:]
        if arg.startswith("--modules"):
            alreadyExistingModules = True

    if directory == "":
        directory = thisDirectory
    if testFile == "":
        testFile = os.path.join(directory, "Test.py")



    main(testFile, thisDirectory, directory, alreadyExistingModules)