"""
Vista de Calendario.
Muestra un calendario con las tareas programadas por día.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QScrollArea, QListWidget,
                             QListWidgetItem, QCalendarWidget, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QTextCharFormat, QColor, QBrush
from datetime import datetime
from ui.task_card import TaskCard
from app.controller import TaskController


class CalendarView(QWidget):
    """Vista de calendario que muestra las tareas programadas por día."""
    
    def __init__(self, controller: TaskController, parent=None):
        """
        Inicializa la vista de calendario.
        
        Args:
            controller: Controlador de tareas
            parent: Widget padre
        """
        super().__init__(parent)
        self.controller = controller
        self.tasks_by_date = {}  # Diccionario {fecha_iso: [lista de tareas]}
        self.task_cards = {}  # Diccionario {task_id: TaskCard}
        
        self._setup_ui()
        self._load_tasks()
        self._update_calendar()
    
    def _setup_ui(self):
        """Configura la interfaz de la vista de calendario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("📅 Calendario de Tareas")
        title_label.setObjectName("calendarTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Layout horizontal: Calendario + Lista de tareas
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        
        # Calendario (izquierda)
        calendar_container = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self._on_date_selected)
        calendar_container.addWidget(self.calendar)
        
        # Botón para hoy
        today_button = QPushButton("Hoy")
        today_button.setObjectName("calendarButton")
        today_button.clicked.connect(self._go_to_today)
        calendar_container.addWidget(today_button)
        
        main_layout.addLayout(calendar_container, 1)
        
        # Lista de tareas del día seleccionado (derecha)
        tasks_container = QVBoxLayout()
        
        date_label_layout = QHBoxLayout()
        self.selected_date_label = QLabel("Seleccione una fecha")
        self.selected_date_label.setObjectName("calendarDateLabel")
        date_label_layout.addWidget(self.selected_date_label)
        date_label_layout.addStretch()
        tasks_container.addLayout(date_label_layout)
        
        # Área scrollable para las tareas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        # Widget contenedor para las tarjetas
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setContentsMargins(5, 5, 5, 5)
        self.tasks_layout.setSpacing(10)
        self.tasks_layout.addStretch()
        
        scroll_area.setWidget(self.tasks_container)
        tasks_container.addWidget(scroll_area)
        
        main_layout.addLayout(tasks_container, 2)
        
        layout.addLayout(main_layout)
        
        # Seleccionar fecha actual por defecto
        self._go_to_today()
    
    def _load_tasks(self):
        """Carga todas las tareas con fechas programadas."""
        tasks = self.controller.get_tasks_with_due_dates()
        
        self.tasks_by_date = {}
        
        for task in tasks:
            due_date = task.get('due_date')
            if due_date:
                # Extraer solo la fecha (sin hora) del ISO string
                try:
                    if 'T' in due_date:
                        date_str = due_date.split('T')[0]
                    else:
                        date_str = due_date
                    
                    if date_str not in self.tasks_by_date:
                        self.tasks_by_date[date_str] = []
                    
                    self.tasks_by_date[date_str].append(task)
                except Exception as e:
                    print(f"Error al procesar fecha {due_date}: {e}")
    
    def _update_calendar(self):
        """Actualiza el calendario para resaltar los días con tareas."""
        # Formato para días con tareas
        format_with_tasks = QTextCharFormat()
        format_with_tasks.setBackground(QBrush(QColor(156, 39, 176, 100)))  # Morado claro
        format_with_tasks.setForeground(QBrush(QColor(255, 255, 255)))
        
        # Aplicar formato a los días con tareas
        for date_str in self.tasks_by_date.keys():
            try:
                year, month, day = map(int, date_str.split('-'))
                qdate = QDate(year, month, day)
                if qdate.isValid():
                    self.calendar.setDateTextFormat(qdate, format_with_tasks)
            except Exception as e:
                print(f"Error al formatear fecha {date_str}: {e}")
    
    def _on_date_selected(self):
        """Gestiona la selección de una fecha en el calendario."""
        selected_date = self.calendar.selectedDate()
        date_str = f"{selected_date.year()}-{selected_date.month():02d}-{selected_date.day():02d}"
        
        # Actualizar etiqueta de fecha
        date_formatted = selected_date.toString("dddd, dd 'de' MMMM 'de' yyyy")
        self.selected_date_label.setText(f"Tareas para: {date_formatted}")
        
        # Mostrar tareas del día seleccionado
        self._show_tasks_for_date(date_str)
    
    def _show_tasks_for_date(self, date_str: str):
        """Muestra las tareas para una fecha específica."""
        # Limpiar tareas actuales
        self.task_cards.clear()
        while self.tasks_layout.count() > 1:  # Mantener el stretch
            item = self.tasks_layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
        
        # Obtener tareas para esta fecha
        tasks = self.tasks_by_date.get(date_str, [])
        
        if not tasks:
            no_tasks_label = QLabel("No hay tareas programadas para este día.")
            no_tasks_label.setAlignment(Qt.AlignCenter)
            no_tasks_label.setObjectName("calendarNoTasksLabel")
            self.tasks_layout.insertWidget(0, no_tasks_label)
        else:
            # Mostrar cada tarea como una tarjeta
            for task in tasks:
                task_id = task.get('id')
                card = TaskCard(task, self.tasks_container)
                
                # Conectar señales si existen los handlers
                if hasattr(self, 'edit_handler'):
                    card.edit_requested.connect(self.edit_handler)
                if hasattr(self, 'delete_handler'):
                    card.delete_requested.connect(self.delete_handler)
                
                self.task_cards[task_id] = card
                self.tasks_layout.insertWidget(self.tasks_layout.count() - 1, card)
    
    def _go_to_today(self):
        """Selecciona la fecha de hoy en el calendario."""
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self._on_date_selected()
    
    def connect_signals(self, edit_task_handler, delete_task_handler):
        """
        Conecta las señales de las tarjetas con los manejadores de la ventana principal.
        
        Args:
            edit_task_handler: Función para manejar editar tarea
            delete_task_handler: Función para manejar eliminar tarea
        """
        self.edit_handler = edit_task_handler
        self.delete_handler = delete_task_handler
    
    def refresh_tasks(self):
        """Recarga las tareas y actualiza el calendario."""
        self.task_cards.clear()
        self._load_tasks()
        self._update_calendar()
        # Actualizar la vista del día seleccionado
        selected_date = self.calendar.selectedDate()
        date_str = f"{selected_date.year()}-{selected_date.month():02d}-{selected_date.day():02d}"
        self._show_tasks_for_date(date_str)
    
    def showEvent(self, event):
        """Evento que se ejecuta cuando la vista se muestra."""
        super().showEvent(event)
        # Actualizar tareas cada vez que se muestra la vista
        self.refresh_tasks()

