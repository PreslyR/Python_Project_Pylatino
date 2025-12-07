"""
Módulo de modelos de datos.
Define la clase TaskModel para gestionar las tareas.
"""

from datetime import datetime
from typing import List, Optional, Dict
from app.database import db


class TaskModel:
    """Modelo para gestionar las tareas en la base de datos."""
    
    STATUS_TODO = "todo"
    STATUS_DOING = "doing"
    STATUS_DONE = "done"
    
    VALID_STATUSES = [STATUS_TODO, STATUS_DOING, STATUS_DONE]
    
    @staticmethod
    def create(title: str, description: str = "", status: str = STATUS_TODO, due_date: str = None) -> int:
        """
        Crea una nueva tarea en la base de datos.
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea
            status: Estado inicial de la tarea (por defecto: "todo")
            due_date: Fecha programada/vencimiento en formato ISO (opcional)
            
        Returns:
            ID de la tarea creada
        """
        if status not in TaskModel.VALID_STATUSES:
            status = TaskModel.STATUS_TODO
        
        created_at = datetime.now().isoformat()
        
        query = """
            INSERT INTO tasks (title, description, status, created_at, due_date)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (title, description, status, created_at, due_date)
        
        cursor = db.execute(query, params)
        return cursor.lastrowid
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Obtiene todas las tareas de la base de datos.
        
        Returns:
            Lista de diccionarios con las tareas
        """
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(task_id: int) -> Optional[Dict]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            Diccionario con los datos de la tarea o None si no existe
        """
        query = "SELECT * FROM tasks WHERE id = ?"
        return db.fetch_one(query, (task_id,))
    
    @staticmethod
    def get_by_status(status: str) -> List[Dict]:
        """
        Obtiene todas las tareas con un estado específico.
        
        Args:
            status: Estado de las tareas a buscar
            
        Returns:
            Lista de diccionarios con las tareas
        """
        query = "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC"
        return db.fetch_all(query, (status,))
    
    @staticmethod
    def update(task_id: int, title: str = None, description: str = None, 
               status: str = None, due_date: str = None) -> bool:
        """
        Actualiza una tarea existente.
        
        Args:
            task_id: ID de la tarea a actualizar
            title: Nuevo título (opcional)
            description: Nueva descripción (opcional)
            status: Nuevo estado (opcional)
            due_date: Nueva fecha programada/vencimiento en formato ISO (opcional)
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        # Construir la consulta dinámicamente basándose en los campos proporcionados
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if status is not None:
            if status in TaskModel.VALID_STATUSES:
                updates.append("status = ?")
                params.append(status)
        
        if due_date is not None:
            updates.append("due_date = ?")
            params.append(due_date)
        
        if not updates:
            return False
        
        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        
        try:
            db.execute(query, tuple(params))
            return True
        except Exception as e:
            print(f"✗ Error al actualizar la tarea: {e}")
            return False
    
    @staticmethod
    def update_status(task_id: int, status: str) -> bool:
        """
        Actualiza solo el estado de una tarea.
        
        Args:
            task_id: ID de la tarea
            status: Nuevo estado
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        return TaskModel.update(task_id, status=status)
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """
        Elimina una tarea de la base de datos.
        
        Args:
            task_id: ID de la tarea a eliminar
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        query = "DELETE FROM tasks WHERE id = ?"
        
        try:
            db.execute(query, (task_id,))
            return True
        except Exception as e:
            print(f"✗ Error al eliminar la tarea: {e}")
            return False
    
    @staticmethod
    def get_by_due_date(due_date: str) -> List[Dict]:
        """
        Obtiene todas las tareas con una fecha de vencimiento específica.
        
        Args:
            due_date: Fecha en formato ISO (YYYY-MM-DD)
            
        Returns:
            Lista de diccionarios con las tareas
        """
        query = "SELECT * FROM tasks WHERE date(due_date) = date(?) ORDER BY created_at DESC"
        return db.fetch_all(query, (due_date,))
    
    @staticmethod
    def get_tasks_with_due_dates() -> List[Dict]:
        """
        Obtiene todas las tareas que tienen una fecha de vencimiento asignada.
        
        Returns:
            Lista de diccionarios con las tareas
        """
        query = "SELECT * FROM tasks WHERE due_date IS NOT NULL ORDER BY due_date ASC"
        return db.fetch_all(query)

