"""
Vista de Estadísticas.
Muestra estadísticas de las tareas con gráficos de barras.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from app.controller import TaskController


class StatsView(QWidget):
    """Vista que muestra estadísticas de las tareas con gráficos."""
    
    def __init__(self, controller: TaskController, parent=None):
        """
        Inicializa la vista de estadísticas.
        
        Args:
            controller: Controlador de tareas
            parent: Widget padre
        """
        super().__init__(parent)
        self.controller = controller
        
        self._setup_ui()
        self._update_stats()
    
    def _setup_ui(self):
        """Configura la interfaz de la vista de estadísticas."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        title_label = QLabel("📊 Estadísticas de Tareas")
        title_label.setObjectName("statsTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Panel de estadísticas (tarjetas con números)
        stats_panel = QHBoxLayout()
        stats_panel.setSpacing(15)
        
        # Tarjeta: Por Hacer
        self.todo_card = self._create_stat_card("Por Hacer", "0", "#2196F3")
        stats_panel.addWidget(self.todo_card)
        
        # Tarjeta: En Progreso
        self.doing_card = self._create_stat_card("En Progreso", "0", "#FF9800")
        stats_panel.addWidget(self.doing_card)
        
        # Tarjeta: Hecho
        self.done_card = self._create_stat_card("Hecho", "0", "#4CAF50")
        stats_panel.addWidget(self.done_card)
        
        # Tarjeta: Total
        self.total_card = self._create_stat_card("Total", "0", "#9C27B0")
        stats_panel.addWidget(self.total_card)
        
        layout.addLayout(stats_panel)
        
        # Botón de actualizar
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        
        self.refresh_button = QPushButton("🔄 Actualizar")
        self.refresh_button.setObjectName("statsRefreshButton")
        self.refresh_button.clicked.connect(self._update_stats)
        refresh_layout.addWidget(self.refresh_button)
        
        refresh_layout.addStretch()
        layout.addLayout(refresh_layout)
        
        # Gráfico de barras
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setObjectName("statsChart")
        layout.addWidget(self.canvas)
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """
        Crea una tarjeta de estadística.
        
        Args:
            title: Título de la tarjeta
            value: Valor a mostrar
            color: Color de la tarjeta (hex)
            
        Returns:
            QFrame configurado como tarjeta
        """
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
                min-height: 120px;
            }}
            QLabel {{
                color: white;
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            QLabel#statValue {
                font-size: 32px;
                font-weight: bold;
                color: white;
            }
        """)
        layout.addWidget(value_label)
        
        return card
    
    def _update_stats(self):
        """Actualiza las estadísticas y el gráfico."""
        # Obtener todas las tareas
        tasks = self.controller.get_all_tasks()
        
        # Contar por estado
        counts = {
            "todo": 0,
            "doing": 0,
            "done": 0
        }
        
        for task in tasks:
            status = task.get('status', 'todo')
            if status in counts:
                counts[status] += 1
        
        total = len(tasks)
        
        # Actualizar las tarjetas
        self._update_stat_card(self.todo_card, str(counts["todo"]))
        self._update_stat_card(self.doing_card, str(counts["doing"]))
        self._update_stat_card(self.done_card, str(counts["done"]))
        self._update_stat_card(self.total_card, str(total))
        
        # Actualizar el gráfico
        self._update_chart(counts)
    
    def _update_stat_card(self, card: QFrame, value: str):
        """
        Actualiza el valor en una tarjeta de estadística.
        
        Args:
            card: Tarjeta a actualizar
            value: Nuevo valor
        """
        layout = card.layout()
        if layout:
            # Buscar el label del valor (el segundo widget)
            if layout.count() >= 2:
                value_label = layout.itemAt(1).widget()
                if value_label:
                    value_label.setText(value)
    
    def _update_chart(self, counts: dict):
        """
        Actualiza el gráfico de barras con las estadísticas.
        
        Args:
            counts: Diccionario con los conteos por estado
        """
        # Limpiar el gráfico anterior
        self.figure.clear()
        
        # Crear el gráfico
        ax = self.figure.add_subplot(111)
        
        # Datos para el gráfico
        estados = ["Por Hacer", "En Progreso", "Hecho"]
        valores = [counts["todo"], counts["doing"], counts["done"]]
        colores = ["#2196F3", "#FF9800", "#4CAF50"]
        
        # Crear el gráfico de barras
        bars = ax.bar(estados, valores, color=colores, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Personalizar el gráfico
        ax.set_ylabel('Cantidad de Tareas', fontsize=12, fontweight='bold')
        ax.set_xlabel('Estado', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de Tareas por Estado', fontsize=14, fontweight='bold', pad=20)
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{valor}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Configurar el eje Y para mostrar solo números enteros
        ax.set_ylim(bottom=0)
        max_val = max(valores) if valores else 1
        ax.set_ylim(top=max(max_val + 1, 5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        # Agregar grid
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Ajustar el layout
        self.figure.tight_layout()
        
        # Actualizar el canvas
        self.canvas.draw()
    
    def showEvent(self, event):
        """Evento que se ejecuta cuando la vista se muestra."""
        super().showEvent(event)
        # Actualizar estadísticas cada vez que se muestra la vista
        self._update_stats()

