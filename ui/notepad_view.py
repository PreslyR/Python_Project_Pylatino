"""
Vista del Bloc de Notas.
Muestra las notas como tarjetas organizadas en un grid.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QScrollArea, QDialog,
                             QLineEdit, QTextEdit, QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
from ui.note_card import NoteCard
from app.note_controller import NoteController


class NoteDialog(QDialog):
    """Diálogo para crear o editar una nota."""
    
    def __init__(self, parent=None, note_data=None):
        """
        Inicializa el diálogo.
        
        Args:
            parent: Widget padre
            note_data: Diccionario con los datos de la nota si se está editando, None si es nueva
        """
        super().__init__(parent)
        self.note_data = note_data
        self.is_editing = note_data is not None
        
        title = "Editar Nota" if self.is_editing else "Nueva Nota"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        self._setup_ui()
        
        if self.is_editing:
            self._load_note_data()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Título:")
        layout.addWidget(title_label)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Ingrese el título de la nota...")
        layout.addWidget(self.title_edit)
        
        # Contenido
        content_label = QLabel("Contenido:")
        layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Escribe el contenido de la nota aquí...")
        layout.addWidget(self.content_edit)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self._validate_and_accept)
        buttons_layout.addWidget(self.save_button)
        
        layout.addLayout(buttons_layout)
    
    def _load_note_data(self):
        """Carga los datos de la nota en los campos del formulario."""
        if self.note_data:
            self.title_edit.setText(self.note_data.get('title', ''))
            self.content_edit.setPlainText(self.note_data.get('content', ''))
    
    def _validate_and_accept(self):
        """Valida los datos antes de cerrar el diálogo."""
        title = self.title_edit.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "El título de la nota es obligatorio.")
            return
        
        self.accept()
    
    def get_note_data(self) -> dict:
        """
        Retorna los datos ingresados en el formulario.
        
        Returns:
            Diccionario con title y content
        """
        return {
            'title': self.title_edit.text().strip(),
            'content': self.content_edit.toPlainText().strip()
        }


class NotepadView(QWidget):
    """Vista del bloc de notas que muestra las notas como tarjetas."""
    
    def __init__(self, parent=None):
        """
        Inicializa la vista del bloc de notas.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        self.controller = NoteController()
        self.note_cards = {}  # Diccionario {note_id: NoteCard}
        
        self._setup_ui()
        self._load_notes()
    
    def _setup_ui(self):
        """Configura la interfaz del bloc de notas."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Barra de herramientas superior
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)
        
        # Título
        title_label = QLabel("📝 Bloc de Notas")
        title_label.setObjectName("notepadTitle")
        toolbar_layout.addWidget(title_label)
        
        toolbar_layout.addStretch()
        
        # Botón: Agregar Nota
        self.add_button = QPushButton("➕ Nueva Nota")
        self.add_button.setObjectName("notepadButton")
        self.add_button.clicked.connect(self._on_add_note_requested)
        toolbar_layout.addWidget(self.add_button)
        
        layout.addLayout(toolbar_layout)
        
        # Área scrollable para las tarjetas de notas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        # Widget contenedor para las tarjetas (con grid layout)
        self.cards_container = QWidget()
        self.grid_layout = QGridLayout(self.cards_container)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(15)
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
    
    def _load_notes(self):
        """Carga todas las notas desde la base de datos y las muestra como tarjetas."""
        notes = self.controller.get_all_notes()
        
        # Limpiar tarjetas existentes
        self._clear_cards()
        
        # Agregar cada nota como tarjeta
        for note in notes:
            self._add_note_card(note)
    
    def _add_note_card(self, note_data: dict):
        """
        Agrega una tarjeta de nota al grid.
        
        Args:
            note_data: Diccionario con los datos de la nota
        """
        note_id = note_data.get('id')
        
        # Si la tarjeta ya existe, actualizarla
        if note_id in self.note_cards:
            self.note_cards[note_id].update_data(note_data)
            return
        
        # Crear nueva tarjeta
        card = NoteCard(note_data, self.cards_container)
        
        # Conectar señales
        card.edit_requested.connect(self._on_edit_note_requested)
        card.delete_requested.connect(self._on_delete_note_requested)
        
        # Calcular posición en el grid (3 columnas)
        row = len(self.note_cards) // 3
        col = len(self.note_cards) % 3
        
        self.grid_layout.addWidget(card, row, col)
        
        # Guardar referencia
        self.note_cards[note_id] = card
    
    def _remove_note_card(self, note_id: int):
        """
        Elimina una tarjeta de nota del grid.
        
        Args:
            note_id: ID de la nota a eliminar
        """
        if note_id in self.note_cards:
            card = self.note_cards[note_id]
            self.grid_layout.removeWidget(card)
            card.setParent(None)
            card.deleteLater()
            del self.note_cards[note_id]
            
            # Reorganizar las tarjetas restantes
            self._reorganize_cards()
    
    def _reorganize_cards(self):
        """Reorganiza las tarjetas en el grid después de eliminar una."""
        # Limpiar el layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Reagregar todas las tarjetas
        cards_list = list(self.note_cards.values())
        for idx, card in enumerate(cards_list):
            row = idx // 3
            col = idx % 3
            self.grid_layout.addWidget(card, row, col)
    
    def _clear_cards(self):
        """Elimina todas las tarjetas."""
        for note_id in list(self.note_cards.keys()):
            self._remove_note_card(note_id)
    
    def _on_add_note_requested(self):
        """Gestiona la solicitud de agregar una nueva nota."""
        dialog = NoteDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            note_data = dialog.get_note_data()
            note_id = self.controller.create_note(
                note_data['title'],
                note_data['content']
            )
            
            if note_id:
                # Obtener la nota completa desde la BD
                new_note = self.controller.get_note(note_id)
                if new_note:
                    self._add_note_card(new_note)
                    self._reorganize_cards()
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear la nota.")
    
    def _on_edit_note_requested(self, note_id: int):
        """
        Gestiona la solicitud de editar una nota.
        
        Args:
            note_id: ID de la nota a editar
        """
        note = self.controller.get_note(note_id)
        
        if not note:
            QMessageBox.warning(self, "Error", "No se pudo cargar la nota.")
            return
        
        dialog = NoteDialog(self, note)
        
        if dialog.exec_() == QDialog.Accepted:
            note_data = dialog.get_note_data()
            
            if self.controller.update_note(
                note_id,
                title=note_data['title'],
                content=note_data['content']
            ):
                # Obtener la nota actualizada
                updated_note = self.controller.get_note(note_id)
                
                if updated_note:
                    # Actualizar la tarjeta
                    self._add_note_card(updated_note)
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar la nota.")
    
    def _on_delete_note_requested(self, note_id: int):
        """
        Gestiona la solicitud de eliminar una nota.
        
        Args:
            note_id: ID de la nota a eliminar
        """
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar esta nota?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.controller.delete_note(note_id):
                self._remove_note_card(note_id)
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la nota.")
