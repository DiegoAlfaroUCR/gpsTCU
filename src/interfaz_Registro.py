import tkinter as tk
import sqlite3
import re
import threading

# Fuente determinada del sistema
font = ("Helvetica", 12)
path = 'src/operadores.db'


class InterfazMain(tk.Tk):
    """Clase para la generación de la interfaz principal de
    registro.


    :param tk: Clase para interfaces con Tkinter
    :type tk: Objeto Tk
    """

    def __init__(self):
        """Función inicializadora de la interfaz principal.
        """
        super().__init__()

        # Inicia en fullscreen, para salir se usa Esc
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda event:
                  self.attributes("-fullscreen", False))

        self.title("REGISTRO DE USUARIO")

        # Ajustar a las dimensiones de la pantalla táctil
        self.geometry("800x480")

        self.configure(bg="lightblue")  # Fondo de color azul claro

        # Variables para los campos de entrada
        self.operator_id = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()  # Variable para el mensaje de registro

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_database()
        self.create_widgets()

    def create_database(self):
        """Se crea el objeto database en caso de no existir.
        """
        conn = sqlite3.connect(path)
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
        """Crea los objetos de la interfaz de registro.
        """
        # Hace que las columnas se expandan
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Usar grid para colocar los campos en 3 columnas y 2 filas
        tk.Label(self, text="ID del Operador:", bg="yellow",
                 font=font).grid(row=0, column=0, padx=5, pady=7)
        tk.Entry(self, textvariable=self.operator_id, font=font).grid(
            row=0, column=1, padx=5, pady=7)

        tk.Label(self, text="Nombre y Apellido:",  bg="yellow",
                 font=font).grid(row=0, column=2, padx=5, pady=7)
        tk.Entry(self, textvariable=self.name, font=font).grid(
            row=0, column=3, padx=5, pady=7)

        tk.Label(self, text="Teléfono:", bg="yellow",
                 font=font).grid(row=1, column=0, padx=5, pady=7)
        tk.Entry(self, textvariable=self.phone, font=font).grid(
            row=1, column=1, padx=5, pady=7)

        tk.Label(self, text="Email:", bg="yellow",
                 font=font).grid(row=1, column=2, padx=5, pady=7)
        tk.Entry(self, textvariable=self.email, font=font).grid(
            row=1, column=3, padx=5, pady=7)

        tk.Label(self, text="Nombre de usuario:",  bg="yellow",
                 font=font).grid(row=2, column=0, padx=5, pady=7)
        tk.Entry(self, textvariable=self.username, font=font).grid(
            row=2, column=1, padx=5, pady=7)

        tk.Label(self, text="Contraseña:",  bg="yellow",
                 font=font).grid(row=2, column=2, padx=5, pady=7)
        tk.Entry(self, textvariable=self.password, font=font,
                 show="*").grid(row=2, column=3, padx=5, pady=7)

        tk.Button(self, text="Registrar", bg="lightgreen",
                  fg="black", command=self.register,
                  font=font).grid(row=3, column=0, columnspan=4, pady=10)

        self.create_keyboard()

        # Label para mostrar el mensaje de registro
        self.success_label = tk.Label(
            self, textvariable=self.message, fg="green")
        self.success_label.grid(row=4, column=0, columnspan=4)

    def create_keyboard(self):
        """Crear el teclado táctil en la pantalla de registro.
        """
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '@', '.', '_',
            'ESPACIO', 'BORRAR'
        ]

        total_columns = 10

        # Posiciona el teclado debajo de los campos
        # Añadir color de fondo al marco
        self.keyboard_frame = tk.Frame(self, bg="lightblue")
        self.keyboard_frame.grid(row=5, column=0, columnspan=4, pady=20)

        # Se dimensiona de forma distinta la tecla según
        # si es caracter, espacio o tecla de borrado.
        for key in keys:
            # Colores predeterminados
            if key == 'ESPACIO':
                bg_color = "lightgray"
                fg_color = "black"
            elif key == 'BORRAR':
                bg_color = "red"
                fg_color = "white"
            else:
                bg_color = "black"
                fg_color = "white"

            # Crear el botón con los colores aplicados
            button = tk.Button(
                self.keyboard_frame,
                text=key,
                width=5,
                font=font,
                bg=bg_color,  # Color de fondo
                fg=fg_color,  # Color del texto
                command=lambda k=key: self.key_press(k)
            )

            row, col = divmod(keys.index(key), 10)

            if key == 'BORRAR':
                button.grid(row=row, column=8, columnspan=2, sticky="we")
                button.config(width=10)
            elif key == "ESPACIO":
                space_row = len(keys) // total_columns
                button.grid(row=space_row, column=0, columnspan=8, sticky="we")
            else:
                button.grid(row=row, column=col)

        def key_press(self, key):
            """Simula el efecto de presionar la tecla seleccionada.

            :param key: Tecla presionada en teclado táctil.
            :type key: tk.button
            """
            focused_widget = self.focus_get()
            if isinstance(focused_widget, tk.Entry):
                if key == "BORRAR":
                    current_text = focused_widget.get()
                    focused_widget.delete(0, tk.END)
                    focused_widget.insert(0, current_text[:-1])
                elif key == "ESPACIO":
                    focused_widget.insert(tk.END, " ")
                else:
                    focused_widget.insert(tk.END, key)

    def verificarRegistro(self, operator_id, name,
                          phone, email, username, password):
        """Se verifica la validez de los datos de registro.

        :param operator_id: ID de operador ingresada.
        :type operator_id: tk.StringVar
        :param name: Nombre completo ingresado.
        :type name: tk.StringVar
        :param phone: Número de teléfono ingresado.
        :type phone: tk.StringVar
        :param email: Email ingresado
        :type email: tk.StringVar
        :param username: Nombre de usuario ingresado
        :type username: tk.StringVar
        :param password: Contraseña ingresada.
        :type password: tk.StringVar
        :raises ValueError: Si los datos ingresados no cumplen con
                            los requisitos dados.
        """
        if not re.match("^[0-9]{1,9}$", operator_id):
            raise ValueError("ID inválido, debe ser numérico.")

        if not re.match("^[0-9]{8}$", phone):
            raise ValueError(
                "Número de teléfono inválido, deben ser 8 números."
                )

        email_pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not re.match(email_pattern, email):
            raise ValueError("Correo electrónico inválido.")

        if not re.match("^[a-zA-Z0-9]{1,10}$", username):
            raise ValueError(
                "Username inválido debe ser menos de 10 letras o números."
                )

        if not re.match("^[a-zA-Z\\s]{1,20}$", name):
            raise ValueError("Nombre inválido debe ser letras"
                             "o espacios y menos de 20 caracteres.")

        if not re.match("^[a-zA-Z0-9]{4,20}$", password):
            raise ValueError("Contraseña incorrecta, debe contener solo"
                             "letras y números y tener al menos 4 de estos.")

    def register(self):
        """Se realiza registro de datos ingresados, si estos son válidos.
        """
        operator_id = self.operator_id.get()
        name = self.name.get()
        phone = self.phone.get()
        email = self.email.get()
        username = self.username.get()
        password = self.password.get()

        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        try:
            self.verificarRegistro(operator_id, name, phone,
                                   email, username, password)
            cursor.execute('''
                INSERT INTO operadores (operator_id, name, phone, email,
                username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (operator_id, name, phone, email, username, password))
            conn.commit()
            self.message.set("Registro exitoso.")

            # Limpiar campos después del registro
            self.operator_id.set("")
            self.name.set("")
            self.phone.set("")
            self.email.set("")
            self.username.set("")
            self.password.set("")

        except sqlite3.IntegrityError:
            self.message.set("Error: ID del operador ya existe.")
        except ValueError as e:
            self.message.set(str(e))
        finally:
            conn.close()

    def on_closing(self):
        """Finaliza el programa correctamente.
        """
        self.destroy()


if __name__ == "__main__":
    app = InterfazMain()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
