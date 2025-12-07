"""
Vista del Tablero Kanban.
Envuelve el tablero Kanban existente para usarlo dentro del QStackedWidget.
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ui.kanban_column import KanbanColumn
from app.controller import TaskController


class KanbanView(QWidget):
    """Vista que contiene el tablero Kanban con las tres columnas."""
    
    def __init__(self, controller: TaskController, parent=None):
        """
        Inicializa la vista del tablero Kanban.
        
        Args:
            controller: Controlador de tareas
            parent: Widget padre
        """
        super().__init__(parent)
        self.controller = controller
        self.columns = {}  # Diccionario {status: KanbanColumn}
        
        self._setup_ui()
        self._load_tasks()
    
    def _setup_ui(self):
        """Configura la interfaz del tablero Kanban."""
        # Layout horizontal para las columnas
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Crear las tres columnas Kanban
        columns_config = [
            ("Por Hacer", "todo"),
            ("En Progreso", "doing"),
            ("Hecho", "done")
        ]
        
        for title, status in columns_config:
            column = KanbanColumn(title, status, self)
            self.columns[status] = column
            main_layout.addWidget(column)
    
    def _load_tasks(self):
        """Carga todas las tareas desde la base de datos y las distribuye en las columnas."""
        tasks = self.controller.get_all_tasks()
        
        for task in tasks:
            status = task.get('status', 'todo')
            if status in self.columns:
                self.columns[status].add_task_card(task)
    
    def connect_signals(self, add_task_handler, task_moved_handler, 
                       edit_task_handler, delete_task_handler):
        """
        Conecta las señales de las columnas con los manejadores de la ventana principal.
        
        Args:
            add_task_handler: Función para manejar agregar tarea
            task_moved_handler: Función para manejar movimiento de tarea
            edit_task_handler: Función para manejar editar tarea
            delete_task_handler: Función para manejar eliminar tarea
        """
        for column in self.columns.values():
            column.add_task_requested.connect(add_task_handler)
            column.task_moved.connect(task_moved_handler)
            column.edit_task_requested.connect(edit_task_handler)
            column.delete_task_requested.connect(delete_task_handler)
    
    def refresh_tasks(self):
        """Recarga las tareas desde la base de datos."""
        # Limpiar todas las columnas
        for column in self.columns.values():
            column.clear_cards()
        
        # Cargar tareas nuevamente
        self._load_tasks()

