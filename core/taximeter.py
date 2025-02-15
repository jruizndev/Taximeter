import logging
from core.trip import Trip
from core.calculator import RateCalculator

# Clase principal del taxímetro
class Taximeter:
   def __init__(self):
       self.active_conditions = []
       self.current_trip = None
       self.rate_calculator = RateCalculator()
       self.initialize_logging()
       
    # Configuración del sistema de logs
   def initialize_logging(self):
       logging.basicConfig(
           filename='logs/taximeter.log',
           level=logging.INFO,
           format='%(asctime)s - %(levelname)s - %(message)s',
           datefmt='%d/%m/%Y %H:%M:%S'
       )

    # Inicio de un nuevo viaje
   def start_new_trip(self):
       self.current_trip = Trip(self.rate_calculator)
       logging.info("Nuevo trayecto iniciado")
       return self.current_trip

    # Cambia estado de movimiento
   def toggle_motion(self):
       if self.current_trip:
           self.current_trip.toggle_motion()

    # Finaliza el viaje actual
   def end_trip(self):
       if self.current_trip:
           trip_data = self.current_trip.finalize()
           self.current_trip = None
           return trip_data