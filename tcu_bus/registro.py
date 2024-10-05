import tkinter as tk
import sqlite3
import subprocess

class RegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Operadores")
        self.geometry("800x480")

        self.create_database()

        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()

        self.create_widgets()
        self.keyboard_frame = None

    def create_database(self):
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operadores (
                operator_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        tk.Label(self, text="ID del Operador:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self, textvariable=self.operator_id).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(self, textvariable=self.name).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self, textvariable=self.phone).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Email:").grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(self, textvariable=self.email).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self, text="Usuario:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self, textvariable=self.username).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Contraseña:").grid(row=2, column=2, padx=5, pady=5)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=2, column=3, padx=5, pady=5)

        tk.Button(self, text="Registrar", command=self.register_user).grid(row=3, column=0, columnspan=4, pady=10)

        tk.Label(self, textvariable=self.message, fg="green").grid(row=4, column=0, columnspan=4, pady=10)

    def register_user(self):
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO operadores (operator_id, name, phone, email, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.operator_id.get(), self.name.get(), self.phone.get(), self.email.get(), self.username.get(), self.password.get()))

        conn.commit()
        conn.close()

        self.message.set("Registro exitoso.")
        print(f"Registrado: {self.username.get()}")
        subprocess.Popen(
            ["C:/Users/perry/AppData/Local/Programs/Python/Python312/python.exe", 
             "c:/Users/perry/OneDrive/Escritorio/busTCU/gpsTCU/tcu_bus/interfaz.py"] # modificar esta direccion con la de la raspe
        )
        self.destroy()  # Cierra la ventana de interfaz.py

if __name__ == "__main__":
    app = RegistrationApp()
    app.mainloop()
