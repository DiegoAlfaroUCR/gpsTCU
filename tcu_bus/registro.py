import tkinter as tk
import sqlite3
import subprocess

class RegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Operadores")
        self.geometry("800x480")  # Ajustar a las dimensiones de la pantalla táctil
        self.geometry("800x480")

        # Crear base de datos y tabla si no existe
        self.create_database()

        # Variables para los campos de entrada
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()  # Variable para el mensaje de registro
        self.message = tk.StringVar()

        # Crear widgets de la interfaz
        self.create_widgets()
        self.keyboard_frame = None  # Inicializar el teclado
        self.keyboard_frame = None

    def create_database(self):
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operadores (
                operator_id TEXT PRIMARY KEY,
@@ -42,7 +38,6 @@ def create_database(self):
        conn.close()

    def create_widgets(self):
        # Usar grid para colocar los campos en 3 columnas y 2 filas
        tk.Label(self, text="ID del Operador:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self, textvariable=self.operator_id).grid(row=0, column=1, padx=5, pady=5)

@@ -61,70 +56,27 @@ def create_widgets(self):
        tk.Label(self, text="Contraseña:").grid(row=2, column=2, padx=5, pady=5)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=2, column=3, padx=5, pady=5)

        tk.Button(self, text="Registrar", command=self.register).grid(row=3, column=0, columnspan=4, pady=10)

        self.create_keyboard()

        # Label para mostrar el mensaje de registro
        self.success_label = tk.Label(self, textvariable=self.message, fg="green")
        self.success_label.grid(row=4, column=0, columnspan=4)

    def create_keyboard(self):
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR']

        self.keyboard_frame = tk.Frame(self)
        self.keyboard_frame.grid(row=5, column=0, columnspan=4, pady=20)  # Posiciona el teclado debajo de los campos

        for key in keys:
            button = tk.Button(self.keyboard_frame, text=key, width=5, command=lambda k=key: self.key_press(k))
            row, col = divmod(keys.index(key), 10)
            button.grid(row=row, column=col)

    def key_press(self, key):
        focused_widget = self.focus_get()
        if key == "BORRAR" and focused_widget:
            current_text = focused_widget.get()
            focused_widget.delete(0, tk.END)
            focused_widget.insert(0, current_text[:-1])
        else:
            if focused_widget:
                focused_widget.insert(tk.END, key)

    def register(self):
        # Obtener los datos de los campos
        operator_id = self.operator_id.get()
        name = self.name.get()
        phone = self.phone.get()
        email = self.email.get()
        username = self.username.get()
        password = self.password.get()

        # Guardar en la base de datos
        tk.Button(self, text="Registrar", command=self.register_user).grid(row=3, column=0, columnspan=4, pady=10)

        tk.Label(self, textvariable=self.message, fg="green").grid(row=4, column=0, columnspan=4, pady=10)

    def register_user(self):
        conn = sqlite3.connect("operadores.db")
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO operadores (operator_id, name, phone, email, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (operator_id, name, phone, email, username, password))
            conn.commit()
            self.message.set("Registro exitoso.")  # Actualizar el mensaje
        except sqlite3.IntegrityError:
            self.message.set("Error: ID del operador ya existe.")  # Mensaje de error
        finally:
            conn.close()

        # Limpiar campos después del registro
        self.operator_id.set("")
        self.name.set("")
        self.phone.set("")
        self.email.set("")
        self.username.set("")
        self.password.set("")

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
