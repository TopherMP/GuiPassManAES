import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()

# Definir el tamaño de la ventana
window_width = 300
window_height = 150

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

# Configurar el grid para que los widgets se centren
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Widgets
label = ttk.Label(root, text="Ingrese clave maestra")
label.grid(row=1, column=1, pady=10)

masterEntry = ttk.Entry(root, show="*")  # Ocultar la entrada para simular contraseña
masterEntry.grid(row=2, column=1, padx=10, pady=5)

# Botones
confirmBtn = ttk.Button(root, text="Confirmar")
confirmBtn.grid(row=3, column=0, padx=10, pady=10)

cancelBtn = ttk.Button(root, text="Cancelar")
cancelBtn.grid(row=3, column=2, padx=10, pady=10)

root.mainloop()