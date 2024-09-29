import tkinter as tk
from tkinter import ttk
import base64
import funciones, utils, genPass

dictJson = utils.load_json(".passwords.json")

# Función para actualizar el Treeview
def update_treeview(treeview):

    for row in treeview.get_children():
        treeview.delete(row)

    for app, data in dictJson.items():

        salt = data["Salt"]
        nonce = data["Nonce"]
        tag = data["Tag"]
        cipherText = data["Password"]

        decodeSalt = base64.b64decode(salt)
        decodeNonce = base64.b64decode(nonce)
        decodeTag = base64.b64decode(tag)
        decodeCipherText = base64.b64decode(cipherText)
        
        print(f"Salt a: {decodeSalt}")
        print(f"Nonce a: {decodeNonce}")
        print(f"Tag a: {decodeTag}")
        print(f"CipherText a: {decodeCipherText}")


        masterPass = "Hola"

        decipher = utils.decryptMasterPass(masterPass, decodeSalt, decodeNonce, decodeTag, decodeCipherText)
        print(f"decipher {decipher}")

        treeview.insert("", "end", values=(app, data["User"], decipher))

# Obtener los datos del TreeView
def get_Data_Entry(event):
    selected_index = treeview.selection()

    if selected_index:

        item = treeview.item(selected_index)
        app_Name = item["values"]

        nameEntry.delete(0, tk.END)
        nameEntry.insert(0, app_Name[0])
        userEntry.delete(0, tk.END)
        userEntry.insert(0, app_Name[1])
        passEntry.delete(0, tk.END)
        passEntry.insert(0, app_Name[2])

def updateLabelSlider(e):
    value = int(slider.get())  # Convertir el valor del slider a entero
    sliderValue.config(text=value)  # Actualizar el texto del label con el valor del slider
    
# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestor de Contraseñas")

# Definir el tamaño de la ventana
window_width = 600
window_height = 600

# Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Establecer la geometría de la ventana con la posición centrada
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Evitar redimensionar la ventana
root.resizable(False, False)

root.config(bg="#f0f0f0")  # Fondo gris claro

# Campo de entrada de datos
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

tk.Label(frame, text="Ingresa nombre página/aplicación:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
nameEntry = ttk.Entry(frame, width=30)
nameEntry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Ingresa tu nombre de usuario o mail:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
userEntry = ttk.Entry(frame, width=30)
userEntry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Ingresa la contraseña:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
passEntry = ttk.Entry(frame, width=30)
passEntry.grid(row=2, column=1, padx=5, pady=5)

# Botones para CRUD
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

btn_create = ttk.Button(button_frame, text="Crear", command=lambda: funciones.create_data(nameEntry, userEntry, passEntry, treeview))
btn_create.grid(row=0, column=0, padx=5, pady=5)

btn_update = ttk.Button(button_frame, text="Actualizar", command=lambda: funciones.update_data(nameEntry, userEntry, passEntry, treeview))
btn_update.grid(row=0, column=1, padx=5, pady=5)

btn_delete = ttk.Button(button_frame, text="Eliminar", command=lambda: funciones.delete_data(treeview, nameEntry, userEntry, passEntry))
btn_delete.grid(row=0, column=2, padx=5, pady=5)

# password generate field
generate_frame = ttk.Frame(root)
generate_frame.pack(pady=10)

# Crear una etiqueta para el slider
label = tk.Label(generate_frame, text="Cantidad de carácteres")
label.grid(row=0, column=2)

# Crear variables para los checkbuttons
var_mayus = tk.IntVar(value=1)
var_num = tk.IntVar(value=1)
var_symbols = tk.IntVar(value=1)

# Crear un label para mostrar el valor actual del slider
sliderValue = tk.Label(generate_frame, text="8")  # Mostrar el valor inicial del slider
sliderValue.grid(row=1, column=3)

# Crear un slider para elegir la longitud de la contraseña
slider = ttk.Scale(generate_frame, from_=8, to=128, orient='horizontal', command=updateLabelSlider)
slider.set(20)  # Establecer el valor inicial del slider
slider.grid(row=1, column=2, pady=5)

# Crear checkbuttons para opciones de la contraseña
check_Mayus = tk.Checkbutton(generate_frame, text="Mayúsculas", variable=var_mayus)
check_Mayus.grid(row=2, column=2)

check_Num = tk.Checkbutton(generate_frame, text="Números", variable=var_num)
check_Num.grid(row=2, column=3)

check_Symbols = tk.Checkbutton(generate_frame, text="Símbolos", variable=var_symbols)
check_Symbols.grid(row=2, column=4)

btn_generate = ttk.Button(generate_frame, text="Generar contraseña",command=lambda: genPass.generate_password(var_mayus,var_num, var_symbols, passEntry, slider))
btn_generate.grid(row=1,column=4)

# Configuración del Treeview
treeview = ttk.Treeview(root, columns=("Aplicación", "Usuario", "Contraseña"), show="headings", height=10)
treeview.pack(padx=20)

treeview.bind("<<TreeviewSelect>>", get_Data_Entry)

treeview.heading("Aplicación", text="Aplicación")
treeview.heading("Usuario", text="Usuario")
treeview.heading("Contraseña", text="Contraseña")

treeview.column("Aplicación")
treeview.column("Usuario")
treeview.column("Contraseña")

# Actualizar datos antes de ejecutar
update_treeview(treeview)

# Ejecutar la ventana
root.mainloop()