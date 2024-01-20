from tkinter import Tk, Label, Button, Entry, StringVar
import mysql.connector
import bcrypt

# Conexión a la base de datos
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="tu_base_de_datos"
        )
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para crear un nuevo usuario
def create_user(connection, username, password):
    cursor = connection.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_password_str = hashed_password.decode('utf-8')
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_password_str))
    connection.commit()

# Guardar datos en la base de datos
def save_to_database(connection, product_data):
    cursor = connection.cursor()
    for product, price in product_data.items():
        query = "INSERT INTO your_table_name (product_column, price_column) VALUES (%s, %s)"
        cursor.execute(query, (product, price))
    connection.commit()

# Verificar las credenciales del usuario
def check_login(username, password):
    connection = connect_to_database()
    if connection is not None:
        cursor = connection.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        stored_hash = cursor.fetchone()
        if stored_hash:
            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash[0].encode('utf-8')):
                    return True, stored_hash[0]
                else:
                    return False, None
            except ValueError:
                print("Invalid salt or stored password.")
    return False, None



# Función para buscar datos en la base de datos (nueva función)
def fetch_from_database(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM your_table_name"
    cursor.execute(query)
    records = cursor.fetchall()
    return records


def update_password(connection, username, new_password):
    cursor = connection.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
    hashed_password_str = hashed_password.decode('utf-8')
    query = "UPDATE users SET password = %s WHERE username = %s"
    cursor.execute(query, (hashed_password_str, username))
    connection.commit()


#Funcion que returna de la crecion del usuario def check_existing_username
def check_existing_username():
    return None