
# Gestor de PDFs con Código QR

## Descripción

Esta aplicación permite cargar archivos PDF, generar códigos QR personalizados basados en el nombre de cada PDF e insertarlos automáticamente dentro del documento, en páginas específicas según el contenido del PDF. Cuenta con una interfaz gráfica sencilla para manejar los archivos y mostrar el progreso.

## Características

- Carga múltiple de archivos PDF.
- Generación automática de códigos QR para cada archivo.
- Inserción del código QR en la página que contiene frases clave o en la primera página si el PDF es de una sola hoja.
- Uso de OCR para detectar texto en PDFs escaneados cuando el texto no es accesible directamente.
- Visualización del progreso durante el procesamiento.
- Apertura directa de archivos PDF desde la interfaz.
- Eliminación de archivos de la lista antes de procesar.
- Opciones avanzadas (por implementar).

## Requisitos

- Python 3.8 o superior
- Librerías Python:
  - `tkinter`
  - `PyPDF2`
  - `qrcode`
  - `reportlab`
  - `pdfplumber`
  - `pytesseract`
  - `pdf2image`
  - `Pillow`
- **Tesseract OCR** instalado y accesible desde el sistema:  
  [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Dependencias del sistema para `pdf2image` (como `poppler`):  
  [Poppler](https://poppler.freedesktop.org/)

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/ccgonzalezb/gestor-pdf-qr.git
cd gestor-pdf-qr
```

2. Instala las dependencias Python:

```bash
pip install -r requirements.txt
```

3. Asegúrate de tener instalado Tesseract OCR y Poppler, y configura las rutas necesarias en el código si es necesario.

## Uso

Ejecuta el programa con:

```bash
py main.py
```

### Instrucciones:

- Haz clic en **Nuevo Archivo** para agregar PDFs a la lista.
- Puedes seleccionar uno o varios PDFs.
- Haz clic en **Procesar** para generar e insertar los códigos QR en los PDFs.
- Puedes abrir los PDFs directamente haciendo clic en **Examinar**.
- La barra de progreso y el texto de estado mostrarán el avance.
- Para eliminar un archivo de la lista, haz doble clic en la fila correspondiente.

## Estructura del Proyecto

- `model.py`: Lógica para manipular PDFs, generar códigos QR y añadirlos en los archivos.
- `view.py`: Interfaz gráfica para la interacción con el usuario.
- `controller.py`: Controlador que conecta la vista con el modelo, gestionando eventos y acciones.
- `main.py`: Punto de entrada para iniciar la aplicación.

## Notas

- La ruta al ejecutable de Tesseract debe ser configurada correctamente en `model.py` (variable `pytesseract.pytesseract.tesseract_cmd`).
- Los códigos QR se guardan temporalmente como imágenes para su inserción en los PDFs.
- Actualmente, la funcionalidad de opciones avanzadas está en desarrollo.

## Autor
Cristian Camilo González Blanco
