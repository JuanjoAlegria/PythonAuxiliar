import pytest

class TestWrapper:
    def __init__(self, testSuitPath, modulePath, htmlFile):
        self.testSuitPath = testSuitPath
        self.modulePath = modulePath
        self.htmlFile = htmlFile


    def runTests(self):
        params = self.testSuitPath + " -s --timeout=10 --libname=" + self.modulePath + " --html=" + self.htmlFile
        pytest.main(str(params))
