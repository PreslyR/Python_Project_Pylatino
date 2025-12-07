"""
Ventana principal de la aplicación.
Contiene el sidebar de navegación y el QStackedWidget con las diferentes vistas.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                             QDialog, QVBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QMessageBox,
                             QStackedWidget, QDateEdit, QCheckBox)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime
from ui.sidebar import Sidebar
from ui.kanban_view import KanbanView
from ui.notepad_view import NotepadView
from ui.stats_view import StatsView
from ui.calendar_view import CalendarView
from app.controller import TaskController


class TaskDialog(QDialog):
    """Diálogo para crear o editar una tarea."""
    
    def __init__(self, parent=None, task_data=None):
        """
        Inicializa el diálogo.
        
        Args:
            parent: Widget padre
            task_data: Diccionario con los datos de la tarea si se está editando, None si es nueva
        """
        super().__init__(parent)
        self.task_data = task_data
        self.is_editing = task_data is not None
        
        title = "Editar Tarea" if self.is_editing else "Nueva Tarea"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self._setup_ui()
        
        if self.is_editing:
            self._load_task_data()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Título:")
        layout.addWidget(title_label)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Ingrese el título de la tarea...")
        layout.addWidget(self.title_edit)
        
        # Descripción
        description_label = QLabel("Descripción:")
        layout.addWidget(description_label)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Ingrese la descripción de la tarea...")
        self.description_edit.setMaximumHeight(150)
        layout.addWidget(self.description_edit)
        
        # Fecha programada/vencimiento
        date_layout = QHBoxLayout()
        
        self.date_checkbox = QCheckBox("Programar fecha:")
        self.date_checkbox.toggled.connect(self._on_date_checkbox_toggled)
        date_layout.addWidget(self.date_checkbox)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setEnabled(False)
        date_layout.addWidget(self.date_edit)
        
        date_layout.addStretch()
        layout.addLayout(date_layout)
        
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
    
    def _on_date_checkbox_toggled(self, checked):
        """Habilita/deshabilita el selector de fecha."""
        self.date_edit.setEnabled(checked)
    
    def _load_task_data(self):
        """Carga los datos de la tarea en los campos del formulario."""
        if self.task_data:
            self.title_edit.setText(self.task_data.get('title', ''))
            self.description_edit.setPlainText(self.task_data.get('description', ''))
            
            # Cargar fecha si existe
            due_date = self.task_data.get('due_date')
            if due_date:
                try:
                    # Convertir ISO string a QDate
                    date_obj = datetime.fromisoformat(due_date)
                    qdate = QDate(date_obj.year, date_obj.month, date_obj.day)
                    self.date_edit.setDate(qdate)
                    self.date_checkbox.setChecked(True)
                    self.date_edit.setEnabled(True)
                except (ValueError, TypeError):
                    pass
    
    def _validate_and_accept(self):
        """Valida los datos antes de cerrar el diálogo."""
        title = self.title_edit.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "El título de la tarea es obligatorio.")
            return
        
        self.accept()
    
    def get_task_data(self) -> dict:
        """
        Retorna los datos ingresados en el formulario.
        
        Returns:
            Diccionario con title, description y due_date
        """
        due_date = None
        if self.date_checkbox.isChecked():
            qdate = self.date_edit.date()
            # Convertir QDate a ISO string (solo fecha, sin hora)
            due_date = f"{qdate.year()}-{qdate.month():02d}-{qdate.day():02d}"
        
        return {
            'title': self.title_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'due_date': due_date
        }


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación con sidebar y múltiples vistas."""
    
    def __init__(self):
        """Inicializa la ventana principal."""
        super().__init__()
        self.controller = TaskController()
        
        self.setWindowTitle("Organizador de Tareas - Kanban")
        self.setGeometry(100, 100, 1400, 800)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de la ventana principal."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout horizontal principal (sidebar + stacked widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear y agregar el sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.view_changed.connect(self._on_view_changed)
        main_layout.addWidget(self.sidebar)
        
        # Crear el QStackedWidget para las vistas
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("stackedWidget")
        main_layout.addWidget(self.stacked_widget)
        
        # Crear las vistas
        self._create_views()
        
        # Establecer la vista inicial (Kanban)
        self.stacked_widget.setCurrentWidget(self.kanban_view)
    
    def _create_views(self):
        """Crea todas las vistas y las agrega al QStackedWidget."""
        # Vista del Tablero Kanban
        self.kanban_view = KanbanView(self.controller, self)
        self.kanban_view.connect_signals(
            self._on_add_task_requested,
            self._on_task_moved,
            self._on_edit_task_requested,
            self._on_delete_task_requested
        )
        self.stacked_widget.addWidget(self.kanban_view)
        
        # Vista del Bloc de Notas
        self.notepad_view = NotepadView(self)
        self.stacked_widget.addWidget(self.notepad_view)
        
        # Vista de Estadísticas
        self.stats_view = StatsView(self.controller, self)
        self.stacked_widget.addWidget(self.stats_view)
        
        # Vista de Calendario
        self.calendar_view = CalendarView(self.controller, self)
        self.calendar_view.connect_signals(
            self._on_edit_task_requested,
            self._on_delete_task_requested
        )
        self.stacked_widget.addWidget(self.calendar_view)
        
        # Guardar referencias para acceso rápido
        self.views = {
            "kanban": 0,
            "notepad": 1,
            "stats": 2,
            "calendar": 3
        }
    
    def _on_view_changed(self, view_name: str):
        """
        Gestiona el cambio de vista desde el sidebar.
        
        Args:
            view_name: Nombre de la vista a mostrar ("kanban", "notepad", "stats")
        """
        index = self.views.get(view_name, 0)
        self.stacked_widget.setCurrentIndex(index)
        
        # Si se cambia a estadísticas, actualizar los datos
        if view_name == "stats":
            self.stats_view._update_stats()
        # Si se cambia a calendario, actualizar las tareas
        elif view_name == "calendar":
            self.calendar_view.refresh_tasks()
    
    # ==================== MÉTODOS DE GESTIÓN DE TAREAS ====================
    # Estos métodos mantienen la funcionalidad original del Kanban intacta
    
    def _on_add_task_requested(self, status: str):
        """
        Gestiona la solicitud de agregar una nueva tarea.
        
        Args:
            status: Estado inicial de la nueva tarea
        """
        dialog = TaskDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            task_id = self.controller.create_task(
                task_data['title'],
                task_data['description'],
                status,
                task_data.get('due_date')
            )
            
            if task_id:
                # Obtener la tarea completa desde la BD
                new_task = self.controller.get_task(task_id)
                if new_task:
                    # Agregar a la vista Kanban
                    kanban_columns = self.kanban_view.columns
                    if status in kanban_columns:
                        kanban_columns[status].add_task_card(new_task)
                    
                    # Actualizar estadísticas si está visible
                    if self.stacked_widget.currentWidget() == self.stats_view:
                        self.stats_view._update_stats()
                    # Actualizar calendario si está visible
                    elif self.stacked_widget.currentWidget() == self.calendar_view:
                        self.calendar_view.refresh_tasks()
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear la tarea.")
    
    def _on_task_moved(self, task_id: int, new_status: str):
        """
        Gestiona el movimiento de una tarea a otra columna.
        
        Args:
            task_id: ID de la tarea movida
            new_status: Nuevo estado de la tarea
        """
        # Obtener las columnas del Kanban
        kanban_columns = self.kanban_view.columns
        
        # Buscar la tarjeta en todas las columnas
        task_card = None
        old_status = None
        
        for status, column in kanban_columns.items():
            card = column.get_task_card(task_id)
            if card:
                task_card = card
                old_status = status
                break
        
        if not task_card:
            return
        
        # Actualizar el estado en la base de datos
        if self.controller.update_task_status(task_id, new_status):
            # Obtener la tarea actualizada
            updated_task = self.controller.get_task(task_id)
            
            if updated_task:
                # Remover de la columna antigua
                if old_status and old_status in kanban_columns:
                    kanban_columns[old_status].remove_task_card(task_id)
                
                # Agregar a la nueva columna
                if new_status in kanban_columns:
                    kanban_columns[new_status].add_task_card(updated_task)
                
                # Actualizar estadísticas si está visible
                if self.stacked_widget.currentWidget() == self.stats_view:
                    self.stats_view._update_stats()
                # Actualizar calendario si está visible (por si cambia la fecha)
                elif self.stacked_widget.currentWidget() == self.calendar_view:
                    self.calendar_view.refresh_tasks()
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el estado de la tarea.")
    
    def _on_edit_task_requested(self, task_id: int):
        """
        Gestiona la solicitud de editar una tarea.
        
        Args:
            task_id: ID de la tarea a editar
        """
        task = self.controller.get_task(task_id)
        
        if not task:
            QMessageBox.warning(self, "Error", "No se pudo cargar la tarea.")
            return
        
        dialog = TaskDialog(self, task)
        
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            
            if self.controller.update_task(
                task_id,
                title=task_data['title'],
                description=task_data['description'],
                due_date=task_data.get('due_date')
            ):
                # Obtener la tarea actualizada
                updated_task = self.controller.get_task(task_id)
                
                if updated_task:
                    # Actualizar la tarjeta en la columna correspondiente
                    status = updated_task.get('status', 'todo')
                    kanban_columns = self.kanban_view.columns
                    if status in kanban_columns:
                        kanban_columns[status].add_task_card(updated_task)
                    
                    # Actualizar calendario si está visible
                    if self.stacked_widget.currentWidget() == self.calendar_view:
                        self.calendar_view.refresh_tasks()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar la tarea.")
    
    def _on_delete_task_requested(self, task_id: int):
        """
        Gestiona la solicitud de eliminar una tarea.
        
        Args:
            task_id: ID de la tarea a eliminar
        """
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar esta tarea?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Buscar la tarjeta en todas las columnas para obtener su estado
            kanban_columns = self.kanban_view.columns
            task_status = None
            
            for status, column in kanban_columns.items():
                if column.get_task_card(task_id):
                    task_status = status
                    break
            
            if self.controller.delete_task(task_id):
                # Remover la tarjeta de la columna
                if task_status and task_status in kanban_columns:
                    kanban_columns[task_status].remove_task_card(task_id)
                
                # Actualizar estadísticas si está visible
                if self.stacked_widget.currentWidget() == self.stats_view:
                    self.stats_view._update_stats()
                # Actualizar calendario si está visible
                elif self.stacked_widget.currentWidget() == self.calendar_view:
                    self.calendar_view.refresh_tasks()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la tarea.")
