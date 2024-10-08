import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import utils
import base64
import encryption

# JSON donde se almacenan los datos
dictJson = utils.load_json(".passwords.json")

# Funciones CRUD
def create_data(masterEntry, nameEntry, userEntry, passEntry, treeview):
    app_Name = nameEntry.get()
    user_Mail_App = userEntry.get()
    pass_App = passEntry.get()
    master = masterEntry.get()

    if master == "":
        messagebox.showwarning("Clave maestra", "Por favor, ingrese su clave maestra.")
    else:

        salt, nonce, encryptedPass, tag = encryption.encryptMasterPass(master, pass_App)
        print(encryptedPass)

        encodePass = base64.b64encode(encryptedPass).decode('utf-8')
        encodeSalt = base64.b64encode(salt).decode('utf-8')
        encodeNonce = base64.b64encode(nonce).decode('utf-8')
        encodeTag = base64.b64encode(tag).decode('utf-8')

        #encodeMaster = base64.b64encode(master).decode('utf-8')

        print(f"Salt: {encodeSalt}")
        print(f"Nonce: {encodeNonce}")
        print(f"Tag: {encodeTag}")
        print(f"CipherText: {encodePass}")


        # Verificar que los campos de texto no estén vacíos
        if not app_Name or not user_Mail_App or not pass_App:
            messagebox.showwarning("Advertencia", "Tienes que completar todos los datos")
            return

        # Verificar si la aplicación ya está en el JSON
        if app_Name in dictJson:
            messagebox.showwarning("Advertencia", "El nombre de la app ya lo tienes agregado, por favor, cambia el nombre")
            return
        

        dictJson[app_Name] = {
            "User": user_Mail_App,
            "Password": encodePass,
            "Salt": encodeSalt,
            "Nonce": encodeNonce,
            "Tag": encodeTag,
            "MasterPass": master
        }

        # Guardar datos en el archivo JSON
        utils.save_json(".passwords.json", dictJson)

        # Actualizar el TreeView
        utils.update_treeview(treeview)

        # Limpiar Entry
        utils.clean_entries(masterEntry, nameEntry, userEntry, passEntry)

# Actualizar datos
def update_data(masterEntry, nameEntry, userEntry, passEntry, treeview):
    for app, data in dictJson.items():

        app_Name = nameEntry.get()
        user_Mail_App = userEntry.get()
        pass_App = passEntry.get()

        salt = data['Salt']
        nonce = data['Nonce']
        tag = data['Tag']

        master = data["MasterPass"]

        if masterEntry.get() != master:
            messagebox.showwarning("Clave maestra", "Por favor, ingrese su clave maestra.")

        else:
            salt, nonce, encryptedPass, tag = encryption.encryptMasterPass(master, pass_App)
            print(encryptedPass)

            # Se codifica en base64
            encodePass = base64.b64encode(encryptedPass).decode('utf-8')
            encodeSalt = base64.b64encode(salt).decode('utf-8')
            encodeNonce = base64.b64encode(nonce).decode('utf-8')
            encodeTag = base64.b64encode(tag).decode('utf-8')

            #encodeMaster = base64.b64encode(master).decode('utf-8')

            # Verificar que los campos de texto no estén vacíos
            if not app_Name or not user_Mail_App or not pass_App:
                messagebox.showwarning("Advertencia", "Tienes que seleccionar una cuenta para editar")
                return

            selected_item = treeview.selection()

            if selected_item:
                values = treeview.item(selected_item)['values']
                original_App_Name = values[0]

                # Eliminar el nombre original si ha cambiado
                if original_App_Name != app_Name:
                    del dictJson[original_App_Name]

                dictJson[app_Name] = {
                    "User": user_Mail_App,
                    "Password": encodePass,
                    "Salt": encodeSalt,
                    "Nonce": encodeNonce,
                    "Tag": encodeTag,
                    "MasterPass": master
                }

                # Guardar datos actualizados
                utils.save_json(".passwords.json", dictJson)

                # Actualizar el TreeView
                utils.update_treeview(treeview)

                # Limpiar Entry
                utils.clean_entries(masterEntry, nameEntry, userEntry, passEntry)

            else:
                messagebox.showwarning("Advertencia", "Selecciona un elemento de la lista para actualizar")

# Eliminar un dato
def delete_data(treeview, nameEntry, userEntry, passEntry):
    selected_index = treeview.selection()

    if selected_index:
        item = treeview.item(selected_index)
        app_Name = item["values"][0]
        
        delete=messagebox.askokcancel("Eliminar dato","Estas seguro que deseas eliminar")
        if delete:
            # Verificar si el nombre del item seleccionado existe en el diccionario
            if app_Name in dictJson:
                del dictJson[app_Name]

                # Guardar los cambios en el archivo JSON
                utils.save_json(".passwords.json", dictJson)

                # Actualizar el TreeView
                utils.update_treeview(treeview)

                # Limpiar Entry
                utils.clean_entries(nameEntry, userEntry, passEntry)
                messagebox.showinfo("Eliminado","Elemento eliminado con éxito")
            else:
                messagebox.showwarning("Advertencia", "El elemento seleccionado no existe")
        else:
            messagebox.showinfo("Cancelado","Has cancelado la operación")
    else:
        messagebox.showwarning("Advertencia", "Selecciona un elemento de la lista para eliminar")

# Obtener los datos del TreeView
def get_Data_Entry(event, treeview, nameEntry, userEntry, passEntry):
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

def updateLabelSlider(e,slider, sliderValue):
    value = int(slider.get())  # Convertir el valor del slider a entero
    sliderValue.config(text=value)  # Actualizar el texto del label con el valor del slider

def encrypt(root):
    for app, data in dictJson.items():
        master = data["MasterPass"]

        salt, nonce, encryptedPass, tag = encryption.encryptMasterPass(master, data["Password"])
        print(encryptedPass)

        encodePass = base64.b64encode(encryptedPass).decode('utf-8')
        print(encodePass)
        encodeSalt = base64.b64encode(salt).decode('utf-8')
        encodeNonce = base64.b64encode(nonce).decode('utf-8')
        encodeTag = base64.b64encode(tag).decode('utf-8')

        dictJson[app] = {
        "User": data["User"],
        "Password": encodePass,
        "Salt": encodeSalt,
        "Nonce": encodeNonce,
        "Tag": encodeTag,
        "MasterPass": master
    }
    root.destroy()