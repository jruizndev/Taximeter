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

    # Test para probar el cálcu.lo de la tarifa total acumulada en un trayecto cambiado de estado
    def test_acummulated_rate_with_state_change(self):
        first_rate = calculate_rate(10, False)
        second_rate = calculate_rate(10, True)
        total_rate =first_rate + second_rate
        self.assertEqual(total_rate, 0.70)
