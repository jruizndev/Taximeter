import time

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
    """Calcular tarifa según estado"""
    return elapsed_time * (0.05 if in_motion else 0.02)

# Función para iniciar un nuevo trayecto
def start_trip():
    start_time = time.time() # Tiempo de inicio del trayecto
    last_state_change = start_time # Último cambio de estado
    accumulated_rate = 0 # Tarifa acumulada
    in_motion = False # Estado inicial: parado

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
            print(f"\nTrayecto finalizado")
            print(f"Tarifa total: {total_rate:.2f}€")
            break
        elif action == 'm':
            accumulated_rate += segment_rate # Actualiza la tarifa acumulada
            last_state_change = current_time # Actualiza el último cambio de estado
            in_motion = not in_motion # Cambia el estado del trayecto (movimiento/parado)

# Función principal del programa
def main():
    while True:
        welcome_message()
        option = input("\nSeleccione una opción (1-2): ")
        
        if option == "1":
            start_trip()
        elif option == "2":
            print("\n¡Gracias por usar el taxímetro!")
            break
        else:
            print("Opción no válida. Por favor, seleccione 1 o 2.")

if __name__ == "__main__":
    main()
