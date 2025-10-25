import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class MenuInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - Aplicaciones")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.bg_color = "#1a1a2e"
        self.accent_color1 = "#0f3460"
        self.accent_color2 = "#16213e"
        self.button_color1 = "#e94560"
        self.button_color2 = "#533483"
        self.text_color = "#eef0f2"
        
        self.root.configure(bg=self.bg_color)
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        titulo_frame = tk.Frame(main_frame, bg=self.bg_color)
        titulo_frame.pack(pady=(0, 40))
        
        titulo = tk.Label(
            titulo_frame,
            text="MENÚ PRINCIPAL",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        titulo.pack()
        
        subtitulo = tk.Label(
            titulo_frame,
            text="Selecciona el programa: ",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#a0a0a0"
        )
        subtitulo.pack(pady=(10, 0))
        
        botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        botones_frame.pack(expand=True)
        
        self.crear_boton_app(
            botones_frame,
            "Buscador de palabras o Patrones en un archivo",
            "Busca palabras y patrones usando\nExpresiones Regulares",
            self.button_color1,
            self.abrir_buscador,
            0
        )
        
        tk.Frame(botones_frame, bg=self.bg_color, height=20).pack()
        
        self.crear_boton_app(
            botones_frame,
            "Generador de palabras a partir de una Gramática",
            "Permite generar palabras a partir de una gramática.",
            self.button_color2,
            self.abrir_app2,
            1
        )
        
        footer_frame = tk.Frame(main_frame, bg=self.bg_color)
        footer_frame.pack(side='bottom', pady=(30, 0))
        
        btn_salir = tk.Button(
            footer_frame,
            text="Salir",
            font=("Arial", 10),
            bg=self.accent_color2,
            fg=self.text_color,
            border=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.salir
        )
        btn_salir.pack()
        
        btn_salir.bind("<Enter>", lambda e: btn_salir.config(bg="#e94560"))
        btn_salir.bind("<Leave>", lambda e: btn_salir.config(bg=self.accent_color2))
    
    def crear_boton_app(self, parent, titulo, descripcion, color, comando, index):
        btn_frame = tk.Frame(parent, bg=color, highlightthickness=0)
        btn_frame.pack(pady=10, fill='x')
        
        content_frame = tk.Frame(btn_frame, bg=color)
        content_frame.pack(padx=3, pady=3, fill='both', expand=True)
        
        btn = tk.Button(content_frame, bg=color, border=0, cursor="hand2", command=comando)
        btn.pack(fill='both', expand=True)
        
        info_frame = tk.Frame(btn, bg=color)
        info_frame.pack(expand=True, pady=25, padx=30)
        
        lbl_titulo = tk.Label(info_frame, text=titulo, font=("Arial", 18, "bold"), 
                             bg=color, fg=self.text_color)
        lbl_titulo.pack()
        
        lbl_desc = tk.Label(info_frame, text=descripcion, font=("Arial", 10), 
                           bg=color, fg="#d0d0d0", justify='center')
        lbl_desc.pack(pady=(8, 0))
        
        def on_enter(e):
            nuevo_color = self.lighten_color(color)
            btn_frame.config(bg=nuevo_color)
            content_frame.config(bg=nuevo_color)
            btn.config(bg=nuevo_color)
            info_frame.config(bg=nuevo_color)
            lbl_titulo.config(bg=nuevo_color)
            lbl_desc.config(bg=nuevo_color)
        
        def on_leave(e):
            btn_frame.config(bg=color)
            content_frame.config(bg=color)
            btn.config(bg=color)
            info_frame.config(bg=color)
            lbl_titulo.config(bg=color)
            lbl_desc.config(bg=color)
        
        for widget in [btn_frame, btn, info_frame, lbl_titulo, lbl_desc]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r, g, b = min(255, r + 30), min(255, g + 30), min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def abrir_buscador(self):
        try:
            ruta = os.path.join("1BusquedaPatrones", "main.py")
            if os.path.exists(ruta):
                subprocess.Popen([sys.executable, ruta])
            else:
                messagebox.showerror("Error", f"No se encontró:\n{os.path.abspath(ruta)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir:\n{str(e)}")
    
    def abrir_app2(self):
        try:
            ruta = os.path.join("2GeneraciondePalabras", "main.py")
            if os.path.exists(ruta):
                subprocess.Popen([sys.executable, ruta])
            else:
                messagebox.showerror("Error", f"No se encontró:\n{os.path.abspath(ruta)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir:\n{str(e)}")
    
    def salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = MenuInicio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
