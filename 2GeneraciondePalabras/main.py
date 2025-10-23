import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

#GRAMÁTICAS 
GRAMATICAS = {
    "Contraseñas": {
        "S": ["<A><B><C>"],
        "A": ["Drk1", "N5va", "Ne8o", "Cy6br", "Bl2e", "S3trm", "Bt7e", "Cl9od"],
        "B": ["1L/3", "5K6", "7m9", "2025", "9a@9", "0*07"],
        "C": ["!", "@", "#", "$", "%", "&", "_gt"]
    },
    "Correos": {
        "S": ["<A><B><C><D>"],
        "A": ["jimena", "marta", "pablo", "ana", "carlos", "lety", "alexis", "sofia", "diego", "valeria", "camila", "marco", "natalia"],
        "B": ["", "123", "_pol", "1999", "867", "gt", "mx"],
        "C": ["@gmail", "@hotmail", "@yahoo", "@outlook", "@edu", ],
        "D": [".com", ".gt", ".org", ".net"]
    },
    "Direcciones": {
        "S": ["<A> <B>, <C>"],
        "A": ["Calle", "Avenida", "Boulevard", "Barrio", "Residencial", "Urbanización", "Colonia", "Jardines"],
        "B": ["San Francisco", "Las Flores", "La Esperanza", "Las Marías", "La Arboleda", "El Paraíso", "Los Pinos", "Santa Ana", "Villa Nueva", "El Carmen", "Los Robles", "La Cima", "Vista Hermosa"],
        "C": ["Zona 1", "Zona 5", "Zona 10", "Zona 12", "Zona 18", "Zona 21", "Zona 7", "Zona 2", "Zona 3", "Zona 4"]
    },
    "Usuarios": {
        "S": ["<A><B><C>"],
        "A": ["Cool", "Happy", "Dark", "Fast", "Smart", "Crazy", "Power", "Silent", "Brave", "Lucky", "Wild", "Mighty", "Fierce", "Swift", "Bold", "Epic", "Ninja", "Shadow", "Ghost", "Storm", "Fire", "Ice"],
        "B": ["Cat", "Dog", "Lion", "Fox", "Wolf", "Bear", "Hawk", "Tiger", "Eagle", "Shark", "Dragon", "Panther", "Cheetah", "Falcon", "Raven", "Viper", "Jaguar", "Cougar", "Lynx", "Otter"],
        "C": ["", "123", "007", "2025", "_gt", "_mx", "xyz", "pro", "king", "queen", "master", "warrior", "rider"]
    },
    "Saludos": {
        "S": ["<A> <B>,<C>"],
        "A": ["Hola", "Buenos días", "Qué tal", "Hey", "Buenas tardes", "Saludos", "Qué onda", "Qué hubo", "Saludos cordiales", "Estimado", "Querido", "Apreciado", "Buen día"],
        "B": ["Juan", "María", "Carlos", "Ana", "Pedro", "equipo", "amigo", "compañero", "colega", "socio", "querido", "joven", "invitado"],
        "C": [" gusto en verte!", " cómo estás?", " bienvenido!", " qué gusto!", " espero que estés bien!", " un placer saludarte!", " feliz de verte!", " que tengas un buen día!", " saludos!", " cuídate mucho!", " nos vemos pronto!"]
    }
}

# Parámetros internos
DEFAULT_MAX_STEPS = 100     
DEFAULT_MAX_ATTEMPTS = 500    
DEFAULT_MAX_LEN_CHARS = 120   
DEFAULT_UNIQUE = True         
DEFAULT_SECURE_PW = True      
DEFAULT_SECURE_PW_LEN = 8     
DEFAULT_SECURE_USE_SYMBOLS = True

#Funciones de generación 
def secure_password(length=12, use_upper=True, use_symbols=True, ensure_each=True):
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%&*()-_+=?"
    pool = lower + digits
    if use_upper:
        pool += string.ascii_uppercase
    if use_symbols:
        pool += symbols

    if length < 4:
        length = 4

    pwd = []
    if ensure_each:
        pwd.append(random.choice(lower))
        pwd.append(random.choice(digits))
        if use_upper:
            pwd.append(random.choice(string.ascii_uppercase))
        if use_symbols:
            pwd.append(random.choice(symbols))

    while len(pwd) < length:
        pwd.append(random.choice(pool))
    random.shuffle(pwd)
    return ''.join(pwd)

def generate_from_grammar(gram, initial="S", max_steps=DEFAULT_MAX_STEPS):
    if initial not in gram:
        initial = list(gram.keys())[0]
    current = gram[initial][0]
    steps = 0
    while ("<" in current and ">" in current) and steps < max_steps:
        replaced = False
        for sym in gram.keys():
            token = f"<{sym}>"
            if token in current:
                options = gram[sym] if gram[sym] else [""]
                choice = random.choice(options)
                current = current.replace(token, choice, 1)
                steps += 1
                replaced = True
                break
        if not replaced:
            break
    current = " ".join(current.split())
    current = current.replace(" ,", ",").replace(" .", ".")
    return current.strip(), steps

def generate_unique(grammar, count,
                    max_steps_per_derivation=DEFAULT_MAX_STEPS,
                    max_attempts=DEFAULT_MAX_ATTEMPTS,
                    max_length_chars=DEFAULT_MAX_LEN_CHARS):
    results = []
    seen = set()
    attempts = 0
    while len(results) < count and attempts < max_attempts:
        attempts += 1
        out, steps = generate_from_grammar(grammar, initial="S", max_steps=max_steps_per_derivation)
        if not out:
            continue
        if len(out) > max_length_chars:
            continue
        if out in seen:
            continue
        seen.add(out)
        results.append(out)  
    return results

