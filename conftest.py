import pytest
import sys
import imp
def pytest_addoption(parser):
    parser.addoption("--libname", action="store", default="",
                     help="name of the tested library")

def pytest_generate_tests(metafunc):
    if 'libPath' in metafunc.fixturenames:
        metafunc.parametrize("libPath", metafunc.config.option.libname)

@pytest.fixture(scope="module")
def module(request):
    libPath = request.config.getoption("--libname")
    if libPath in sys.modules:
        del sys.modules[libPath]
    moduleToBeTested = imp.load_source(libPath, libPath)
    return moduleToBeTested