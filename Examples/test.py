import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from TestWrapper import TestWrapper
# for i in range(3):
#     params = "testPy.py --timeout=10 --libname=m" + str(i+1)
#     pytest.main(params)

testPath = "/home/juanjo/Proyectos/PythonAuxiliar/Examples/testPy.py"
modulePathTemplate = "/home/juanjo/Proyectos/PythonAuxiliar/Examples/m"
reportPathTemplate = "/home/juanjo/Proyectos/PythonAuxiliar/Examples/Reports/m"
for i in range(1,4):
    t = TestWrapper(testPath, modulePathTemplate + str(i) + ".py", reportPathTemplate + str(i) + ".html")
    t.runTests()
# moduleName = "/home/juanjo/Proyectos/Auxiliar/m1.py"
# reportFile = "/home/juanjo/Proyectos/Auxiliar/Reports/yo.html"
# t = TestWrapper(testPath, moduleName, reportFile)
# t.runTests()