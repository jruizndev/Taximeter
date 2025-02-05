import unittest
from main import calculate_rate

class TestTaximeter(unittest.TestCase):
    # Test para comprobar la función de cálculo de tarfa en movimiento
    def test_calculate_rate_in_motion(self):
        rate = calculate_rate(10, True)
        self.assertEqual(rate, 0.50)

    # Test para comprobar la función de cálculo de tarfa en parado
    def test_calculate_rate_stopped(self):
        rate = calculate_rate(10, False)
        self.assertEqual(rate, 0.20)