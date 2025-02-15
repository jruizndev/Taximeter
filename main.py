import logging
from core.taximeter import Taximeter
from core.ui import TaxiUI

def main():
    logging.info("Programa iniciado")
    taximeter = Taximeter()
    ui = TaxiUI(taximeter)

    # Mostrar menú de autenticación hasta que el usuario inicie sesión
    while not ui.current_user:
        ui.show_auth_menu()
        
    # Una vez autenticado, mostrar el menú principal
    while True:
        ui.show_welcome_message()
        option = input("\nSeleccione una opción (1-4): ")
        
        if option == "1":
            ui.handle_trip()
        elif option == "2":
            ui.show_current_rates()
        elif option == "3":
            ui.manage_special_conditions()
        elif option == "4":
            logging.info("Programa finalizado")
            print("\n¡Gracias por usar el taxímetro!")
            ui.auth.db.disconnect()  
            break
        else:
            logging.warning(f"Opción inválida seleccionada: {option}")
            print("Opción no válida. Por favor, seleccione 1-4")

if __name__ == "__main__":
   main()