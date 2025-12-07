"""
Componente KanbanColumn.
Widget que representa una columna del tablero Kanban.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, 
                             QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent
from ui.task_card import TaskCard


class KanbanColumn(QWidget):
    """Widget que representa una columna del tablero Kanban con capacidad de recibir drops."""
    
    # Señal cuando se necesita agregar una nueva tarea en esta columna
    add_task_requested = pyqtSignal(str)  # status
    
    # Señal cuando se mueve una tarea a esta columna
    task_moved = pyqtSignal(int, str)  # task_id, new_status
    
    # Señal cuando se solicita editar una tarea
    edit_task_requested = pyqtSignal(int)  # task_id
    
    # Señal cuando se solicita eliminar una tarea
    delete_task_requested = pyqtSignal(int)  # task_id
    
    def __init__(self, title: str, status: str, parent=None):
        """
        Inicializa la columna Kanban.
        
        Args:
            title: Título de la columna
            status: Estado asociado a esta columna ("todo", "doing", "done")
            parent: Widget padre
        """
        super().__init__(parent)
        self.status = status
        self.task_cards = {}  # Diccionario {task_id: TaskCard}
        
        self._setup_ui(title)
        self._apply_styles()
        
        # Habilitar drag & drop
        self.setAcceptDrops(True)
    
    def _setup_ui(self, title: str):
        """Configura la interfaz de la columna."""
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Título de la columna
        title_label = QLabel(title)
        title_label.setObjectName("columnTitle")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Botón para agregar nueva tarea
        add_button = QPushButton("+ Agregar Tarea")
        add_button.setObjectName("addTaskButton")
        add_button.clicked.connect(lambda: self.add_task_requested.emit(self.status))
        main_layout.addWidget(add_button)
        
        # Área scrollable para las tarjetas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        # Widget contenedor para las tarjetas
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(5, 5, 5, 5)
        self.cards_layout.setSpacing(0)
        self.cards_layout.addStretch()  # Empuja las tarjetas hacia arriba
        
        scroll_area.setWidget(self.cards_container)
        main_layout.addWidget(scroll_area)
    
    def _apply_styles(self):
        """Aplica estilos a la columna basados en su estado."""
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setProperty("status", self.status)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def add_task_card(self, task_data: dict):
        """
        Agrega una tarjeta de tarea a la columna.
        
        Args:
            task_data: Diccionario con los datos de la tarea
        """
        task_id = task_data.get('id')
        
        # Si la tarjeta ya existe, actualizarla en lugar de crear una nueva
        if task_id in self.task_cards:
            self.task_cards[task_id].update_data(task_data)
            return
        
        # Crear nueva tarjeta
        card = TaskCard(task_data, self.cards_container)
        
        # Conectar señales
        card.edit_requested.connect(self.edit_task_requested.emit)
        card.delete_requested.connect(self.delete_task_requested.emit)
        
        # Agregar al layout (antes del stretch)
        layout_count = self.cards_layout.count()
        self.cards_layout.insertWidget(layout_count - 1, card)
        
        # Guardar referencia
        self.task_cards[task_id] = card
    
    def remove_task_card(self, task_id: int):
        """
        Elimina una tarjeta de la columna.
        
        Args:
            task_id: ID de la tarea a eliminar
        """
        if task_id in self.task_cards:
            card = self.task_cards[task_id]
            self.cards_layout.removeWidget(card)
            card.setParent(None)
            card.deleteLater()
            del self.task_cards[task_id]
    
    def clear_cards(self):
        """Elimina todas las tarjetas de la columna."""
        for task_id in list(self.task_cards.keys()):
            self.remove_task_card(task_id)
    
    def get_task_card(self, task_id: int) -> TaskCard:
        """
        Obtiene una tarjeta por su ID.
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            TaskCard o None si no existe
        """
        return self.task_cards.get(task_id)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Gestiona el evento de entrada de un drag."""
        if event.mimeData().hasFormat("application/x-task") or event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Gestiona el movimiento durante el drag."""
        if event.mimeData().hasFormat("application/x-task") or event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        """Gestiona el evento de soltar una tarjeta en la columna."""
        task_id = None
        
        if event.mimeData().hasFormat("application/x-task"):
            task_id = int(event.mimeData().data("application/x-task").data().decode())
        elif event.mimeData().hasText():
            try:
                task_id = int(event.mimeData().text())
            except ValueError:
                event.ignore()
                return
        
        if task_id:
            # Emitir señal para mover la tarea
            self.task_moved.emit(task_id, self.status)
            event.acceptProposedAction()
        else:
            event.ignore()

