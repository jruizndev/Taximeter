import time
import logging
from datetime import datetime

# Configuración del sistema de logs
logging.basicConfig(
   filename='logs/taximeter.log',
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s',
   datefmt='%d/%m/%Y %H:%M:%S'
)

# Función que muestra el menú inicial
def welcome_message():
   print("=== TAXÍMETRO DIGITAL ===")
   print("\nBienvenido al sistema de taxímetro digital.")
   print("Este programa permite calcular tarifas de viajes en taxi.\n")
   print("Opciones disponibles:")
   print("1. Iniciar nuevo trayecto")
   print("2. Salir")

# Función para calcular tarifa según el estado del trayecto
def calculate_rate(elapsed_time, in_motion):
   return elapsed_time * (0.05 if in_motion else 0.02)

# Función para guardar el historial de viajes en un archivo txt
def save_trip_history(duration, total_rate, movements):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    with open('history/trips.txt', 'a') as file:
        file.write(f"VIAJE {timestamp}\n")
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

# Función para iniciar un nuevo trayecto
def start_trip():
    start_time = time.time() # Tiempo de inicio del trayecto
    last_state_change = start_time # Último cambio de estado
    accumulated_rate = 0 # Tarifa acumulada
    in_motion = False # Estado inicial: parado
    movements = [(0, in_motion)] # Lista para guardar cambios de estado

    logging.info("Nuevo trayecto iniciado")

    # Instrucciones para el taxista
    print("\n¡Trayecto iniciado!")
    print("Controles:")
    print("'m' - cambiar movimiento/parado") 
    print("'f' - finalizar trayecto")

    # Bucle principal del viaje
    while True:
        current_time = time.time() # Tiempo actual
        segment_time = current_time - last_state_change # Cuánto tiempo ha pasado desde el último cambio
        segment_rate = calculate_rate(segment_time, in_motion) # Calcula la tarifa del tramo
        total_rate = accumulated_rate + segment_rate # Tarifa total acumulada
        
        # Mostrar estado actual
        print(f"\rEstado: {'Movimiento' if in_motion else 'Parado'} | "
              f"Tiempo: {current_time - start_time:.1f}s | "
              f"Tarifa: {total_rate:.2f}€", end="", flush=True)
        
        action = input("\nAcción ('m' para cambiar estado, 'f' para finalizar): ").lower()
        
        if action == 'f':
            trip_duration = current_time - start_time
            logging.info(f"Trayecto finalizado - Duración: {trip_duration:.1f}s - Tarifa: {total_rate:.2f}€")
            save_trip_history(trip_duration, total_rate, movements)
            print(f"\nTrayecto finalizado")
            print(f"Tarifa total: {total_rate:.2f}€")
            break
        elif action == 'm':
            accumulated_rate += segment_rate # Actualiza la tarifa acumulada
            last_state_change = current_time # Actualiza el último cambio de estado
            in_motion = not in_motion # Cambia el estado del trayecto (movimiento/parado)
            movements.append((current_time - start_time, in_motion))
            logging.info(f"Estado cambiado a {'movimiento' if in_motion else 'parado'}")

# Función principal del programa
def main():
    while True:
        welcome_message()
        option = input("\nSeleccione una opción (1-2): ")
        
        if option == "1":
            start_trip()
        elif option == "2":
            logging.info("Programa finalizado")
            print("\n¡Gracias por usar el taxímetro!")
            break
        else:
            logging.warning(f"Opción inválida seleccionada: {option}")
            print("Opción no válida. Por favor, seleccione 1 o 2.")

if __name__ == "__main__":
    main()