import time
import logging
from datetime import datetime
from config import TIME_SLOTS, SPECIAL_CONDITIONS

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


# Variable global para condiciones especiales
active_conditions = []

# Configuración del sistema de logs
logging.basicConfig(
  filename='logs/taximeter.log',
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  datefmt='%d/%m/%Y %H:%M:%S'
)

def get_current_rate():
   current_time = datetime.now().time()
   current_str = current_time.strftime('%H:%M')

   for slot_name, slot_info in TIME_SLOTS.items():
       if slot_name == 'normal':
           continue
       
       start = slot_info['start']
       end = slot_info['end']
       
       if start <= current_str <= end:
           return slot_info
   
   return TIME_SLOTS['normal']

def welcome_message():
   print("=== TAXÍMETRO DIGITAL ===")
   print("\nBienvenido al sistema de taxímetro digital.")
   print("Este programa permite calcular tarifas de viajes en taxi.\n")
   print("Opciones disponibles:")
   print("1. Iniciar nuevo trayecto")
   print("2. Ver tarifas actuales")
   print("3. Gestionar condiciones especiales")
   print("4. Salir")

def show_trip_summary(duration, total_rate, movements, current_rates):
   print("\n=== RESUMEN DEL VIAJE ===")
   print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
   print(f"Duración: {duration:.1f}s")
   print(f"Tarifa aplicada: {current_rates['description']}")
   if active_conditions:
       print(f"Condición especial: {active_conditions[0].capitalize()}")
   print(f"\nDesglose de estados:")
   for i in range(len(movements)):
       start_time = movements[i][0]
       state = "Movimiento" if movements[i][1] else "Parado"
       if i < len(movements) - 1:
           end_time = movements[i+1][0]
       else:
           end_time = movements[-1][0]
       print(f"- {start_time:.1f}s a {end_time:.1f}s: {state}")
   print(f"\nTarifa total: {total_rate:.2f}€")

def manage_special_conditions():
   global active_conditions
   print("\n=== CONDICIONES ESPECIALES ===")
   print("Condiciones activas:", active_conditions if active_conditions else "Ninguna")
   print("\nSeleccione condición:")
   print("1. Lluvia (+20%)")
   print("2. Eventos (+30%)")
   print("3. Desactivar todas")
   print("4. Volver")

   option = input("\nOpción: ")
   if option == "1":
       active_conditions = ["rain"]
       print("Activada tarifa por lluvia")
   elif option == "2":
       active_conditions = ["events"]
       print("Activada tarifa por eventos")
   elif option == "3":
       active_conditions = []
       print("Condiciones especiales desactivadas")
   elif option == "4":
       return

def calculate_rate(elapsed_time, in_motion, special_condition=None):
    current_rates = get_current_rate()
    base_rate = current_rates['motion_rate'] if in_motion else current_rates['stopped_rate']
    
    # Aplicar multiplicador si hay condición especial
    if special_condition and special_condition in SPECIAL_CONDITIONS:
        base_rate *= SPECIAL_CONDITIONS[special_condition]
    
    return elapsed_time * base_rate

def show_current_rates():
   current_rates = get_current_rate()
   print("\n=== TARIFAS DEL TAXÍMETRO ===")
   print("\nTARIFA ACTUAL:")
   print(f"► {current_rates['description']}")
   print(f"  - En movimiento: {current_rates['motion_rate']}€/s")
   print(f"  - Parado: {current_rates['stopped_rate']}€/s")

   if active_conditions:
       condition = active_conditions[0]
       multiplier = SPECIAL_CONDITIONS[condition]
       print(f"\nCondición especial activa: {condition.capitalize()} (+{(multiplier-1)*100}%)")
   
   input("\nPresione Enter para continuar...")

def save_trip_history(duration, total_rate, movements):
   timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   current_rates = get_current_rate()
   
   with open('history/trips.txt', 'a') as file:
       file.write(f"VIAJE {timestamp}\n")
       file.write(f"Tarifa aplicada: {current_rates['description']}\n")
       if active_conditions:
           file.write(f"Condición especial: {active_conditions[0].capitalize()}\n")
       file.write(f"Duración: {duration:.1f}s\n")
       file.write("Estados:\n")
       
       for i in range(len(movements)):
           start_time = movements[i][0]
           state = "Movimiento" if movements[i][1] else "Parado"
           
           if i < len(movements) - 1:
               end_time = movements[i+1][0]
           else:
               end_time = duration
               
           file.write(f"- {start_time:.1f}s a {end_time:.1f}s: {state}\n")
           
       file.write(f"Tarifa total: {total_rate:.2f}€\n")
       file.write("-----------------------------------------\n")

def start_trip(taximeter):
    taximeter.start_new_trip()
    current_trip = taximeter.current_trip
    
    current_rates = current_trip.rate_calculator.get_current_rate()
    condition_info = f" - {taximeter.active_conditions[0].capitalize()}" if taximeter.active_conditions else ""
    logging.info(f"Nuevo trayecto iniciado - Tarifa: {current_rates['description']}{condition_info}")

    print("\n¡Trayecto iniciado!")
    print(f"Tarifa actual: {current_rates['description']}{condition_info}")
    print("Controles:")
    print("'m' - cambiar movimiento/parado") 
    print("'f' - finalizar trayecto")

    while True:
        current_status = current_trip.get_current_status()
        
        print(f"\rEstado: {'Movimiento' if current_status['state'] == 'Movimiento' else 'Parado'} | "
                f"Tiempo: {current_status['time']:.1f}s | "
                f"Tarifa: {current_status['rate']:.2f}€", end="", flush=True)
        
        action = input("\nAcción ('m' para cambiar estado, 'f' para finalizar): ").lower()
        
        if action == 'f':
            trip_data = taximeter.end_trip()
            logging.info(f"Trayecto finalizado - Duración: {trip_data['duration']:.1f}s - Tarifa: {trip_data['total_rate']:.2f}€")
            save_trip_history(trip_data['duration'], trip_data['total_rate'], trip_data['movements'])
            show_trip_summary(trip_data['duration'], trip_data['total_rate'], trip_data['movements'], trip_data['rate_info'])
            
            while True:
                print("\nOpciones:")
                print("1. Iniciar nuevo trayecto")
                print("2. Volver al menú principal")
                
                option = input("\nSeleccione una opción: ")
                if option == "1":
                    return start_trip(taximeter)
                elif option == "2":
                    return
                else:
                    print("Opción no válida. Por favor, seleccione 1 o 2")
            
        elif action == 'm':
            taximeter.toggle_motion()
            logging.info(f"Estado cambiado a {'movimiento' if current_trip.in_motion else 'parado'}")

def main():
   logging.info("Programa iniciado")
   taximeter = Taximeter() 
   while True:
       welcome_message()
       option = input("\nSeleccione una opción (1-4): ")
       
       if option == "1":
           start_trip(taximeter)
       elif option == "2":
           show_current_rates()
       elif option == "3":
           manage_special_conditions()
       elif option == "4":
           logging.info("Programa finalizado")
           print("\n¡Gracias por usar el taxímetro!")
           break
       else:
           logging.warning(f"Opción inválida seleccionada: {option}")
           print("Opción no válida. Por favor, seleccione 1-4")

if __name__ == "__main__":
   main()