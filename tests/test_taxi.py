import unittest
from unittest.mock import patch
from main import Taximeter, Trip, RateCalculator
from config.config import TIME_SLOTS, SPECIAL_CONDITIONS

class TestTaximeter(unittest.TestCase):
    def setUp(self):
        self.taximeter = Taximeter()
        self.trip = Trip(self.taximeter.rate_calculator)

    # Validación función de cálculo de tarifa en movimiento: tarifa punta mañana
    def test_calculate_rate_in_motion_morning(self):
        with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['morning_rush']):
            self.trip.in_motion = True
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['morning_rush']['motion_rate']
            self.assertEqual(rate, expected_rate)
      

   # Validación función de cálculo de tarifa en parado: tarifa punta mañana
    def test_calculate_rate_stopped_morning(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['morning_rush']):
            self.trip.in_motion = False
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['morning_rush']['stopped_rate']
            self.assertEqual(rate, expected_rate)

   # Validación de cáculo de tarifa con estado parado y en movimiento: tarifa punta mañana
    def test_accumulated_rate_with_state_change_morning(self):
        with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['morning_rush']):
            self.trip.in_motion = False
            first_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            self.trip.in_motion = True
            second_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            expected_total = first_rate + second_rate
            self.assertEqual(first_rate + second_rate, expected_total)

   # Validación función de cálculo de tarifa en movimiento: tarifa punta tarde
    def test_calculate_rate_in_motion_evening(self):
        with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['evening_rush']):
            self.trip.in_motion = True
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['evening_rush']['motion_rate']
            self.assertEqual(rate, expected_rate)

   # Validación función de cálculo de tarifa en parado: tarifa punta tarde
    def test_calculate_rate_stopped_evening(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['evening_rush']):
            self.trip.in_motion = False
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['evening_rush']['stopped_rate']
            self.assertEqual(rate, expected_rate)

   # Validación de cáculo de tarifa con estado parado y en movimiento: tarifa punta tarde
    def test_accumulated_rate_with_state_change_evening(self):
      with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['evening_rush']):
            self.trip.in_motion = False
            first_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            self.trip.in_motion = True
            second_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            expected_total = first_rate + second_rate
            self.assertEqual(first_rate + second_rate, expected_total)

   # Validación función de cálculo de tarifa en movimiento: tarifa noche
    def test_calculate_rate_in_motion_night(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['night_life']):
            self.trip.in_motion = True
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['night_life']['motion_rate']
            self.assertEqual(rate, expected_rate)

   # Validación función de cálculo de tarifa en parado: tarifa noche
    def test_calculate_rate_stopped_night(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['night_life']):
            self.trip.in_motion = False
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['night_life']['stopped_rate']
            self.assertEqual(rate, expected_rate)

   # Validación de cáculo de tarifa con estado parado y en movimiento: tarifa noche
    def test_accumulated_rate_with_state_change_night(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['night_life']):
            self.trip.in_motion = False
            first_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            self.trip.in_motion = True
            second_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            expected_total = first_rate + second_rate
            self.assertEqual(first_rate + second_rate, expected_total)

   # Validación función de cálculo de tarifa en movimiento: tarifa valle
    def test_calculate_rate_in_motion_low(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['low_demand']):
            self.trip.in_motion = True
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['low_demand']['motion_rate']
            self.assertEqual(rate, expected_rate)

   # Validacion función de cálculo de tarifa en parado: tarifa valle
    def test_calculate_rate_stopped_low(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['low_demand']):
            self.trip.in_motion = False
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['low_demand']['stopped_rate']
            self.assertEqual(rate, expected_rate)

   # Validación de cáculo de tarifa con estado parado y en movimiento: tarifa valle
    def test_accumulated_rate_with_state_change_low(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['low_demand']):
            self.trip.in_motion = False
            first_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            self.trip.in_motion = True
            second_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            expected_total = first_rate + second_rate
            self.assertEqual(first_rate + second_rate, expected_total)

   # Validación función de cálculo de tarifa en movimiento: tarifa normal
    def test_calculate_rate_in_motion_normal(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['normal']):
            self.trip.in_motion = True
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['normal']['motion_rate']
            self.assertEqual(rate, expected_rate)
   
   # Validaciónfunción de cálculo de tarifa en parado: tarifa normal
    def test_calculate_rate_stopped_normal(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['normal']):
            self.trip.in_motion = False
            segment_time = 10  
            rate = self.trip.rate_calculator.calculate_rate(segment_time, self.trip.in_motion)

            expected_rate = 10 * TIME_SLOTS['normal']['stopped_rate']
            self.assertEqual(rate, expected_rate)
   
   # Validación de cáculo de tarifa con estado parado y en movimiento: tarifa normal
    def test_accumulated_rate_with_state_change_normal(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value=TIME_SLOTS['normal']):
            self.trip.in_motion = False
            first_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            self.trip.in_motion = True
            second_rate = self.trip.rate_calculator.calculate_rate(10, self.trip.in_motion)

            expected_total = first_rate + second_rate
            self.assertEqual(first_rate + second_rate, expected_total)

   # Validación multiplicador de tarifa en condición de lluvia
    def test_calculate_rate_with_rain_condition(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value = TIME_SLOTS['normal']):
        segment_time = 10
        rate = self.trip.rate_calculator.calculate_rate(segment_time, True, 'rain')

       expected_rate = 10 * TIME_SLOTS['normal']['motion_rate'] * SPECIAL_CONDITIONS['rain']
       self.assertEqual(rate, expected_rate)

    # Test para verificar multiplicador de tarifa en eventos
    def test_calculate_rate_with_events_condition(self):
       with patch.object(RateCalculator, 'get_current_rate', return_value = TIME_SLOTS['normal']):
        segment_time = 10
        rate = self.trip.rate_calculator.calculate_rate(segment_time, True, 'events')

       expected_rate = 10 * TIME_SLOTS['normal']['motion_rate'] * SPECIAL_CONDITIONS['events']
       self.assertEqual(rate, expected_rate)