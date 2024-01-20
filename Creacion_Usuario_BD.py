from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel
from PIL import Image, ImageTk
from BaseDeDatos import connect_to_database, create_user, check_login

class AdminUserCreation:
    def __init__(self, root):
        self.root = root
        root.title("Creacion_de_Usuarios")

        width = 400   # Ancho de la ventana
        height = 470  # Alto de la ventana

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2

        root.geometry(f"{width}x{height}+{x_position}+{y_position}")

        frame = Frame(root)
        frame.pack()

        try:
            img = Image.open("icono.png")
            self.user_icon = ImageTk.PhotoImage(img)
            self.icon_label = Label(frame, image=self.user_icon)
            self.icon_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        except:
            print("No se pudo cargar la imagen de usuario.")

        self.welcome_label = Label(frame, text="Bienvenido Administrador", font=("Helvetica", 14, "bold"))
        self.welcome_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.instructions_label = Label(frame, text="Registre al usuario", width=30, font=("Helvetica", 12, "bold"))
        self.instructions_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.username_label = Label(frame, text="Crear Nombre del usuario:", width=20, font=("Helvetica", 10, "bold"))
        self.username_label.grid(row=3, column=0, sticky="e", padx=5, pady=(5, 0))

        self.username_entry = Entry(frame, width=20)
        self.username_entry.grid(row=3, column=1, padx=5, pady=(5, 0))

        self.password_label = Label(frame, text="Crear Contraseña del usuario:", width=25, font=("Helvetica", 10, "bold"))
        self.password_label.grid(row=4, column=0, sticky="e", padx=5, pady=(5, 0))

        self.password_entry = Entry(frame, width=20)
        self.password_entry.grid(row=4, column=1, padx=5, pady=(5, 0))

        self.save_button = Button(frame, text="Registrar Usuario", command=self.save_user, bg="#00264D", fg="white")
        self.save_button.grid(row=5, column=1, columnspan=2, pady=10)

        self.recover_password_button = Button(frame, text="Recuperar Contraseña", command=self.recover_password, bg="#FF5733", fg="white")
        self.recover_password_button.grid(row=6, column=1, columnspan=2, pady=10)

    def save_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            connection = connect_to_database()
            if connection is not None:
                if not self.check_existing_username(connection, username):
                    create_user(connection, username, password)
                    messagebox.showinfo("Registro Exitoso", f"Usuario {username} creado en la base de datos exitosamente.")
                    self.username_entry.delete(0, 'end')
                    self.password_entry.delete(0, 'end')
                else:
                    messagebox.showerror("Error de Registro", "El nombre de usuario ya existe en la base de datos.")
            else:
                messagebox.showerror("Error de Conexión", "Error de conexión a la base de datos.")
        else:
            messagebox.showerror("Campos Incompletos", "Por favor, complete todos los campos.")

    def recover_password(self):
        self.recover_window = Toplevel(self.root)
        self.recover_window.title("Recuperar Contraseña")
        self.recover_window.grab_set()  # Bloquear interacción con otras ventanas

        recover_label = Label(self.recover_window, text="Ingrese su nombre de usuario:", font=("Helvetica", 12, "bold"))
        recover_label.pack(pady=10)

        self.username_entry = Entry(self.recover_window, font=("Helvetica", 12))
        self.username_entry.pack(pady=10)

        recover_button = Button(self.recover_window, text="Recuperar", command=self.execute_recovery)
        recover_button.pack()

    def execute_recovery(self):
        username = self.username_entry.get()
        connection = connect_to_database()
        if connection is not None:
            if self.check_existing_username(connection, username):
                success, stored_hash = check_login(username, "dummy")  # "dummy" es una contraseña ficticia
                if success:
                    messagebox.showinfo("Contraseña Recuperada", f"La contraseña cifrada del usuario {username} es: {stored_hash}")
                    password = stored_hash
                else:
                    messagebox.showerror("Error", "No se encontró la contraseña del usuario.")
            else:
                messagebox.showerror("Usuario no encontrado", "El usuario no existe en la base de datos.")
        else:
            messagebox.showerror("Error de Conexión", "Error de conexión a la base de datos.")
        self.recover_window.destroy()  # Cerrar la ventana de recuperación

    def check_existing_username(self, connection, username):
        try:
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result and result[0] > 0:
                return True
            else:
                return False
        except Exception as e:
            print("Error al verificar el nombre de usuario:", e)
            return False

if __name__ == "__main__":
    root = Tk()
    app = AdminUserCreation(root)
    root.mainloop()
