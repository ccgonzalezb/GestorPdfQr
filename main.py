from model import PDFManager
from view import PDFExcelView
from controller import PDFController

def main():
    # Crear instancias del modelo y la vista
    model = PDFManager()
    view = PDFExcelView()
    
    # Crear el controlador y pasarle el modelo y la vista
    controller = PDFController(view, model)
    
    # Iniciar la aplicación
    view.mainloop()

if __name__ == "__main__":
    main()
