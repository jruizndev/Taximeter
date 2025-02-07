import unittest
from unittest.mock import patch
from main import calculate_rate
from config import TIME_SLOTS

class TestTaximeter(unittest.TestCase):
    # Test para comprobar la función de cálculo de tarifa en movimiento: tarifa punta mañana
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_morning(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['morning_rush']
       expected_rate = 10 * TIME_SLOTS['morning_rush']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)

    # Test para comprobar la función de cálculo de tarifa en parado: tarifa punta mañana
   @patch('main.get_current_rate')
   def test_calculate_rate_stopped_morning(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['morning_rush']
       expected_rate = 10 * TIME_SLOTS['morning_rush']['stopped_rate'] 
       rate = calculate_rate(10, False)
       self.assertEqual(rate, expected_rate)

    # Test para probar el cálculo de la tarifa total acumulada en un trayecto cambiado de estado: tarifa punta mañana
   @patch('main.get_current_rate')
   def test_accumulated_rate_with_state_change_morning(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['morning_rush']
       stopped = 10 * TIME_SLOTS['morning_rush']['stopped_rate']  
       in_motion = 10 * TIME_SLOTS['morning_rush']['motion_rate']  
       expected_total = stopped + in_motion   

       first_rate = calculate_rate(10, False)
       second_rate = calculate_rate(10, True)
       self.assertEqual(first_rate + second_rate, expected_total)

    # Test para comprobar la función de cálculo de tarifa en movimiento: tarifa punta tarde
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_evening(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['evening_rush']
       expected_rate = 10 * TIME_SLOTS['evening_rush']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)

    # Test para comprobar la función de cálculo de tarifa en parado: tarifa punta tarde
   @patch('main.get_current_rate')
   def test_calculate_rate_stopped_evening(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['evening_rush']
       expected_rate = 10 * TIME_SLOTS['evening_rush']['stopped_rate'] 
       rate = calculate_rate(10, False)
       self.assertEqual(rate, expected_rate)

    # Test para probar el cálculo de la tarifa total acumulada en un trayecto cambiado de estado: tarifa punta tarde
   @patch('main.get_current_rate')
   def test_accumulated_rate_with_state_change_evening(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['evening_rush']
       stopped = 10 * TIME_SLOTS['evening_rush']['stopped_rate']  
       in_motion = 10 * TIME_SLOTS['evening_rush']['motion_rate']  
       expected_total = stopped + in_motion   

       first_rate = calculate_rate(10, False)
       second_rate = calculate_rate(10, True)
       self.assertEqual(first_rate + second_rate, expected_total)

    # Test para comprobar la función de cálculo de tarifa en movimiento: tarifa noche
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_night(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['night_life']
       expected_rate = 10 * TIME_SLOTS['night_life']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)

    # Test para comprobar la función de cálculo de tarifa en parado: tarifa noche
   @patch('main.get_current_rate')
   def test_calculate_rate_stopped_night(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['night_life']
       expected_rate = 10 * TIME_SLOTS['night_life']['stopped_rate'] 
       rate = calculate_rate(10, False)
       self.assertEqual(rate, expected_rate)

   # Test para comprobar la función de cálculo de tarifa en movimiento: tarifa valle
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_low(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['low_demand']
       expected_rate = 10 * TIME_SLOTS['low_demand']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)

   # Test para comprobar la función de cálculo de tarifa en parado: tarifa valle
   @patch('main.get_current_rate')
   def test_calculate_rate_stopped_low(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['low_demand']
       expected_rate = 10 * TIME_SLOTS['low_demand']['stopped_rate'] 
       rate = calculate_rate(10, False)
       self.assertEqual(rate, expected_rate)

   # Test para probar el cálculo de la tarifa total acumulada en un trayecto cambiado de estado: tarifa valle
   @patch('main.get_current_rate')
   def test_accumulated_rate_with_state_change_low(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['low_demand']
       stopped = 10 * TIME_SLOTS['low_demand']['stopped_rate']  
       in_motion = 10 * TIME_SLOTS['low_demand']['motion_rate']  
       expected_total = stopped + in_motion   

       first_rate = calculate_rate(10, False)
       second_rate = calculate_rate(10, True)
       self.assertEqual(first_rate + second_rate, expected_total)

    # Test para comprobar la función de cálculo de tarifa en movimiento: tarifa normal
   @patch('main.get_current_rate')
   def test_calculate_rate_in_motion_normal(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['normal']
       expected_rate = 10 * TIME_SLOTS['normal']['motion_rate']  
       rate = calculate_rate(10, True)
       self.assertEqual(rate, expected_rate)
    
    # Test para comprobar la función de cálculo de tarifa en parado: tarifa normal
   @patch('main.get_current_rate')
   def test_calculate_rate_stopped_normal(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['normal']
       expected_rate = 10 * TIME_SLOTS['normal']['stopped_rate'] 
       rate = calculate_rate(10, False)
       self.assertEqual(rate, expected_rate)
    
    # Test para probar el cálculo de la tarifa total acumulada en un trayecto cambiado de estado: tarifa normal
   @patch('main.get_current_rate')
   def test_accumulated_rate_with_state_change_normal(self, mock_get_rate):
       mock_get_rate.return_value = TIME_SLOTS['normal']
       stopped = 10 * TIME_SLOTS['normal']['stopped_rate']  
       in_motion = 10 * TIME_SLOTS['normal']['motion_rate']  
       expected_total = stopped + in_motion   

       first_rate = calculate_rate(10, False)
       second_rate = calculate_rate(10, True)
       self.assertEqual(first_rate + second_rate, expected_total)