"""
Punto de entrada principal de la aplicación.
Organizador de Tareas estilo Kanban.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow


def load_styles(app: QApplication):
    """
    Carga los estilos CSS desde el archivo styles.qss.
    
    Args:
        app: Instancia de QApplication
    """
    try:
        with open('ui/styles.qss', 'r', encoding='utf-8') as f:
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)
            print("✓ Estilos cargados correctamente")
    except FileNotFoundError:
        print("⚠ Advertencia: No se encontró el archivo 'ui/styles.qss'. Se usarán estilos por defecto.")
    except Exception as e:
        print(f"⚠ Advertencia: Error al cargar los estilos: {e}")


def main():
    """Función principal que inicia la aplicación."""
    # Habilitar alta DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Crear la aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("Organizador de Tareas Kanban")
    
    # Cargar estilos
    load_styles(app)
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

