"""
Componente Sidebar.
Barra lateral de navegación con botones para cambiar entre vistas.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal


class Sidebar(QWidget):
    """Barra lateral de navegación con botones para cambiar entre vistas."""
    
    # Señal emitida cuando se selecciona una vista
    view_changed = pyqtSignal(str)  # nombre de la vista: "kanban", "notepad", "stats", "calendar"
    
    def __init__(self, parent=None):
        """
        Inicializa el sidebar.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        self.current_button = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz del sidebar."""
        # Layout principal vertical
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        
        # Título del sidebar (opcional)
        # Puedes agregar un logo o título aquí si quieres
        
        # Espaciador superior
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Botón: Tablero Kanban
        self.kanban_button = QPushButton("📋 Tablero Kanban")
        self.kanban_button.setObjectName("sidebarButton")
        self.kanban_button.setCheckable(True)
        self.kanban_button.setChecked(True)  # Vista por defecto
        self.kanban_button.clicked.connect(lambda: self._on_button_clicked("kanban", self.kanban_button))
        layout.addWidget(self.kanban_button)
        
        # Botón: Bloc de notas
        self.notepad_button = QPushButton("📝 Bloc de notas")
        self.notepad_button.setObjectName("sidebarButton")
        self.notepad_button.setCheckable(True)
        self.notepad_button.clicked.connect(lambda: self._on_button_clicked("notepad", self.notepad_button))
        layout.addWidget(self.notepad_button)
        
        # Botón: Estadísticas
        self.stats_button = QPushButton("📊 Estadísticas")
        self.stats_button.setObjectName("sidebarButton")
        self.stats_button.setCheckable(True)
        self.stats_button.clicked.connect(lambda: self._on_button_clicked("stats", self.stats_button))
        layout.addWidget(self.stats_button)
        
        # Botón: Calendario
        self.calendar_button = QPushButton("📅 Calendario")
        self.calendar_button.setObjectName("sidebarButton")
        self.calendar_button.setCheckable(True)
        self.calendar_button.clicked.connect(lambda: self._on_button_clicked("calendar", self.calendar_button))
        layout.addWidget(self.calendar_button)
        
        # Espaciador para empujar los botones hacia arriba
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Establecer el ancho fijo del sidebar
        self.setFixedWidth(220)
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def _on_button_clicked(self, view_name: str, button: QPushButton):
        """
        Gestiona el clic en un botón del sidebar.
        
        Args:
            view_name: Nombre de la vista a mostrar
            button: Botón que fue presionado
        """
        # Desmarcar el botón anterior
        if self.current_button and self.current_button != button:
            self.current_button.setChecked(False)
        
        # Marcar el nuevo botón
        button.setChecked(True)
        self.current_button = button
        
        # Emitir señal para cambiar la vista
        self.view_changed.emit(view_name)
    
    def set_current_view(self, view_name: str):
        """
        Establece la vista actual programáticamente.
        
        Args:
            view_name: Nombre de la vista ("kanban", "notepad", "stats")
        """
        buttons_map = {
            "kanban": self.kanban_button,
            "notepad": self.notepad_button,
            "stats": self.stats_button,
            "calendar": self.calendar_button
        }
        
        button = buttons_map.get(view_name)
        if button:
            self._on_button_clicked(view_name, button)

