import tkinter as tk
from tkinter import ttk  # Para widgets más modernos

class TaxiMeterGUI:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Pepe Taxi")
        
        # Configurar el tamaño de la ventana
        self.root.geometry("800x600")
        
        # Crear un label de bienvenida
        welcome_label = ttk.Label(
            self.root, 
            text="Bienvenido al Taxímetro Digital",
            font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()

# Si ejecutamos este archivo directamente
if __name__ == "__main__":
    app = TaxiMeterGUI()
    app.run()