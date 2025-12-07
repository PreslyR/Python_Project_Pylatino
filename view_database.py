"""
Script para visualizar el contenido de la base de datos.
Útil para pruebas y depuración.
"""

import sqlite3
from datetime import datetime


def show_database_info(db_path="tasks.db"):
    """Muestra información completa de la base de datos."""
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("=" * 70)
        print("VISUALIZADOR DE BASE DE DATOS - TASKS.DB")
        print("=" * 70)
        
        # 1. Mostrar todas las tablas
        print("\n📋 TABLAS EN LA BASE DE DATOS:")
        print("-" * 70)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            print("   No hay tablas en la base de datos.")
        else:
            for table in tables:
                table_name = table['name']
                print(f"\n   ✓ {table_name}")
                
                # Mostrar estructura de la tabla
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                print(f"      Columnas:")
                for col in columns:
                    col_name = col['name']
                    col_type = col['type']
                    col_notnull = "NOT NULL" if col['notnull'] else "NULL"
                    col_pk = "PRIMARY KEY" if col['pk'] else ""
                    default = f"DEFAULT {col['dflt_value']}" if col['dflt_value'] else ""
                    
                    print(f"        - {col_name} ({col_type}) {col_notnull} {col_pk} {default}")
        
        # 2. Mostrar el contenido de cada tabla
        print("\n" + "=" * 70)
        print("📊 CONTENIDO DE LAS TABLAS:")
        print("=" * 70)
        
        for table in tables:
            table_name = table['name']
            print(f"\n📌 TABLA: {table_name}")
            print("-" * 70)
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"   Total de registros: {count}")
            
            if count == 0:
                print("   (La tabla está vacía)")
            else:
                # Obtener todos los registros
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                # Mostrar encabezados
                if rows:
                    headers = [description[0] for description in cursor.description]
                    print(f"\n   {' | '.join(headers)}")
                    print("   " + "-" * 68)
                    
                    # Mostrar cada fila
                    for row in rows:
                        values = []
                        for header in headers:
                            value = row[header]
                            # Formatear valores
                            if value is None:
                                values.append("NULL")
                            elif isinstance(value, str) and len(value) > 30:
                                values.append(value[:27] + "...")
                            else:
                                values.append(str(value))
                        print(f"   {' | '.join(values)}")
        
        # 3. Mostrar estadísticas específicas para la tabla tasks
        if any(t['name'] == 'tasks' for t in tables):
            print("\n" + "=" * 70)
            print("📈 ESTADÍSTICAS DE TAREAS:")
            print("=" * 70)
            
            cursor.execute("""
                SELECT 
                    status,
                    COUNT(*) as cantidad
                FROM tasks
                GROUP BY status
            """)
            
            stats = cursor.fetchall()
            if stats:
                print("\n   Tareas por estado:")
                for stat in stats:
                    status = stat['status']
                    cantidad = stat['cantidad']
                    print(f"     - {status}: {cantidad} tarea(s)")
            
            cursor.execute("SELECT COUNT(*) as total FROM tasks")
            total = cursor.fetchone()['total']
            print(f"\n   Total de tareas: {total}")
        
        print("\n" + "=" * 70)
        print("✅ Visualización completada")
        print("=" * 70)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"\n❌ Error al acceder a la base de datos: {e}")
    except FileNotFoundError:
        print(f"\n❌ No se encontró el archivo de base de datos: {db_path}")
        print("   Asegúrate de haber ejecutado la aplicación al menos una vez.")


def show_tasks_table(db_path="tasks.db"):
    """Muestra solo la tabla de tareas de forma más detallada."""
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("=" * 80)
        print("TAREAS EN LA BASE DE DATOS")
        print("=" * 80)
        
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        
        if not tasks:
            print("\n   No hay tareas en la base de datos.")
        else:
            print(f"\n   Total: {len(tasks)} tarea(s)\n")
            
            for idx, task in enumerate(tasks, 1):
                print(f"┌─ TAREA #{task['id']} ─" + "─" * 60)
                print(f"│")
                print(f"│  Título:      {task['title']}")
                print(f"│  Descripción: {task['description'] or '(sin descripción)'}")
                print(f"│  Estado:      {task['status'].upper()}")
                
                # Formatear fecha
                try:
                    created_at = datetime.fromisoformat(task['created_at'])
                    fecha_formateada = created_at.strftime("%d/%m/%Y %H:%M:%S")
                    print(f"│  Creada:      {fecha_formateada}")
                except:
                    print(f"│  Creada:      {task['created_at']}")
                
                print(f"│")
                
                if idx < len(tasks):
                    print(f"├" + "─" * 68)
                else:
                    print(f"└" + "─" * 68)
                print()
        
        print("=" * 80)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"\n❌ Error: {e}")
    except FileNotFoundError:
        print(f"\n❌ No se encontró el archivo: {db_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--tasks":
        # Mostrar solo la tabla de tareas de forma detallada
        show_tasks_table()
    else:
        # Mostrar información completa de la base de datos
        show_database_info()

