"""
Módulo de modelo de notas.
Define la clase NoteModel para gestionar las notas.
"""

from datetime import datetime
from typing import List, Optional, Dict
from app.database import db


class NoteModel:
    """Modelo para gestionar las notas en la base de datos."""
    
    @staticmethod
    def create(title: str, content: str = "") -> int:
        """
        Crea una nueva nota en la base de datos.
        
        Args:
            title: Título de la nota
            content: Contenido de la nota
            
        Returns:
            ID de la nota creada
        """
        created_at = datetime.now().isoformat()
        updated_at = created_at
        
        query = """
            INSERT INTO notes (title, content, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """
        params = (title, content, created_at, updated_at)
        
        cursor = db.execute(query, params)
        return cursor.lastrowid
    
    @staticmethod
    def get_all() -> List[Dict]:
        """
        Obtiene todas las notas de la base de datos.
        
        Returns:
            Lista de diccionarios con las notas
        """
        query = "SELECT * FROM notes ORDER BY updated_at DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(note_id: int) -> Optional[Dict]:
        """
        Obtiene una nota por su ID.
        
        Args:
            note_id: ID de la nota
            
        Returns:
            Diccionario con los datos de la nota o None si no existe
        """
        query = "SELECT * FROM notes WHERE id = ?"
        return db.fetch_one(query, (note_id,))
    
    @staticmethod
    def update(note_id: int, title: str = None, content: str = None) -> bool:
        """
        Actualiza una nota existente.
        
        Args:
            note_id: ID de la nota a actualizar
            title: Nuevo título (opcional)
            content: Nuevo contenido (opcional)
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        
        if not updates:
            return False
        
        # Siempre actualizar updated_at
        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        
        params.append(note_id)
        query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
        
        try:
            db.execute(query, tuple(params))
            return True
        except Exception as e:
            print(f"✗ Error al actualizar la nota: {e}")
            return False
    
    @staticmethod
    def delete(note_id: int) -> bool:
        """
        Elimina una nota de la base de datos.
        
        Args:
            note_id: ID de la nota a eliminar
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        query = "DELETE FROM notes WHERE id = ?"
        
        try:
            db.execute(query, (note_id,))
            return True
        except Exception as e:
            print(f"✗ Error al eliminar la nota: {e}")
            return False

