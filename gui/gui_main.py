import tkinter as tk
from tkinter import ttk
from gui.frames.auth_frame import AuthFrame
from gui.frames.meter_display import MeterDisplay

class TaxiMeterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pepe Taxi")
        self.root.geometry("800x600")
        
        self.auth_frame = AuthFrame(self.root, self.show_main_window)
        self.auth_frame.pack(expand=True, fill="both")

    def show_main_window(self, user):
        self.current_user = user
        self.auth_frame.pack_forget()
        
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(expand=True, fill="both")

        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))

        user_label = ttk.Label(
            header_frame,
            text=f"Usuario: {user['username']} | Rol: {user['role']}",
            style='TLabel'
        )
        user_label.pack(side="left")

        logout_button = ttk.Button(
            header_frame,  
            text="Cerrar Sesión",
            command=self.handle_logout
        )
        logout_button.pack(side="right")

        self.meter_display = MeterDisplay(self.main_frame)
        self.meter_display.pack(expand=True, fill="both")

    def handle_logout(self):
        self.main_frame.destroy()
        self.auth_frame.reset_fields()  
        self.auth_frame.pack(expand=True, fill="both")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TaxiMeterGUI()
    app.run()