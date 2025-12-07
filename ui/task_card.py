"""
Componente TaskCard.
Widget que representa una tarjeta de tarea individual.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QPoint
from PyQt5.QtGui import QDrag, QPainter
from app.utils import format_datetime, truncate_text


class TaskCard(QFrame):
    """Widget que representa una tarjeta de tarea con capacidad de drag & drop."""
    
    # Señales para comunicar eventos al controlador
    edit_requested = pyqtSignal(int)  # task_id
    delete_requested = pyqtSignal(int)  # task_id
    status_changed = pyqtSignal(int, str)  # task_id, new_status
    
    def __init__(self, task_data: dict, parent=None):
        """
        Inicializa la tarjeta de tarea.
        
        Args:
            task_data: Diccionario con los datos de la tarea (id, title, description, status, created_at)
            parent: Widget padre
        """
        super().__init__(parent)
        self.task_data = task_data
        self.task_id = task_data.get('id')
        self.setAcceptDrops(False)  # Las tarjetas no reciben drops, solo se arrastran
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configura la interfaz de la tarjeta."""
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Título de la tarea
        self.title_label = QLabel(truncate_text(self.task_data.get('title', 'Sin título'), 40))
        self.title_label.setObjectName("taskTitle")
        self.title_label.setWordWrap(True)
        main_layout.addWidget(self.title_label)
        
        # Descripción de la tarea
        description = self.task_data.get('description', '')
        if description:
            self.description_label = QLabel(truncate_text(description, 60))
            self.description_label.setObjectName("taskDescription")
            self.description_label.setWordWrap(True)
            main_layout.addWidget(self.description_label)
        
        # Fecha de creación
        created_at = self.task_data.get('created_at', '')
        if created_at:
            formatted_date = format_datetime(created_at)
            self.date_label = QLabel(formatted_date)
            self.date_label.setObjectName("taskDate")
            main_layout.addWidget(self.date_label)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.setObjectName("editButton")
        self.edit_button.clicked.connect(lambda: self.edit_requested.emit(self.task_id))
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(lambda: self.delete_requested.emit(self.task_id))
        buttons_layout.addWidget(self.delete_button)
        
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        
        # Configurar el widget para ser arrastrable
        self.setCursor(Qt.OpenHandCursor)
    
    def _apply_styles(self):
        """Aplica estilos adicionales a la tarjeta."""
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def mousePressEvent(self, event):
        """Inicia el drag cuando se presiona el mouse sobre la tarjeta."""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
    
    def mouseMoveEvent(self, event):
        """Gestiona el movimiento del mouse para iniciar el drag."""
        if not (event.buttons() & Qt.LeftButton):
            return
        
        # Verificar si el movimiento es suficiente para iniciar el drag
        if not hasattr(self, 'drag_start_position'):
            return
        
        distance = (event.pos() - self.drag_start_position).manhattanLength()
        min_drag_distance = 10  # Distancia mínima en píxeles para iniciar el drag
        if distance < min_drag_distance:
            return
        
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # Guardar el ID de la tarea y su estado actual en los datos del drag
        mime_data.setText(str(self.task_id))
        mime_data.setData("application/x-task", str(self.task_id).encode())
        
        drag.setMimeData(mime_data)
        
        # Crear una imagen de la tarjeta para el drag
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Cambiar el cursor durante el drag
        self.setCursor(Qt.ClosedHandCursor)
        
        # Ejecutar el drag
        drop_action = drag.exec_(Qt.MoveAction)
        
        # Restaurar el cursor
        self.setCursor(Qt.OpenHandCursor)
    
    def get_task_id(self) -> int:
        """Retorna el ID de la tarea."""
        return self.task_id
    
    def get_status(self) -> str:
        """Retorna el estado actual de la tarea."""
        return self.task_data.get('status', 'todo')
    
    def update_data(self, new_data: dict):
        """
        Actualiza los datos de la tarjeta.
        
        Args:
            new_data: Nuevo diccionario con los datos de la tarea
        """
        self.task_data = new_data
        self.task_id = new_data.get('id')
        
        # Actualizar los labels
        self.title_label.setText(truncate_text(new_data.get('title', 'Sin título'), 40))
        
        description = new_data.get('description', '')
        if hasattr(self, 'description_label'):
            if description:
                self.description_label.setText(truncate_text(description, 60))
                self.description_label.show()
            else:
                self.description_label.hide()
        elif description:
            self.description_label = QLabel(truncate_text(description, 60))
            self.description_label.setObjectName("taskDescription")
            self.description_label.setWordWrap(True)
            # Insertar después del título
            layout = self.layout()
            layout.insertWidget(1, self.description_label)
        
        created_at = new_data.get('created_at', '')
        if created_at:
            formatted_date = format_datetime(created_at)
            if hasattr(self, 'date_label'):
                self.date_label.setText(formatted_date)
            else:
                self.date_label = QLabel(formatted_date)
                self.date_label.setObjectName("taskDate")
                layout = self.layout()
                layout.insertWidget(-1, self.date_label)

