from tkinter import Tk, Label, Button, Entry, Frame, messagebox
from PIL import Image, ImageTk
from BaseDeDatos import check_login, connect_to_database

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio_de_sesión")

        width = 500  # Ancho de la ventana
        height = 500  # Alto de la ventana

        # Centrar la ventana en la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2 + 20  # Ajusta la posición vertical

        # Definir las dimensiones y posición inicial de la ventana
        root.geometry(f"{width}x{height}+{x_position}+{y_position}")

        frame = Frame(root)  # Crear un frame para agrupar los elementos
        frame.pack(pady=20)  # Añade un margen en la parte superior

        try:
            img = Image.open("icono.png")  # Cargar la imagen
            img = img.resize((300, 300), Image.LANCZOS)  # Redimensionar la imagen
            self.user_icon = ImageTk.PhotoImage(img)

        except Exception as e:
            print("No se pudo cargar la imagen de usuario.")
            print("Error:", e)

        self.root.configure(bg="#f2f2f2")  # Color de fondo

        # Colocar el icono arriba del título "Login"
        self.icon_label = Label(frame, image=self.user_icon)
        self.icon_label.grid(row=0, column=1, columnspan=2, pady=(0, 10))  # Añadir un espaciado en la parte inferior

        self.label = Label(frame, text="Login", font=("Helvetica", 16, "bold"), bg="#f2f2f2")
        self.label.grid(row=1, column=1, columnspan=2, pady=0, sticky="n")  # Ajustar el pady a 0 y usar sticky="n"

        self.username_label = Label(frame, text="Usuario:", font=("Helvetica", 12, "bold"), bg="#f2f2f2")
        self.username_label.grid(row=2, column=1, sticky="e", padx=(10, 0))  # Agregar un espaciado a la derecha

        self.username_entry = Entry(frame, font=("Helvetica", 12))
        self.username_entry.grid(row=2, column=2, sticky="w", padx=(0, 10))  # Agregar un espaciado a la izquierda

        self.password_label = Label(frame, text="Contraseña:", font=("Helvetica", 12, "bold"), bg="#f2f2f2")
        self.password_label.grid(row=3, column=1, sticky="e", padx=(10, 0))  # Agregar un espaciado a la derecha

        self.password_entry = Entry(frame, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=3, column=2, sticky="w", padx=(0, 10))  # Agregar un espaciado a la izquierda

        self.login_button = Button(frame, text="Iniciar sesión", command=self.verify_login, bg="#00264D", fg="white",
                                   font=("Helvetica", 12))
        self.login_button.grid(row=4, column=2, pady=(10, 20),
                               sticky="n")  # Ajustar el pady del botón y usar sticky="n"

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:  # Verifica que los campos no estén vacíos
            if check_login(username, password):
                self.show_info("Inicio de sesión exitoso")
                self.root.destroy()  # Cierra la ventana de inicio de sesión

                # Abre la ventana de la InterfazGrafica
                db_connection = connect_to_database()
                if db_connection is not None:
                    new_root = Tk()
                    from InterfazGrafica import FacturationSystem
                    app = FacturationSystem(new_root, db_connection)
                    new_root.mainloop()
            else:
                self.show_error("Usuario o Contraseña son incorrectos")
        else:
            self.show_error("Por favor, complete todos los campos.")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_info(self, message):
        messagebox.showinfo("Información", message)


if __name__ == "__main__":
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()
