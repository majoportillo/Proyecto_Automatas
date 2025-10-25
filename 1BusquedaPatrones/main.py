import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import re
import urllib.request

class BuscadorRegex:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Patrones - Expresiones Regulares")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        self.bg_color = "#1a1a2e"
        self.frame_color = "#16213e"
        self.accent_color = "#e94560"
        self.text_color = "#eef0f2"
        self.button_color = "#533483"
        
        self.root.configure(bg=self.bg_color)
        self.texto_actual = ""
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        titulo = tk.Label(
            main_frame,
            text="BUSCADOR DE PATRONES",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        titulo.pack(pady=(0, 15))
        
        entrada_frame = tk.Frame(main_frame, bg=self.frame_color)
        entrada_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            entrada_frame,
            text="Fuente de Texto",
            font=("Arial", 11, "bold"),
            bg=self.frame_color,
            fg=self.text_color
        ).pack(pady=(8, 8))
        
        botones_entrada = tk.Frame(entrada_frame, bg=self.frame_color)
        botones_entrada.pack(pady=(0, 8))
        
        self.crear_boton(botones_entrada, "Cargar Archivo", self.cargar_archivo).pack(side='left', padx=5)
        self.crear_boton(botones_entrada, "Cargar URL", self.cargar_url).pack(side='left', padx=5)
        self.crear_boton(botones_entrada, "Ingresar Texto", self.ingresar_texto).pack(side='left', padx=5)
        
        self.label_origen = tk.Label(
            entrada_frame,
            text="No hay texto cargado",
            font=("Arial", 9),
            bg=self.frame_color,
            fg="#a0a0a0"
        )
        self.label_origen.pack(pady=(0, 8))
        
        busqueda_frame = tk.Frame(main_frame, bg=self.frame_color)
        busqueda_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            busqueda_frame,
            text="Expresión Regular",
            font=("Arial", 11, "bold"),
            bg=self.frame_color,
            fg=self.text_color
        ).pack(pady=(8, 8))
        
        regex_input_frame = tk.Frame(busqueda_frame, bg=self.frame_color)
        regex_input_frame.pack(pady=(0, 8), padx=20, fill='x')
        
        tk.Label(
            regex_input_frame,
            text="Patrón:",
            font=("Arial", 10),
            bg=self.frame_color,
            fg=self.text_color
        ).pack(side='left', padx=(0, 10))
        
        self.entry_regex = tk.Entry(
            regex_input_frame,
            font=("Consolas", 11),
            bg="#2a2a3e",
            fg=self.text_color,
            insertbackground=self.text_color,
            relief='flat',
            bd=0
        )
        self.entry_regex.pack(side='left', fill='x', expand=True, ipady=8, ipadx=10)
        
        self.crear_boton(regex_input_frame, "Buscar", self.buscar_coincidencias).pack(side='left', padx=(10, 0))
        
        self.case_sensitive = tk.BooleanVar(value=False)
        check = tk.Checkbutton(
            busqueda_frame,
            text="Ignorar mayúsculas/minúsculas",
            variable=self.case_sensitive,
            font=("Arial", 9),
            bg=self.frame_color,
            fg=self.text_color,
            selectcolor="#2a2a3e",
            activebackground=self.frame_color,
            activeforeground=self.text_color
        )
        check.pack(pady=(0, 8))
        
        texto_frame = tk.Frame(main_frame, bg=self.frame_color)
        texto_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(
            texto_frame,
            text="Texto",
            font=("Arial", 11, "bold"),
            bg=self.frame_color,
            fg=self.text_color
        ).pack(pady=(8, 5))
        
        self.text_area = scrolledtext.ScrolledText(
            texto_frame,
            wrap=tk.WORD,
            height=10,
            font=("Consolas", 10),
            bg="#2a2a3e",
            fg=self.text_color,
            insertbackground=self.text_color,
            relief='flat',
            bd=0
        )
        self.text_area.pack(fill='both', expand=True, padx=10, pady=(0, 8))
        
        resultados_frame = tk.Frame(main_frame, bg=self.frame_color)
        resultados_frame.pack(fill='both', expand=True)
        
        header_resultados = tk.Frame(resultados_frame, bg=self.frame_color)
        header_resultados.pack(fill='x', pady=(8, 5))
        
        tk.Label(
            header_resultados,
            text="Coincidencias",
            font=("Arial", 11, "bold"),
            bg=self.frame_color,
            fg=self.text_color
        ).pack(side='left', padx=(10, 20))
        
        self.label_contador = tk.Label(
            header_resultados,
            text="0 coincidencias encontradas",
            font=("Arial", 9),
            bg=self.frame_color,
            fg="#a0a0a0"
        )
        self.label_contador.pack(side='left')
        
        botones_resultado = tk.Frame(resultados_frame, bg=self.frame_color)
        botones_resultado.pack(pady=(0, 8))
        
        self.crear_boton(botones_resultado, "Guardar Coincidencias", self.guardar_coincidencias).pack(side='left', padx=5)
        self.crear_boton(botones_resultado, "Limpiar", self.limpiar_todo).pack(side='left', padx=5)
        
        self.resultados_text = scrolledtext.ScrolledText(
            resultados_frame,
            wrap=tk.WORD,
            height=6,
            font=("Consolas", 9),
            bg="#2a2a3e",
            fg=self.text_color,
            insertbackground=self.text_color,
            relief='flat',
            bd=0
        )
        self.resultados_text.pack(fill='both', expand=True, padx=10, pady=(0, 8))
    
    def crear_boton(self, parent, texto, comando):
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            font=("Arial", 10),
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.lighten_color(self.button_color),
            activeforeground=self.text_color,
            relief='flat',
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8
        )
        
        btn.bind("<Enter>", lambda e: btn.config(bg=self.lighten_color(self.button_color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.button_color))
        
        return btn
    
    def lighten_color(self, color):
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r, g, b = min(255, r + 40), min(255, g + 40), min(255, b + 40)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def cargar_archivo(self):
        filename = filedialog.askopenfilename(
            title="Seleccione archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    self.texto_actual = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, self.texto_actual)
                    self.label_origen.config(text=f"Archivo: {filename}", fg="#4ecca3")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def cargar_url(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Cargar desde URL")
        dialog.geometry("450x150")
        dialog.configure(bg=self.frame_color)
        
        tk.Label(
            dialog,
            text="URL:",
            font=("Arial", 11),
            bg=self.frame_color,
            fg=self.text_color
        ).pack(pady=(20, 5), padx=20, anchor='w')
        
        url_entry = tk.Entry(
            dialog,
            font=("Arial", 10),
            bg="#2a2a3e",
            fg=self.text_color,
            insertbackground=self.text_color,
            relief='flat',
            bd=0
        )
        url_entry.pack(pady=5, padx=20, fill='x', ipady=8, ipadx=10)
        
        def descargar():
            url = url_entry.get()
            if url:
                try:
                    with urllib.request.urlopen(url) as response:
                        self.texto_actual = response.read().decode('utf-8')
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, self.texto_actual)
                        self.label_origen.config(text=f"URL: {url}", fg="#4ecca3")
                        dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar la URL:\n{str(e)}")
        
        self.crear_boton(dialog, "Cargar", descargar).pack(pady=15)
    
    def ingresar_texto(self):
        self.text_area.delete(1.0, tk.END)
        self.texto_actual = ""
        self.label_origen.config(text="Ingrese su texto en el área de texto", fg="#4ecca3")
        self.text_area.focus()
    
    def buscar_coincidencias(self):
        patron = self.entry_regex.get()
        
        if not patron:
            messagebox.showwarning("Advertencia", "Por favor ingrese una expresión regular")
            return
        
        self.texto_actual = self.text_area.get(1.0, tk.END)
        
        if not self.texto_actual.strip():
            messagebox.showwarning("Advertencia", "No hay texto para buscar")
            return
        
        try:
            flags = re.IGNORECASE if self.case_sensitive.get() else 0
            coincidencias = list(re.finditer(patron, self.texto_actual, flags))
            
            self.resultados_text.delete(1.0, tk.END)
            self.label_contador.config(text=f"{len(coincidencias)} coincidencias encontradas")
            
            if coincidencias:
                self.text_area.tag_remove("highlight", 1.0, tk.END)
                self.text_area.tag_config("highlight", background="#e94560", foreground="#ffffff")
                
                for i, match in enumerate(coincidencias, 1):
                    pos = match.start()
                    linea_num = self.texto_actual[:pos].count('\n') + 1
                    
                    start_idx = f"1.0+{match.start()}c"
                    end_idx = f"1.0+{match.end()}c"
                    self.text_area.tag_add("highlight", start_idx, end_idx)
                    
                    resultado = f"[{i}] Línea {linea_num}: {match.group()}\n"
                    self.resultados_text.insert(tk.END, resultado)
            else:
                self.resultados_text.insert(tk.END, "No se encontraron coincidencias")
                
        except re.error as e:
            messagebox.showerror("Error de Expresión Regular", 
                               f"La expresión regular es inválida:\n{str(e)}")
    
    def guardar_coincidencias(self):
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
        self.text_area.delete(1.0, tk.END)
        self.resultados_text.delete(1.0, tk.END)
        self.entry_regex.delete(0, tk.END)
        self.texto_actual = ""
        self.label_origen.config(text="No hay texto cargado", fg="#a0a0a0")
        self.label_contador.config(text="0 coincidencias encontradas")
        self.text_area.tag_remove("highlight", 1.0, tk.END)

def main():
    root = tk.Tk()
    app = BuscadorRegex(root)
    root.mainloop()

if __name__ == "__main__":
    main()