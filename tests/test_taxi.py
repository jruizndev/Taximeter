import unittest
from main import calculate_rate

# Test para comprobar la función de cálculo de tarfa en movimiento
class TestTaximeter(unittest.TestCase):
    def test_calculate_rate_in_motion(self):
        rate = calculate_rate(10, True)
        self.assertEqual(rate, 0.50)

