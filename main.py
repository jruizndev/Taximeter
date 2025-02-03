def welcome_message():
    print("=== TAXÍMETRO DIGITAL ===")
    print("\nBienvenido al sistema de taxímetro digital.")
    print("Este programa permite calcular tarifas de viajes en taxi.\n")
    print("Opciones disponibles:")
    print("1. Iniciar nuevo trayecto")
    print("2. Salir")

def main():
    welcome_message()
    while True:
        option = input("\nSeleccione una opción (1-2): ")
        if option == "1":
            print("Iniciando trayecto...")
        elif option == "2":
            print("\n¡Gracias por usar el taxímetro!")
            break
        else:
            print("Opción no válida. Por favor, seleccione 1 o 2.")

if __name__ == "__main__":
    main()