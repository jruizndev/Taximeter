import unittest
from unittest.mock import patch
from main import calculate_rate
from config import TIME_SLOTS

class TestTaximeter(unittest.TestCase):
   # Test para comprobar la función de cálculo de tarfa en movimiento: tarifa valle
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_low(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['low_demand']
       expected_rate = 10 * TIME_SLOTS['low_demand']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)

   # Test para comprobar la función de cálculo de tarfa en parado: tarifa valle
   @patch('main.get_current_rate')
   def test_calculate_rate_stopped_low(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['low_demand']
       expected_rate = 10 * TIME_SLOTS['low_demand']['stopped_rate'] 
       rate = calculate_rate(10, False)
       self.assertEqual(rate, expected_rate)

   # Test para probar el cálcu.lo de la tarifa total acumulada en un trayecto cambiado de estado: tarifa valle
   @patch('main.get_current_rate')
   def test_accumulated_rate_with_state_change_low(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['low_demand']
       stopped = 10 * TIME_SLOTS['low_demand']['stopped_rate']  
       in_motion = 10 * TIME_SLOTS['low_demand']['motion_rate']  
       expected_total = stopped + in_motion   

       first_rate = calculate_rate(10, False)
       second_rate = calculate_rate(10, True)
       self.assertEqual(first_rate + second_rate, expected_total)

       # Test para comprobar la función de cálculo de tarfa en movimiento: tarifa normal
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_normal(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['normal']
       expected_rate = 10 * TIME_SLOTS['normal']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)