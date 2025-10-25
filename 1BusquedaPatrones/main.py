import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import re
import urllib.request

class BuscadorRegex:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Patrones - Expresiones Regulares")
        self.root.geometry("900x700")
        
        # Variable para almacenar el texto
        self.texto_actual = ""
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # === SECCIÓN DE ENTRADA ===
        entrada_frame = ttk.LabelFrame(main_frame, text="Fuente de Texto", padding="10")
        entrada_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        entrada_frame.columnconfigure(1, weight=1)
        
        # Botones de entrada
        ttk.Button(entrada_frame, text="Cargar Archivo", 
                   command=self.cargar_archivo).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(entrada_frame, text="Cargar URL", 
                   command=self.cargar_url).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(entrada_frame, text="Ingresar Texto", 
                   command=self.ingresar_texto).grid(row=0, column=2, padx=5, pady=5)
        
        # Label para mostrar origen
        self.label_origen = ttk.Label(entrada_frame, text="No hay texto cargado", 
                                      foreground="gray")
        self.label_origen.grid(row=1, column=0, columnspan=3, pady=5)
        
        # === SECCIÓN DE BÚSQUEDA ===
        busqueda_frame = ttk.LabelFrame(main_frame, text="Expresión Regular", padding="10")
        busqueda_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        busqueda_frame.columnconfigure(1, weight=1)
        
        ttk.Label(busqueda_frame, text="Patrón:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.entry_regex = ttk.Entry(busqueda_frame, width=50)
        self.entry_regex.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(busqueda_frame, text="Buscar", 
                   command=self.buscar_coincidencias).grid(row=0, column=2, padx=5)
        
        # Opciones de búsqueda
        opciones_frame = ttk.Frame(busqueda_frame)
        opciones_frame.grid(row=1, column=0, columnspan=3, pady=5)
        
        self.case_sensitive = tk.BooleanVar(value=False)
        ttk.Checkbutton(opciones_frame, text="Ignorar mayúsculas/minúsculas", 
                       variable=self.case_sensitive).pack(side=tk.LEFT, padx=5)
        
        # === ÁREA DE TEXTO ===
        texto_frame = ttk.LabelFrame(main_frame, text="Texto", padding="10")
        texto_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        texto_frame.columnconfigure(0, weight=1)
        texto_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(texto_frame, wrap=tk.WORD, 
                                                    height=15, width=80)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === ÁREA DE RESULTADOS ===
        resultados_frame = ttk.LabelFrame(main_frame, text="Coincidencias", padding="10")
        resultados_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.label_contador = ttk.Label(resultados_frame, text="0 coincidencias encontradas")
        self.label_contador.pack(anchor=tk.W, pady=5)
        
        # Opciones de resultados
        opciones_resultado_frame = ttk.Frame(resultados_frame)
        opciones_resultado_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(opciones_resultado_frame, text="Guardar Coincidencias", 
                   command=self.guardar_coincidencias).pack(side=tk.LEFT, padx=5)
        ttk.Button(opciones_resultado_frame, text="Limpiar", 
                   command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        
        # Lista de resultados
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.resultados_text = scrolledtext.ScrolledText(list_frame, wrap=tk.WORD, 
                                                          height=10, width=80)
        self.resultados_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def cargar_archivo(self):
        """Cargar texto desde un archivo"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    self.texto_actual = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, self.texto_actual)
                    self.label_origen.config(text=f"Archivo: {filename}", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def cargar_url(self):
        """Cargar texto desde una URL"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Cargar desde URL")
        dialog.geometry("400x100")
        
        ttk.Label(dialog, text="URL:").pack(pady=10, padx=10, anchor=tk.W)
        url_entry = ttk.Entry(dialog, width=50)
        url_entry.pack(pady=5, padx=10)
        
        def descargar():
            url = url_entry.get()
            if url:
                try:
                    with urllib.request.urlopen(url) as response:
                        self.texto_actual = response.read().decode('utf-8')
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, self.texto_actual)
                        self.label_origen.config(text=f"URL: {url}", foreground="green")
                        dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar la URL:\n{str(e)}")
        
        ttk.Button(dialog, text="Cargar", command=descargar).pack(pady=10)
    
    def ingresar_texto(self):
        """Permitir ingresar texto directamente"""
        self.text_area.delete(1.0, tk.END)
        self.texto_actual = ""
        self.label_origen.config(text="Ingrese su texto en el área de texto", 
                                foreground="blue")
        self.text_area.focus()
    
    def buscar_coincidencias(self):
        """Buscar coincidencias de la expresión regular"""
        patron = self.entry_regex.get()
        
        if not patron:
            messagebox.showwarning("Advertencia", "Por favor ingrese una expresión regular")
            return
        
        # Obtener el texto actual del área de texto
        self.texto_actual = self.text_area.get(1.0, tk.END)
        
        if not self.texto_actual.strip():
            messagebox.showwarning("Advertencia", "No hay texto para buscar")
            return
        
        try:
            # Configurar flags
            flags = re.IGNORECASE if self.case_sensitive.get() else 0
            
            # Buscar coincidencias
            coincidencias = list(re.finditer(patron, self.texto_actual, flags))
            
            # Limpiar resultados anteriores
            self.resultados_text.delete(1.0, tk.END)
            
            # Actualizar contador
            self.label_contador.config(text=f"{len(coincidencias)} coincidencias encontradas")
            
            if coincidencias:
                # Resaltar en el texto
                self.text_area.tag_remove("highlight", 1.0, tk.END)
                self.text_area.tag_config("highlight", background="yellow")
                
                # Mostrar resultados
                lineas = self.texto_actual.split('\n')
                for i, match in enumerate(coincidencias, 1):
                    # Encontrar número de línea
                    pos = match.start()
                    linea_num = self.texto_actual[:pos].count('\n') + 1
                    
                    # Resaltar en el área de texto
                    start_idx = f"1.0+{match.start()}c"
                    end_idx = f"1.0+{match.end()}c"
                    self.text_area.tag_add("highlight", start_idx, end_idx)
                    
                    # Agregar a resultados
                    resultado = f"[{i}] Línea {linea_num}: {match.group()}\n"
                    self.resultados_text.insert(tk.END, resultado)
            else:
                self.resultados_text.insert(tk.END, "No se encontraron coincidencias")
                
        except re.error as e:
            messagebox.showerror("Error de Expresión Regular", 
                               f"La expresión regular es inválida:\n{str(e)}")
    
    def guardar_coincidencias(self):
        """Guardar las coincidencias en un archivo"""
        contenido = self.resultados_text.get(1.0, tk.END)
        
        if not contenido.strip() or contenido.strip() == "No se encontraron coincidencias":
            messagebox.showwarning("Advertencia", "No hay coincidencias para guardar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"Patrón buscado: {self.entry_regex.get()}\n")
                    file.write(f"{self.label_contador.cget('text')}\n")
                    file.write("=" * 50 + "\n\n")
                    file.write(contenido)
                messagebox.showinfo("Éxito", "Coincidencias guardadas correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def limpiar_todo(self):
        """Limpiar todas las áreas"""
        self.text_area.delete(1.0, tk.END)
        self.resultados_text.delete(1.0, tk.END)
        self.entry_regex.delete(0, tk.END)
        self.texto_actual = ""
        self.label_origen.config(text="No hay texto cargado", foreground="gray")
        self.label_contador.config(text="0 coincidencias encontradas")
        self.text_area.tag_remove("highlight", 1.0, tk.END)

def main():
    root = tk.Tk()
    app = BuscadorRegex(root)
    root.mainloop()

if __name__ == "__main__":
    main()