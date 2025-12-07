# 📊 Visualizador de Base de Datos

Este documento explica diferentes formas de ver y explorar la base de datos SQLite del proyecto.

## 🔧 Opción 1: Script Python (Recomendado)

### Ver información completa de la base de datos:
```bash
python view_database.py
```

### Ver solo la tabla de tareas de forma detallada:
```bash
python view_database.py --tasks
```

**Este script muestra:**
- ✅ Todas las tablas en la base de datos
- ✅ Estructura de cada tabla (columnas, tipos, restricciones)
- ✅ Contenido de todas las tablas
- ✅ Estadísticas de tareas por estado
- ✅ Información formateada y fácil de leer

## 💻 Opción 2: Usando sqlite3 desde la línea de comandos

### Abrir la base de datos:
```bash
sqlite3 tasks.db
```

### Comandos útiles en sqlite3:

```sql
-- Ver todas las tablas
.tables

-- Ver estructura de una tabla
.schema tasks

-- Ver todas las tareas
SELECT * FROM tasks;

-- Ver tareas con formato bonito
.headers on
.mode column
SELECT * FROM tasks;

-- Contar tareas por estado
SELECT status, COUNT(*) as cantidad 
FROM tasks 
GROUP BY status;

-- Ver las últimas 5 tareas creadas
SELECT id, title, status, created_at 
FROM tasks 
ORDER BY created_at DESC 
LIMIT 5;

-- Salir de sqlite3
.quit
```

### Desde PowerShell/CMD (sin entrar en sqlite3):
```bash
# Ver todas las tareas
sqlite3 tasks.db "SELECT * FROM tasks;"

# Ver estructura de la tabla
sqlite3 tasks.db ".schema tasks"

# Contar tareas
sqlite3 tasks.db "SELECT COUNT(*) FROM tasks;"
```

## 🎨 Opción 3: Herramientas gráficas (Recomendadas para uso frecuente)

### DB Browser for SQLite (Gratis)
- Descarga: https://sqlitebrowser.org/
- Permite visualizar, editar y administrar la base de datos con interfaz gráfica
- Muy útil para depuración y pruebas

### Otras opciones:
- **SQLiteStudio**: https://sqlitestudio.pl/
- **DBeaver**: https://dbeaver.io/ (Soporta múltiples bases de datos)

## 📝 Ejemplos de consultas útiles

### Ver todas las tareas:
```sql
SELECT * FROM tasks ORDER BY created_at DESC;
```

### Ver solo tareas pendientes:
```sql
SELECT id, title, description, created_at 
FROM tasks 
WHERE status = 'todo'
ORDER BY created_at DESC;
```

### Ver tareas en progreso:
```sql
SELECT id, title, description, created_at 
FROM tasks 
WHERE status = 'doing'
ORDER BY created_at DESC;
```

### Ver tareas completadas:
```sql
SELECT id, title, description, created_at 
FROM tasks 
WHERE status = 'done'
ORDER BY created_at DESC;
```

### Buscar tareas por título:
```sql
SELECT * FROM tasks 
WHERE title LIKE '%buscar%';
```

### Estadísticas completas:
```sql
SELECT 
    status,
    COUNT(*) as cantidad,
    MIN(created_at) as primera_tarea,
    MAX(created_at) as ultima_tarea
FROM tasks
GROUP BY status;
```

## ⚠️ Notas importantes

- La base de datos se crea automáticamente cuando ejecutas la aplicación
- El archivo se llama `tasks.db` y está en la raíz del proyecto
- **NO edites la base de datos manualmente** mientras la aplicación está corriendo (puede causar errores)
- Para hacer pruebas, es mejor usar el script `view_database.py` o cerrar la aplicación primero

