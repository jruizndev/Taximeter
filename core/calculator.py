from datetime import datetime
from config.config import TIME_SLOTS, SPECIAL_CONDITIONS

# Manejo de cáculos de tarifas según horario y condiciones
class RateCalculator:
   
   @staticmethod
   # Determina tarifa según hora actual
   def get_current_rate():
       current_time = datetime.now().time()
       current_str = current_time.strftime('%H:%M')

       for slot_name, slot_info in TIME_SLOTS.items():
           if slot_name == 'normal':
               continue
           if slot_info['start'] <= current_str <= slot_info['end']:
               return slot_info
       return TIME_SLOTS['normal']

    # Calcula tarifa según estado y condiciones
   @staticmethod
   def calculate_rate(elapsed_time, in_motion, special_condition=None):
       current_rates = RateCalculator.get_current_rate()
       base_rate = current_rates['motion_rate'] if in_motion else current_rates['stopped_rate']
       
       if special_condition in SPECIAL_CONDITIONS:
           base_rate *= SPECIAL_CONDITIONS[special_condition]
       
       return elapsed_time * base_rate