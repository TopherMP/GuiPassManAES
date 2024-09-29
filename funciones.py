from tkinter import messagebox
import utils
import base64

# JSON donde se almacenan los datos
dictJson = utils.load_json("passwords.json")

# Funciones CRUD
def create_data(nameEntry, userEntry, passEntry, treeview):
    app_Name = nameEntry.get()
    user_Mail_App = userEntry.get()
    pass_App = passEntry.get()

    masterPass = "Hola"
    salt, nonce, encryptedPass, tag = utils.encryptMasterPass(masterPass, pass_App)
    print(encryptedPass)

    encodePass = base64.b64encode(encryptedPass).decode('utf-8')
    encodeSalt = base64.b64encode(salt).decode('utf-8')
    encodeNonce = base64.b64encode(nonce).decode('utf-8')
    encodeTag = base64.b64encode(tag).decode('utf-8')

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
        "Tag": encodeTag
    }

    # Guardar datos en el archivo JSON
    utils.save_json("passwords.json", dictJson)

    # Actualizar el TreeView
    update_treeview(treeview)

    # Limpiar Entry
    utils.clean_entries(nameEntry, userEntry, passEntry)

# Actualizar datos
def update_data(nameEntry, userEntry, passEntry, treeview):
    app_Name = nameEntry.get()
    user_Mail_App = userEntry.get()
    pass_App = passEntry.get()

    masterPass = "Hola"
    salt, nonce, encryptedPass, tag = utils.encryptMasterPass(masterPass, pass_App)
    print(encryptedPass)

    encodePass = base64.b64encode(encryptedPass).decode('utf-8')
    encodeSalt = base64.b64encode(salt).decode('utf-8')
    encodeNonce = base64.b64encode(nonce).decode('utf-8')
    encodeTag = base64.b64encode(tag).decode('utf-8')

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
            "Tag": encodeTag
        }

        # Guardar datos actualizados
        utils.save_json("passwords.json", dictJson)

        # Actualizar el TreeView
        update_treeview(treeview)

        # Limpiar Entry
        utils.clean_entries(nameEntry, userEntry, passEntry)

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
                utils.save_json("passwords.json", dictJson)

                # Actualizar el TreeView
                update_treeview(treeview)

                # Limpiar Entry
                utils.clean_entries(nameEntry, userEntry, passEntry)
                messagebox.showinfo("Eliminado","Elemento eliminado con éxito")
            else:
                messagebox.showwarning("Advertencia", "El elemento seleccionado no existe")
        else:
            messagebox.showinfo("Cancelado","Has cancelado la operación")
    else:
        messagebox.showwarning("Advertencia", "Selecciona un elemento de la lista para eliminar")

# Actualizar tabla
def update_treeview(treeview):
    # Limpiar el Treeview antes de agregar nuevos datos
    for row in treeview.get_children():
        treeview.delete(row)

    # Insertar los datos del JSON en el Treeview
    for app, data in dictJson.items():
        treeview.insert("", "end", values=(app, data["User"], data["Password"]))
