import unittest
from main import calculate_rate
from config import TIME_SLOTS 

class TestTaximeter(unittest.TestCase):
    # Test para comprobar la función de cálculo de tarfa en movimiento: tarifa valle
    def test_calculate_rate_in_motion_low(self):
        expected_rate = 10 * TIME_SLOTS['low_demand']['motion_rate']  
        rate = calculate_rate(10, True)
        self.assertEqual(rate, expected_rate)

    # Test para comprobar la función de cálculo de tarfa en parado: tarifa valle
    def test_calculate_rate_stopped_low(self):
        expected_rate = 10 * TIME_SLOTS['low_demand']['stopped_rate'] 
        rate = calculate_rate(10, False)
        self.assertEqual(rate, expected_rate)

    # Test para probar el cálcu.lo de la tarifa total acumulada en un trayecto cambiado de estado: tarifa valle
    def test_acummulated_rate_with_state_change_low(self):
        stopped = 10 * TIME_SLOTS['low_demand']['stopped_rate']  
        in_motion = 10 * TIME_SLOTS['low_demand']['motion_rate']  
        expected_total = stopped + in_motion  

        first_rate = calculate_rate(10, False)
        second_rate = calculate_rate(10, True)
        self.assertEqual(first_rate + second_rate, expected_total)
