import tkinter as tk
from tkinter import filedialog, messagebox
import re

root = tk.Tk()
root.title("Buscador de Patrones con Expresiones Regulares")
root.geometry("600x400")

def buscar_patrones():
    # Obtener el texto del área de texto
    texto = text_area.get("1.0", tk.END)

    # Obtener el patrón de la entrada
    patron = entry_patron.get()

    # Buscar el patrón en el texto
    coincidencias = re.findall(patron, texto)

    # Mostrar las coincidencias
    if coincidencias:
        messagebox.showinfo("Resultados", f"Se encontraron {len(coincidencias)} coincidencias.")
    else:
        messagebox.showinfo("Resultados", "No se encontraron coincidencias.")

# Crear widgets
label_archivo = tk.Label(root, text="Archivo:")
entry_archivo = tk.Entry(root)
button_buscar = tk.Button(root, text="Buscar", command=buscar_patrones)

# Ubicar los widgets en la ventana
label_archivo.pack()
entry_archivo.pack()
button_buscar.pack()

root.mainloop()