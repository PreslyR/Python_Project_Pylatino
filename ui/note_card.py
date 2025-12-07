"""
Componente NoteCard.
Widget que representa una tarjeta de nota individual.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from app.utils import format_datetime, truncate_text


class NoteCard(QFrame):
    """Widget que representa una tarjeta de nota."""
    
    # Señales para comunicar eventos
    edit_requested = pyqtSignal(int)  # note_id
    delete_requested = pyqtSignal(int)  # note_id
    
    def __init__(self, note_data: dict, parent=None):
        """
        Inicializa la tarjeta de nota.
        
        Args:
            note_data: Diccionario con los datos de la nota (id, title, content, created_at, updated_at)
            parent: Widget padre
        """
        super().__init__(parent)
        self.note_data = note_data
        self.note_id = note_data.get('id')
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configura la interfaz de la tarjeta."""
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Título de la nota
        self.title_label = QLabel(truncate_text(self.note_data.get('title', 'Sin título'), 50))
        self.title_label.setObjectName("noteTitle")
        self.title_label.setWordWrap(True)
        main_layout.addWidget(self.title_label)
        
        # Contenido de la nota
        content = self.note_data.get('content', '')
        if content:
            self.content_label = QLabel(truncate_text(content, 150))
            self.content_label.setObjectName("noteContent")
            self.content_label.setWordWrap(True)
            main_layout.addWidget(self.content_label)
        
        # Espaciador
        main_layout.addStretch()
        
        # Fecha de última modificación
        updated_at = self.note_data.get('updated_at', '')
        if updated_at:
            formatted_date = format_datetime(updated_at)
            self.date_label = QLabel(f"Modificado: {formatted_date}")
            self.date_label.setObjectName("noteDate")
            main_layout.addWidget(self.date_label)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.setObjectName("editButton")
        self.edit_button.clicked.connect(lambda: self.edit_requested.emit(self.note_id))
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(lambda: self.delete_requested.emit(self.note_id))
        buttons_layout.addWidget(self.delete_button)
        
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)
    
    def _apply_styles(self):
        """Aplica estilos adicionales a la tarjeta."""
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def get_note_id(self) -> int:
        """Retorna el ID de la nota."""
        return self.note_id
    
    def update_data(self, new_data: dict):
        """
        Actualiza los datos de la tarjeta.
        
        Args:
            new_data: Nuevo diccionario con los datos de la nota
        """
        self.note_data = new_data
        self.note_id = new_data.get('id')
        
        # Actualizar los labels
        self.title_label.setText(truncate_text(new_data.get('title', 'Sin título'), 50))
        
        content = new_data.get('content', '')
        if hasattr(self, 'content_label'):
            if content:
                self.content_label.setText(truncate_text(content, 150))
                self.content_label.show()
            else:
                self.content_label.hide()
        elif content:
            self.content_label = QLabel(truncate_text(content, 150))
            self.content_label.setObjectName("noteContent")
            self.content_label.setWordWrap(True)
            # Insertar después del título
            layout = self.layout()
            layout.insertWidget(1, self.content_label)
        
        updated_at = new_data.get('updated_at', '')
        if updated_at:
            formatted_date = format_datetime(updated_at)
            if hasattr(self, 'date_label'):
                self.date_label.setText(f"Modificado: {formatted_date}")
            else:
                self.date_label = QLabel(f"Modificado: {formatted_date}")
                self.date_label.setObjectName("noteDate")
                layout = self.layout()
                layout.insertWidget(-2, self.date_label)

