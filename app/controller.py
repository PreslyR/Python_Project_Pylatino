"""
Módulo controlador.
Puente entre la UI y los modelos de datos.
"""

from typing import List, Dict, Optional
from app.models import TaskModel


class TaskController:
    """Controlador para gestionar las operaciones de tareas."""
    
    def __init__(self):
        """Inicializa el controlador."""
        self.model = TaskModel
    
    def create_task(self, title: str, description: str = "", 
                    status: str = TaskModel.STATUS_TODO, due_date: str = None) -> Optional[int]:
        """
        Crea una nueva tarea.
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea
            status: Estado inicial de la tarea
            due_date: Fecha programada/vencimiento en formato ISO (opcional)
            
        Returns:
            ID de la tarea creada o None si hubo un error
        """
        if not title or not title.strip():
            return None
        
        try:
            task_id = self.model.create(title.strip(), description.strip(), status, due_date)
            return task_id
        except Exception as e:
            print(f"✗ Error al crear la tarea: {e}")
            return None
    
    def get_all_tasks(self) -> List[Dict]:
        """
        Obtiene todas las tareas.
        
        Returns:
            Lista de diccionarios con las tareas
        """
        try:
            return self.model.get_all()
        except Exception as e:
            print(f"✗ Error al obtener las tareas: {e}")
            return []
    
    def get_tasks_by_status(self, status: str) -> List[Dict]:
        """
        Obtiene las tareas filtradas por estado.
        
        Args:
            status: Estado de las tareas a buscar
            
        Returns:
            Lista de diccionarios con las tareas
        """
        try:
            return self.model.get_by_status(status)
        except Exception as e:
            print(f"✗ Error al obtener las tareas por estado: {e}")
            return []
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            Diccionario con los datos de la tarea o None
        """
        try:
            return self.model.get_by_id(task_id)
        except Exception as e:
            print(f"✗ Error al obtener la tarea: {e}")
            return None
    
    def update_task(self, task_id: int, title: str = None, 
                   description: str = None, status: str = None, due_date: str = None) -> bool:
        """
        Actualiza una tarea.
        
        Args:
            task_id: ID de la tarea a actualizar
            title: Nuevo título (opcional)
            description: Nueva descripción (opcional)
            status: Nuevo estado (opcional)
            due_date: Nueva fecha programada/vencimiento en formato ISO (opcional)
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        try:
            return self.model.update(task_id, title, description, status, due_date)
        except Exception as e:
            print(f"✗ Error al actualizar la tarea: {e}")
            return False
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """
        Actualiza el estado de una tarea.
        
        Args:
            task_id: ID de la tarea
            status: Nuevo estado
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        try:
            return self.model.update_status(task_id, status)
        except Exception as e:
            print(f"✗ Error al actualizar el estado de la tarea: {e}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Elimina una tarea.
        
        Args:
            task_id: ID de la tarea a eliminar
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        try:
            return self.model.delete(task_id)
        except Exception as e:
            print(f"✗ Error al eliminar la tarea: {e}")
            return False
    
    def get_tasks_by_due_date(self, due_date: str) -> List[Dict]:
        """
        Obtiene las tareas con una fecha de vencimiento específica.
        
        Args:
            due_date: Fecha en formato ISO (YYYY-MM-DD)
            
        Returns:
            Lista de diccionarios con las tareas
        """
        try:
            return self.model.get_by_due_date(due_date)
        except Exception as e:
            print(f"✗ Error al obtener las tareas por fecha: {e}")
            return []
    
    def get_tasks_with_due_dates(self) -> List[Dict]:
        """
        Obtiene todas las tareas que tienen una fecha de vencimiento asignada.
        
        Returns:
            Lista de diccionarios con las tareas
        """
        try:
            return self.model.get_tasks_with_due_dates()
        except Exception as e:
            print(f"✗ Error al obtener las tareas con fechas: {e}")
            return []

