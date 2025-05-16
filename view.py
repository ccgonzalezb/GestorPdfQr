import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class PDFExcelView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de PDFs con Código QR")
        self.geometry("600x400")

        self.pdf_files = []

        self.create_widgets()

    def create_widgets(self):
        """Crea los elementos de la interfaz gráfica."""
        main_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)

        ttk.Label(header_frame, text="Seleccione los archivos PDF a cargar").pack(side=tk.LEFT)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.new_file_button = ttk.Button(button_frame, text="Nuevo Archivo")
        self.new_file_button.pack(side=tk.LEFT, padx=5)

        self.load_button = ttk.Button(button_frame, text="Procesar")
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.section_label = ttk.Label(button_frame, text="Archivos Cargados:")
        self.section_label.pack(side=tk.LEFT, padx=5)

        self.browse_button = ttk.Button(button_frame, text="Examinar")
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # Botón de opciones avanzadas
        self.advanced_options_button = ttk.Button(button_frame, text="Opciones Avanzadas", command=self.open_advanced_options)
        self.advanced_options_button.pack(side=tk.LEFT, padx=5)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        # Label de estado
        self.status_label = ttk.Label(main_frame, text="Esperando acción...")
        self.status_label.pack(pady=10)

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("#", "Ruta", "Eliminar")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("#", text="N°")
        self.tree.heading("Ruta", text="Ruta")
        self.tree.heading("Eliminar", text="Eliminar")
        self.tree.column("#", width=30, anchor=tk.CENTER)
        self.tree.column("Ruta", width=450, anchor=tk.W)
        self.tree.column("Eliminar", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', self.on_double_click)

    def update_progress(self, value):
        """Actualiza la barra de progreso."""
        self.progress["value"] = value
        self.update_idletasks()  # Forzar la actualización en la UI

    def update_status_label(self, text):
        """Actualiza el texto del Label de estado."""
        self.status_label.config(text=text)

    def add_file_to_table(self, file_path):
        """Añade un archivo PDF a la tabla."""
        next_id = len(self.tree.get_children()) + 1
        self.tree.insert("", "end", values=(next_id, file_path, "Eliminar"))

    def remove_file_from_table(self, item):
        """Elimina un archivo de la tabla."""
        self.tree.delete(item)

    def on_double_click(self, event):
        """Elimina el archivo seleccionado de la tabla al hacer doble clic."""
        item = self.tree.selection()[0]
        self.remove_file_from_table(item)

    def show_info_message(self, title, message):
        """Muestra un mensaje informativo."""
        messagebox.showinfo(title, message)

    def show_error_message(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning_message(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)

    def select_pdf(self):
        """Permite al usuario seleccionar uno o más archivos PDF."""
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        return file_paths

    def select_excel(self):
        """Permite al usuario seleccionar un archivo Excel."""
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        return file_path

    def save_excel(self):
        """Permite al usuario guardar un archivo Excel."""
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        return file_path

    def open_advanced_options(self):
        """Función de ejemplo para manejar el botón de Opciones Avanzadas."""
        messagebox.showinfo("Opciones Avanzadas", "Aquí se pueden agregar configuraciones avanzadas.")

    def clear_table(self):
        """Limpia la tabla de archivos cargados."""
        for item in self.tree.get_children():
            self.tree.delete(item)