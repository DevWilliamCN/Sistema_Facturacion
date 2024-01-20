# Importar las bibliotecas necesarias
from tkinter import Tk, Label, Button, Entry, StringVar
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import webbrowser
import os
from BaseDeDatos import connect_to_database, save_to_database, fetch_from_database  # Importar funciones de manejo de la base de datos

# Definir la clase del sistema de facturación
class FacturationSystem:
    # Constructor de la clase
    def __init__(self, root, db_connection):
        # Inicializar atributos
        self.root = root
        self.db_connection = db_connection
        self.root.title("Sistema_Facturacion")

        self.product_data = {}  # Diccionario para almacenar datos de productos

        # Interfaz gráfica
        self.label = Label(root, text="¡Manejo de productos!")
        self.label.grid(row=0, column=0, columnspan=2)

        self.product_label = Label(root, text="Producto:")
        self.product_label.grid(row=1, column=0)
        self.product_entry = Entry(root)
        self.product_entry.grid(row=1, column=1)

        self.price_label = Label(root, text="Precio:")
        self.price_label.grid(row=2, column=0)
        self.price_entry = Entry(root)
        self.price_entry.grid(row=2, column=1)

        self.add_button = Button(root, text="Añadir Producto", command=self.add_product)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.save_button = Button(root, text="Guardar en Base de datos", command=self.save_to_database)
        self.save_button.grid(row=4, column=0, columnspan=2)

        self.invoice_button = Button(root, text="Facturar", command=self.generate_invoice)
        self.invoice_button.grid(row=5, column=0, columnspan=2)

        self.generate_pdf_button = Button(root, text="Generar PDF", command=self.generate_pdf)
        self.generate_pdf_button.grid(row=6, column=0, columnspan=2)

    # Método para añadir producto
    def add_product(self):
        product = self.product_entry.get()
        price = self.price_entry.get()
        if product and price:
            try:
                price = float(price)
                self.product_data[product] = price
                print(f"Producto {product} añadido con precio {price}.")
            except ValueError:
                print("Por favor, ingrese un precio válido.")
        else:
            print("Por favor, complete los campos de producto y precio.")

    # Método para guardar en la base de datos
    def save_to_database(self):
        save_to_database(self.db_connection, self.product_data)

    # Método para generar factura (placeholder)
    def generate_invoice(self):
        print("Generando factura de los productos")

    # Método para generar PDF
    def generate_pdf(self):
        print("Generando PDF de los productos")
        data = [["ID", "Producto", "Precio"]]

        records = fetch_from_database(self.db_connection)
        for row in records:
            data.append([row[0], row[1], row[2]])

        pdf_filename = "Productos.pdf"
        pdf = SimpleDocTemplate(
            pdf_filename,
            pagesize=letter
        )

        table = Table(data)
        table.setStyle(TableStyle([
            # (aquí van todas las configuraciones de estilo de la tabla)
            # ...
        ]))

        elems = []
        elems.append(table)
        pdf.build(elems)

        webbrowser.open_new(os.path.abspath(pdf_filename))

# Conectar a la base de datos
db_connection = connect_to_database()

# Comprobar si la conexión fue exitosa
if db_connection is not None:
    root = Tk()
    app = FacturationSystem(root, db_connection)
    root.mainloop()
else:
    print("No se pudo conectar a la base de datos. El programa se cerrará.")
