import qrcode
from qrcode.image.styledpil import StyledPilImage
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pdfplumber  # Importar pdfplumber
import io
import os

class PDFManager:
    def __init__(self):
        self.pdf_files = []

        # Especificar la ruta de Tesseract (modifica según la ubicación en tu sistema)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Ruta para Windows

    def add_pdf(self, file_path):
        """Añade un archivo PDF a la lista de archivos a procesar."""
        self.pdf_files.append(file_path)

    def generate_qr_for_pdf(self, pdf_name):
        """Genera un código QR basado en el nombre del archivo PDF."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(pdf_name)
        qr.make(fit=True)

        # Ruta fija de la imagen para el QR
        qr_img_path = r"C:\Users\PERSONAL\Desktop\Desarrollos Jempp\GestiónQr\imagenes\JEMPP.png"
        img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=qr_img_path)
        output_qr_img_path = f"{pdf_name}_qr.png"
        img.save(output_qr_img_path)
        return output_qr_img_path

    def add_qr_to_pdf(self, pdf_path, qr_img_path):
        """Añade un código QR a la página que contiene una de las frases específicas o a la primera página si es un PDF de una sola hoja."""
        pdf_reader = PdfReader(pdf_path)
        pdf_writer = PdfWriter()

        num_pages = len(pdf_reader.pages)

        if num_pages == 1:
            target_page_index = 0
        else:
            # Buscar la página que contiene alguna de las frases específicas
            search_phrases = [
                "Mayor General OLVEIRO PÉREZ MAHECHA",
                "Jefe de Estado Mayor de Planeación y Políticas",
                "Jefe de Estado Mayor de Planeacién y Politicas",
                "Jefe de Estado Mayor de Planeacion y Politicas",
                "PEREZ MAHECHA",
                "OLVEIRO PÉREZ MAHECHA",
            ]
            target_page_index = None

            with pdfplumber.open(pdf_path) as pdf:  # Usar pdfplumber para abrir el PDF
                for page_number, page in enumerate(pdf.pages):
                    text = page.extract_text()  # Extraer texto de la página con pdfplumber
                    if text:
                        for phrase in search_phrases:
                            if phrase in text:
                                target_page_index = page_number
                                break
                    if target_page_index is not None:
                        break  # Si ya encontró una frase, sale del loop

            # Si no se encuentra texto con pdfplumber, intenta con OCR (Tesseract)
            if target_page_index is None:
                for page_number, page in enumerate(pdf_reader.pages):
                    images = convert_from_path(pdf_path, first_page=page_number+1, last_page=page_number+1)
                    if images:
                        text = pytesseract.image_to_string(images[0])  # Usar OCR para obtener el texto
                        print(f"Texto extraído de la página {page_number + 1} con OCR:\n{text}\n")  # Imprime el texto extraído
                        for phrase in search_phrases:
                            if phrase in text:
                                target_page_index = page_number
                                break
                    if target_page_index is not None:
                        break

        if target_page_index is not None:
            # Convertir la página del PDF a una imagen
            page_images = convert_from_path(pdf_path, first_page=target_page_index+1, last_page=target_page_index+1)
            page_image = page_images[0]  # Solo obtenemos la primera (y única) imagen de la página objetivo

            # Abrir la imagen del QR y cambiar su tamaño a 150x150
            qr_img = Image.open(qr_img_path)
            qr_img = qr_img.resize((150, 150))

            # Obtener las dimensiones de la imagen de la página
            page_width, page_height = page_image.size

            # Pegar el QR en la esquina inferior derecha
            qr_position = (page_width - 80 - 100, page_height - 130 - 90)  # Desplazado 10 píxeles desde el borde
            page_image.paste(qr_img, qr_position)

            # Guardar la imagen modificada como un nuevo archivo temporal
            temp_image_path = f"{pdf_path[:-4]}_page_with_qr.png"
            page_image.save(temp_image_path)

            # Convertir la imagen modificada de nuevo a un PDF usando ReportLab
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawImage(temp_image_path, 0, 0, *letter)  # Ajusta tamaño y posición según sea necesario
            can.save()

            # Mover el archivo PDF temporal al inicio
            packet.seek(0)
            qr_pdf = PdfReader(packet)
            qr_page = qr_pdf.pages[0]

            # Añadir todas las páginas del PDF original al escritor
            for page_number, page in enumerate(pdf_reader.pages):
                if page_number == target_page_index:
                    # Superponer la página con el QR en la página original
                    pdf_writer.add_page(qr_page)
                else:
                    pdf_writer.add_page(page)

            # Guardar el nuevo archivo PDF
            output_pdf_path = f"{pdf_path[:-4]}_con_qr.pdf"
            with open(output_pdf_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)

            # Eliminar la imagen temporal
            os.remove(temp_image_path)

            return output_pdf_path

    def process_single_pdf(self, pdf_path):
        """Procesa un único archivo PDF, generando el código QR e insertándolo."""
        pdf_name = os.path.basename(pdf_path).replace(".pdf", "")
        qr_img_path = self.generate_qr_for_pdf(pdf_name)  # Generar el QR
        self.add_qr_to_pdf(pdf_path, qr_img_path)  # Insertar el QR en el PDF
        os.remove(qr_img_path)  # Eliminar la imagen QR temporal

    def process_pdfs(self, progress_callback=None):
        """Procesa todos los archivos PDF en la lista, generando un código QR para cada uno e insertándolo."""
        total_files = len(self.pdf_files)
        for index, pdf_file in enumerate(self.pdf_files):
            self.process_single_pdf(pdf_file)
            if progress_callback:
                progress_callback((index + 1) / total_files * 100)

    def is_file_in_list(self, file_path):
        """Verifica si un archivo PDF ya está en la lista."""
        return file_path in self.pdf_files

    def clear_files(self):
        """Limpia la lista de archivos PDF."""
        self.pdf_files = []
