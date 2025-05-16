import os
import time

class PDFController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.setup_view()

    def setup_view(self):
        """Configura los botones y acciones de la vista."""
        self.view.new_file_button.config(command=self.handle_add_file)
        self.view.load_button.config(command=self.handle_process_pdfs)
        self.view.browse_button.config(command=self.handle_open_files)
        self.view.advanced_options_button.config(command=self.handle_advanced_options)

    def handle_open_files(self):
        """Permite al usuario seleccionar archivos PDF y los abre en el visor predeterminado del sistema."""
        file_paths = self.view.select_pdf()
        if file_paths:
            for file_path in file_paths:
                try:
                    os.startfile(file_path)  # Windows
                except AttributeError:
                    import subprocess
                    subprocess.call(['open', file_path])  # MacOS
                    subprocess.call(['xdg-open', file_path])  # Linux

    def handle_add_file(self):
        """Maneja la acción de agregar un nuevo archivo PDF a la lista."""
        file_paths = self.view.select_pdf()
        if file_paths:
            for file_path in file_paths:
                if not self.model.is_file_in_list(file_path):
                    self.model.add_pdf(file_path)
                    self.view.add_file_to_table(file_path)
                else:
                    self.view.show_warning_message("Advertencia", f"El archivo {file_path} ya ha sido agregado.")

    def handle_process_pdfs(self):
        """Maneja la acción de procesar los PDFs, generando los QR e insertándolos."""
        if self.model.pdf_files:
            total_files = len(self.model.pdf_files)
            self.view.update_progress(0)  # Reinicia la barra de progreso
            self.view.update_status_label(f"Procesando archivo 1 de {total_files}")  # Muestra el primer archivo

            for index, pdf_file in enumerate(self.model.pdf_files):
                self.model.process_single_pdf(pdf_file)  # Procesa cada PDF
                progress = ((index + 1) / total_files) * 100
                self.view.update_progress(progress)  # Actualiza la barra de progreso
                self.view.update_status_label(f"Procesando archivo {index + 1} de {total_files}")  # Actualiza el label de estado
                time.sleep(0.5)  # Simula tiempo de procesamiento (puedes ajustar esto según tus necesidades)

            self.view.show_info_message("Éxito", "Los archivos PDF han sido procesados exitosamente.")
            self.view.clear_table()
            self.model.clear_files()
            self.view.update_progress(100)  # Completa la barra
            self.view.update_status_label("Procesamiento completado.")
        else:
            self.view.show_warning_message("Advertencia", "No hay archivos PDF para procesar.")

    def handle_advanced_options(self):
        """Maneja la acción de opciones avanzadas."""
        self.view.show_info_message("Opciones Avanzadas", "Esta es la sección de opciones avanzadas.")

    def handle_remove_file(self):
        """Maneja la acción de eliminar un archivo PDF de la lista."""
        selected_item = self.view.tree.selection()
        if selected_item:
            for item in selected_item:
                file_path = self.view.tree.item(item)['values'][1]
                self.model.pdf_files.remove(file_path)
                self.view.remove_file_from_table(item)
        else:
            self.view.show_warning_message("Advertencia", "Seleccione un archivo para eliminar.")