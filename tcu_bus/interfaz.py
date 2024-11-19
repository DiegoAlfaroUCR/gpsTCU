import tkinter as tk
import threading
import subprocess
from funcionesGPS import manejarGPS
import sqlite3

class VirtualKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INICIO DE SESION")
        self.geometry("800x480")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, fill='both')

        tk.Label(self.login_frame, text="USUARIO:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.username).pack(pady=10)

        tk.Label(self.login_frame, text="CONTRASEÑA:").pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.password, show="*").pack(pady=10)

        self.keyboard_frame = tk.Frame(self.login_frame)
        self.keyboard_frame.pack(pady=10)

        self.create_keyboard()

        tk.Button(self.login_frame, text="INICIAR", command=self.send_data).pack(pady=5)
        tk.Button(self.login_frame, text="REGISTRARSE", command=self.show_registration).pack(pady=5)

        self.trip_frame = tk.Frame(self)

        tk.Button(self.trip_frame, text="Iniciar Viaje",
                  command=self.start_gps, width=20, height=3).pack(pady=20)
        tk.Button(self.trip_frame, text="Finalizar Viaje",
                  command=self.stop_gps, width=20, height=3).pack(pady=20)

        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message, fg="green").pack(pady=10)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR'
        ]

        keyboard_frame = tk.Frame(self.keyboard_frame)
        keyboard_frame.pack(pady=20)

        for index, key in enumerate(keys):
            button = tk.Button(
                keyboard_frame, text=key, width=6,
                command=lambda k=key: self.key_press(k)
            )
            row, col = divmod(index, 10)
            button.grid(row=row, column=col, padx=2, pady=2)

    def key_press(self, key):
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            else:
                focused_widget.insert(tk.END, key)

    def send_data(self):
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operadores WHERE username=? AND password=?", 
                       (self.username.get(), self.password.get()))
        user = cursor.fetchone()
        conn.close()

        if user:
            print(f"Usuario: {self.username.get()}")
            print(f"Contraseña: {self.password.get()}")

            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')
            self.keyboard_frame.pack_forget()
        else:
            tk.messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos")

    def show_registration(self):
        # Ejecuta registro.py cuando el botón de registro es presionado
        subprocess.Popen(
            ["C:/Users/perry/AppData/Local/Programs/Python/Python312/python.exe", 
             "c:/Users/perry/OneDrive/Escritorio/busTCU/gpsTCU/tcu_bus/registro.py"] # modificar esta direccion con la de la raspe
        )
        self.destroy()  # Cierra la ventana de interfaz.py

    def start_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            print("La lectura de GPS ya está en progreso.")
            return

        self.stop_event.clear()

        self.gps_thread = threading.Thread(
            target=manejarGPS,
            args=(self.stop_event,),
            daemon=True
        )
        self.gps_thread.start()
        self.status_message.set("Lectura de GPS iniciada.")
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_event.set()
            self.gps_thread.join()
            self.status_message.set("Lectura de GPS finalizada.")
            print("Lectura de GPS finalizada.")
        else:
            print("La lectura de GPS no está en ejecución.")

    def on_closing(self):
        self.stop_gps()
        self.destroy()

if __name__ == "__main__":
    app = VirtualKeyboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
