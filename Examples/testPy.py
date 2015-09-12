def test_suma(module):
    assert module.suma(3,4) == 7
    assert module.suma(0,0) == 0
    assert module.suma(9,-8) == 1


def test_mult(module):
    assert module.mult(3,4) == 12
    assert module.mult(0,0) == 0
    assert module.mult(9,-8) == -72


def test_div(module):
    assert module.div(3,4) == 0.75
    assert module.div(0,1) == 0
    assert module.div(9,-3) == -3