import json
import tkinter as tk
from tkinter import messagebox
import hashlib
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def deriveKey(masterPass, salt): # Derive master password
    key = PBKDF2(masterPass, salt, dkLen=32, count=125000, hmac_hash_module=SHA256)
    return key

def encryptMasterPass(masterPass, pswrd):
    salt = get_random_bytes(16)
    key = deriveKey(masterPass,salt)

    cipher = AES.new(key,AES.MODE_EAX)
    nonce = cipher.nonce
    cipherText, tag = cipher.encrypt_and_digest(pswrd.encode('utf-8'))

    return salt, nonce, cipherText, tag

def decryptMasterPass(masterPass, salt, nonce, tag, cipherText):

    key = deriveKey(masterPass, salt)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plainText = cipher.decrypt_and_verify(cipherText, tag)

    return plainText.decode('utf-8')


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
def validate_entries(*entries):
    return all(entry.get().strip() != "" for entry in entries)

def clean_entries(*entries):
    for entry in entries:
        entry.delete(0,tk.END)