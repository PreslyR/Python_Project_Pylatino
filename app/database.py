"""
Módulo de gestión de base de datos SQLite.
Maneja la conexión y creación de tablas.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional


class Database:
    """Clase para manejar la conexión y operaciones de la base de datos SQLite."""
    
    def __init__(self, db_path: str = "tasks.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establece la conexión con la base de datos."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
            print(f"✓ Conexión establecida con la base de datos: {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Error al conectar con la base de datos: {e}")
            raise
    
    def _create_tables(self):
        """Crea las tablas necesarias si no existen."""
        try:
            cursor = self.connection.cursor()
            
            # Tabla de tareas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL DEFAULT 'todo',
                    created_at TEXT NOT NULL,
                    due_date TEXT
                )
            """)
            
            # Agregar columna due_date si no existe (para bases de datos existentes)
            try:
                cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
                self.connection.commit()
                print("✓ Columna 'due_date' agregada a la tabla 'tasks'")
            except sqlite3.OperationalError:
                # La columna ya existe, no hacer nada
                pass
            
            # Tabla de notas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            self.connection.commit()
            print("✓ Tabla 'tasks' verificada/creada correctamente")
            print("✓ Tabla 'notes' verificada/creada correctamente")
        except sqlite3.Error as e:
            print(f"✗ Error al crear las tablas: {e}")
            raise
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Ejecuta una consulta SQL.
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (tupla)
            
        Returns:
            Cursor con el resultado de la consulta
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"✗ Error al ejecutar la consulta: {e}")
            self.connection.rollback()
            raise
    
    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """
        Ejecuta una consulta SELECT y retorna todos los resultados.
        
        Args:
            query: Consulta SQL SELECT
            params: Parámetros para la consulta (tupla)
            
        Returns:
            Lista de diccionarios con los resultados
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Convertir Row objects a diccionarios
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"✗ Error al obtener los resultados: {e}")
            raise
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[dict]:
        """
        Ejecuta una consulta SELECT y retorna un solo resultado.
        
        Args:
            query: Consulta SQL SELECT
            params: Parámetros para la consulta (tupla)
            
        Returns:
            Diccionario con el resultado o None si no hay resultados
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"✗ Error al obtener el resultado: {e}")
            raise
    
    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()
            print("✓ Conexión con la base de datos cerrada")


# Instancia global de la base de datos
db = Database()

