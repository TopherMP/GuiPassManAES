import secrets
import string
import tkinter as tk

# Función para generar la contraseña
def generate_password(var_mayus,var_num, var_symbols, pswrdEntry, slider):

    length = int(slider.get())  # Convertir el valor del slider a entero

    pswrdList = []

    minusList = list(string.ascii_lowercase)
    mayusList = list(string.ascii_uppercase)
    numbersList = list(string.digits)
    symbolsList = list('!#$%&()*^')

    minusRandom = [secrets.choice(minusList) for _ in range(length//2)]
    mayusRandom = [secrets.choice(mayusList) for _ in range(length//2)]
    numbersRandom = [secrets.choice(numbersList) for _ in range(length//3)]
    symbolsRandom = [secrets.choice(symbolsList) for _ in range(length//3)]

    # Concatenar listas obtenidas aleatoriamente para generar la contraseña
    if var_mayus.get():
        pswrdList += mayusRandom
    if var_num.get():
        pswrdList += numbersRandom
    if var_symbols.get():
        pswrdList += symbolsRandom

    pswrdList += minusRandom
    secrets.SystemRandom().shuffle(pswrdList)
    
    pswrd = ''.join(secrets.choice(pswrdList) for _ in range(length))
    
    pswrdEntry.delete(0, tk.END)  # Limpiar cualquier valor anterior
    pswrdEntry.insert(0, pswrd)  # Insertar la nueva contraseña