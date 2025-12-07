"""
Módulo controlador de notas.
Puente entre la UI y los modelos de notas.
"""

from typing import List, Dict, Optional
from app.note_model import NoteModel


class NoteController:
    """Controlador para gestionar las operaciones de notas."""
    
    def __init__(self):
        """Inicializa el controlador."""
        self.model = NoteModel
    
    def create_note(self, title: str, content: str = "") -> Optional[int]:
        """
        Crea una nueva nota.
        
        Args:
            title: Título de la nota
            content: Contenido de la nota
            
        Returns:
            ID de la nota creada o None si hubo un error
        """
        if not title or not title.strip():
            return None
        
        try:
            note_id = self.model.create(title.strip(), content.strip())
            return note_id
        except Exception as e:
            print(f"✗ Error al crear la nota: {e}")
            return None
    
    def get_all_notes(self) -> List[Dict]:
        """
        Obtiene todas las notas.
        
        Returns:
            Lista de diccionarios con las notas
        """
        try:
            return self.model.get_all()
        except Exception as e:
            print(f"✗ Error al obtener las notas: {e}")
            return []
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """
        Obtiene una nota por su ID.
        
        Args:
            note_id: ID de la nota
            
        Returns:
            Diccionario con los datos de la nota o None
        """
        try:
            return self.model.get_by_id(note_id)
        except Exception as e:
            print(f"✗ Error al obtener la nota: {e}")
            return None
    
    def update_note(self, note_id: int, title: str = None, content: str = None) -> bool:
        """
        Actualiza una nota.
        
        Args:
            note_id: ID de la nota a actualizar
            title: Nuevo título (opcional)
            content: Nuevo contenido (opcional)
            
        Returns:
            True si la actualización fue exitosa, False en caso contrario
        """
        try:
            return self.model.update(note_id, title, content)
        except Exception as e:
            print(f"✗ Error al actualizar la nota: {e}")
            return False
    
    def delete_note(self, note_id: int) -> bool:
        """
        Elimina una nota.
        
        Args:
            note_id: ID de la nota a eliminar
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        try:
            return self.model.delete(note_id)
        except Exception as e:
            print(f"✗ Error al eliminar la nota: {e}")
            return False

