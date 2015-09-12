from TestWrapper import TestWrapper
# for i in range(3):
#     params = "testPy.py --timeout=10 --libname=m" + str(i+1)
#     pytest.main(params)

testPath = "/home/juanjo/Proyectos/Auxiliar/testPy.py"
# for i in range(1,4):
#     t = TestWrapper(testPath, modulePathTemplate + str(i) + ".py")
#     t.runTests()
moduleName = "/home/juanjo/Proyectos/Auxiliar/Attachments/yo.py"
reportFile = "/home/juanjo/Proyectos/Auxiliar/Reports/yo.html"
t = TestWrapper(testPath, moduleName, reportFile)
t.runTests()