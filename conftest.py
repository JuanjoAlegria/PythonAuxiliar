def pytest_addoption(parser):
    parser.addoption("--libname", action="append", default=[],
                     help="name of the tested library")

def pytest_generate_tests(metafunc):
    if 'libPath' in metafunc.fixturenames:
        metafunc.parametrize("libPath", metafunc.config.option.libname)