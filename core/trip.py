import time

# Clase para gestionar viajes
class Trip:
   def __init__(self, rate_calculator):
       self.start_time = time.time()
       self.last_state_change = self.start_time
       self.accumulated_rate = 0
       self.in_motion = False
       self.movements = [(0, self.in_motion)]
       self.rate_calculator = rate_calculator

    # Cambia estado del taxi
   def toggle_motion(self):
       current_time = time.time()
       self.accumulated_rate += self.calculate_segment_rate()
       self.last_state_change = current_time
       self.in_motion = not self.in_motion
       self.movements.append((current_time - self.start_time, self.in_motion))

    # Calcula tarifa del segmento actual
   def calculate_segment_rate(self):
       current_time = time.time()
       segment_time = current_time - self.last_state_change
       return self.rate_calculator.calculate_rate(segment_time, self.in_motion)
    
    # Finaliza el viaje y retorna datos
   def finalize(self):
       current_time = time.time()
       self.accumulated_rate += self.calculate_segment_rate()
       trip_duration = current_time - self.start_time
       self.movements.append((trip_duration, self.in_motion))
       return {
           'duration': trip_duration,
           'total_rate': self.accumulated_rate,
           'movements': self.movements,
           'rate_info': self.rate_calculator.get_current_rate()
       }

    # Obtiene estado actual del viaje
   def get_current_status(self):
       current_time = time.time()
       return {
           'state': 'Movimiento' if self.in_motion else 'Parado',
           'time': current_time - self.start_time,
           'rate': self.accumulated_rate + self.calculate_segment_rate()
       }