# Interfaz
class SimpleGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Generador de Gramáticas")
        root.geometry("640x480")
        root.config(bg="#0b1020")

        self.title_font = ("Segoe UI", 18, "bold")
        self.lbl_font = ("Segoe UI", 11, "bold")
        self.txt_font = ("Consolas", 11)

        title = tk.Label(root, text="Generador de Gramáticas", font=self.title_font,
                         fg="#7ee7c7", bg="#0b1020")
        title.pack(pady=(14, 8))

        subtitle = tk.Label(root, text="Selecciona la gramática en la izquierda y escribe cuántas palabras quieres.",
                            font=("Segoe UI", 9), fg="#bcd9d0", bg="#0b1020")
        subtitle.pack()

        main = tk.Frame(root, bg="#0b1020")
        main.pack(fill="both", expand=True, padx=16, pady=12)

        left = tk.Frame(main, bg="#071019", width=200)
        left.pack(side="left", fill="y", padx=(0,12), pady=4)
        left.pack_propagate(False)

        lbl_choice = tk.Label(left, text="Gramáticas", font=self.lbl_font, bg="#071019", fg="#dff6ee")
        lbl_choice.pack(pady=(10,6))

        self.gram_listbox = tk.Listbox(left, font=("Segoe UI", 11), bg="#061017", fg="#e9f9f0",
                                       selectbackground="#2ee6c1", activestyle="none", bd=0, highlightthickness=0)
        for g in GRAMATICAS.keys():
            self.gram_listbox.insert(tk.END, g)
        self.gram_listbox.select_set(0)
        self.gram_listbox.pack(fill="y", expand=True, padx=10, pady=(0,12))

        center = tk.Frame(main, bg="#0b1020")
        center.pack(side="left", fill="both", expand=True)

        lbl_qty = tk.Label(center, text="Cantidad de palabras a generar:", font=self.lbl_font, bg="#0b1020", fg="#dff6d8")
        lbl_qty.pack(pady=(20,6))

        self.qty_entry = tk.Entry(center, font=("Segoe UI", 14), justify="center", width=8)
        self.qty_entry.insert(0, "10")
        self.qty_entry.pack(pady=(0,12))

        gen_btn = tk.Button(center, text="Generar", font=("Segoe UI", 12, "bold"), bg="#2ee6c1", fg="#021018",
                            width=18, command=self.on_generate, relief="flat")
        gen_btn.pack(pady=(6,10))

        res_frame = tk.Frame(root, bg="#071019")
        res_frame.pack(fill="both", expand=True, padx=16, pady=(6,12))

        lbl_res = tk.Label(res_frame, text="Resultados:", font=self.lbl_font, bg="#071019", fg="#dff6d8")
        lbl_res.pack(anchor="w", padx=8, pady=(8,0))

        self.result_text = tk.Text(res_frame, height=10, font=self.txt_font, bg="#061017", fg="#e9f9f0",
                                   bd=0, highlightthickness=0, wrap="word")
        self.result_text.pack(fill="both", expand=True, padx=8, pady=(4,8))

        export_btn = tk.Button(root, text="Exportar resultados", font=("Segoe UI", 10, "bold"),
                               bg="#ffb703", fg="#081018", command=self.on_export, relief="flat")
        export_btn.pack(pady=(0,12))

        footer = tk.Label(root, text="Proyecto - Autómatas y Lenguajes Formales", font=("Segoe UI", 9),
                          bg="#0b1020", fg="#9fb6b2")
        footer.pack(side="bottom", pady=6)

    def on_generate(self):
        # Leer gramática seleccionada y cantidad
        sel = self.gram_listbox.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una gramática.")
            return
        gram_name = self.gram_listbox.get(sel[0])
        try:
            qty = int(self.qty_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atención", "Escribe una cantidad válida")
            return

        self.result_text.delete(1.0, tk.END)

        # Parámetros internos
        max_steps = DEFAULT_MAX_STEPS
        max_attempts = DEFAULT_MAX_ATTEMPTS
        max_len = DEFAULT_MAX_LEN_CHARS
        unique = DEFAULT_UNIQUE
        secure_pw = DEFAULT_SECURE_PW and gram_name == "Contraseñas"
        secure_pw_length = DEFAULT_SECURE_PW_LEN
        secure_use_upper = DEFAULT_SECURE_USE_UPPER
        secure_use_symbols = DEFAULT_SECURE_USE_SYMBOLS

        results = []

        if secure_pw:
            seen = set()
            attempts = 0
            while len(results) < qty and attempts < max_attempts:
                attempts += 1
                pwd = secure_password(length=secure_pw_length, use_upper=secure_use_upper, use_symbols=secure_use_symbols)
                if unique and pwd in seen:
                    continue
                seen.add(pwd)
                results.append(pwd)
        else:
            gram = GRAMATICAS[gram_name]
            if unique:
                generated = generate_unique(gram, qty,
                                            max_steps_per_derivation=max_steps,
                                            max_attempts=max_attempts,
                                            max_length_chars=max_len)
                results = generated
            else:
                attempts = 0
                res = []
                while len(res) < qty and attempts < max_attempts:
                    attempts += 1
                    out, steps = generate_from_grammar(gram, initial="S", max_steps=max_steps)
                    if not out or len(out) > max_len:
                        continue
                    res.append(out)
                results = res

        if not results:
            self.result_text.insert(tk.END, "No se pudieron generar resultados con las restricciones internas.\n")
            return
        for i, val in enumerate(results, start=1):
            self.result_text.insert(tk.END, f"{i}. {val}\n")

    def on_export(self):
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Atención", "No hay resultados para exportar.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if not filepath:
            return
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Guardado", f"Resultados guardados en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGeneratorApp(root)
    root.mainloop()

