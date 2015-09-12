import unittest
import fact2
from timeoutV2 import timeout

class TestFact(unittest.TestCase):
    
    @timeout(t=10)
    def test_1(self):
        self.assertEqual(fact2.fact(20), 120, "incorrect fact")


suite = unittest.TestLoader().loadTestsFromTestCase(TestFact)
unittest.TextTestRunner(verbosity=2).run(suite)
