import sys
def test_import(libPath):
    import imp
    if libPath in sys.modules:
        del sys.modules[libPath]
    tested_library = imp.load_source(libPath, libPath)
    assert tested_library.foo() == 1


