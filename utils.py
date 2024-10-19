import json
import tkinter as tk
import base64
from tkinter import messagebox
import encryption

# Función para cargar datos desde un archivo JSON
def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        #with open(filename, 'w') as file: json.dump(data, file, indent=4)
        return {}

# Función para guardar datos en un archivo JSON
def save_json(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo '{filename}': {str(e)}")

# Función para verificar si los campos de entrada están vacíos
#def validate_entries(*entries):
#    return all(entry.get().strip() != "" for entry in entries)

def clean_entries(*entries):
    for entry in entries:
        entry.delete(0,tk.END)

def update_treeview(treeview):
    dictJson = load_json(".passwords.json") # Se lée JSON
    
    for row in treeview.get_children():
        treeview.delete(row)

    for app, data in dictJson.items():
        
        # Se obtienen estos datos desde el JSON
        salt = data["EncryptData"]["Salt"]
        nonce = data["EncryptData"]["Nonce"]
        tag = data["EncryptData"]["Tag"]
        cipherText = data["Password"]

        # Se decodifican de base64
        decodeSalt = base64.b64decode(salt)
        decodeNonce = base64.b64decode(nonce)
        decodeTag = base64.b64decode(tag)
        decodeCipherText = base64.b64decode(cipherText)

        print(f"Salt a: {decodeSalt}")
        print(f"Nonce a: {decodeNonce}")
        print(f"Tag a: {decodeTag}")
        print(f"CipherText a: {decodeCipherText}")

        master = data["EncryptData"]["MasterPass"] # Se obtiene la contraseña maestra

        decipher = encryption.decryptMasterPass(master, decodeSalt, decodeNonce, decodeTag, decodeCipherText) # Se desencripta
        print(f"decipher {decipher}")

        treeview.insert("", "end", values=(app, data["User"], decipher)) # Se actualiza la tabla con los datos desencriptados y decodificados