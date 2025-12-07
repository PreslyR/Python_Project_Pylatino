# 📋 Organizador de Tareas - Kanban

Aplicación de escritorio desarrollada en Python con PyQt5 para gestionar tareas de manera eficiente usando el método Kanban. Incluye un tablero Kanban interactivo, bloc de notas, estadísticas y un calendario para programar tareas.

## ✨ Características

### 🎯 Tablero Kanban
- **Tres columnas**: Por Hacer, En Progreso, Hecho
- **Drag & Drop**: Arrastra y suelta tareas entre columnas
- **CRUD completo**: Crear, leer, actualizar y eliminar tareas
- **Guardado automático**: Todas las operaciones se guardan en SQLite

### 📝 Bloc de Notas
- **Sistema de tarjetas**: Cada nota es una tarjeta independiente
- **Auto-guardado**: Guarda automáticamente después de 1 segundo sin escribir
- **Funcionalidades**: Crear, editar, eliminar y exportar notas
- **Almacenamiento persistente**: Base de datos SQLite

### 📊 Estadísticas
- **Contadores por estado**: Visualiza cuántas tareas hay en cada estado
- **Gráfico de barras**: Visualización interactiva con matplotlib
- **Actualización en tiempo real**: Se actualiza automáticamente

### 📅 Calendario
- **Vista mensual**: Navega por el calendario para ver tareas programadas
- **Días resaltados**: Los días con tareas aparecen marcados
- **Lista de tareas**: Al hacer clic en un día, muestra todas sus tareas
- **Fechas programadas**: Asigna fechas de vencimiento a tus tareas

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **PyQt5**: Interfaz gráfica de usuario
- **SQLite**: Base de datos local
- **Matplotlib**: Gráficos y visualizaciones

## 📦 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/organizador-tareas-kanban.git
cd organizador-tareas-kanban
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- PyQt5 (interfaz gráfica)
- Matplotlib (gráficos)

### 3. Ejecutar la aplicación

```bash
python main.py
```

## 📖 Uso

### Tablero Kanban

1. **Crear tarea**: Haz clic en el botón "+ Agregar Tarea" en cualquier columna
2. **Editar tarea**: Haz clic en "Editar" en la tarjeta de la tarea
3. **Mover tarea**: Arrastra la tarjeta a otra columna
4. **Eliminar tarea**: Haz clic en "Eliminar" y confirma

### Bloc de Notas

1. Accede desde el sidebar haciendo clic en "📝 Bloc de notas"
2. Haz clic en "➕ Nueva Nota" para crear una nota
3. Las notas se guardan automáticamente
4. Usa los botones para editar, eliminar o exportar

### Calendario

1. Accede desde el sidebar haciendo clic en "📅 Calendario"
2. Los días con tareas programadas aparecen resaltados
3. Haz clic en un día para ver las tareas de ese día
4. Al crear una tarea, marca "Programar fecha:" para asignarle una fecha

### Estadísticas

1. Accede desde el sidebar haciendo clic en "📊 Estadísticas"
2. Visualiza contadores y gráfico de barras
3. Haz clic en "🔄 Actualizar" para refrescar los datos

## 📁 Estructura del Proyecto

```
organizador-tareas-kanban/
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
│
├── app/                   # Módulo de aplicación
│   ├── __init__.py
│   ├── database.py        # Gestión de base de datos SQLite
│   ├── models.py          # Modelo de datos (TaskModel)
│   ├── note_model.py      # Modelo de datos para notas
│   ├── controller.py      # Controlador de tareas
│   ├── note_controller.py # Controlador de notas
│   └── utils.py           # Utilidades auxiliares
│
├── ui/                    # Módulo de interfaz de usuario
│   ├── __init__.py
│   ├── main_window.py     # Ventana principal
│   ├── sidebar.py         # Barra lateral de navegación
│   ├── kanban_view.py     # Vista del tablero Kanban
│   ├── kanban_column.py   # Componente de columna Kanban
│   ├── task_card.py       # Tarjeta de tarea
│   ├── notepad_view.py    # Vista del bloc de notas
│   ├── note_card.py       # Tarjeta de nota
│   ├── stats_view.py      # Vista de estadísticas
│   ├── calendar_view.py   # Vista de calendario
│   └── styles.qss         # Estilos CSS
│
├── tasks.db               # Base de datos SQLite (se crea automáticamente)
└── view_database.py       # Script para visualizar la base de datos
```

## 🗄️ Base de Datos

El proyecto utiliza SQLite como base de datos local. Se crean automáticamente dos tablas:

### Tabla `tasks`
- `id`: ID único de la tarea
- `title`: Título de la tarea
- `description`: Descripción de la tarea
- `status`: Estado (todo, doing, done)
- `created_at`: Fecha de creación
- `due_date`: Fecha programada/vencimiento (opcional)

### Tabla `notes`
- `id`: ID único de la nota
- `title`: Título de la nota
- `content`: Contenido de la nota
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última modificación

### Visualizar la base de datos

Para ver el contenido de la base de datos, ejecuta:

```bash
python view_database.py
```

O para ver solo las tareas:

```bash
python view_database.py --tasks
```

## 🎨 Personalización

### Estilos

Los estilos de la aplicación se encuentran en `ui/styles.qss`. Puedes modificar colores, fuentes y apariencia editando este archivo.

### Configuración

- La base de datos se guarda en `tasks.db` en la raíz del proyecto
- El bloc de notas guarda automáticamente en `notepad.txt` (si usas el sistema anterior)
- Las notas se guardan en la base de datos SQLite

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

```bash
python main.py
```

### Estructura del código

- **MVC Pattern**: Separación entre modelos, vistas y controladores
- **Señales PyQt**: Comunicación entre componentes usando señales
- **Modular**: Cada componente es independiente y reutilizable

## 📝 Notas

- La base de datos se crea automáticamente al ejecutar la aplicación por primera vez
- Todas las operaciones se guardan inmediatamente en la base de datos
- El proyecto no requiere conexión a internet

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [MIT License](LICENSE).

## 👤 Autor

Desarrollado como proyecto de organización de tareas con PyQt5.

## 🐛 Problemas Conocidos

- Ninguno hasta el momento

## 🔮 Futuras Mejoras

- [ ] Búsqueda de tareas y notas
- [ ] Categorías o etiquetas
- [ ] Notificaciones de tareas vencidas
- [ ] Exportar/Importar datos
- [ ] Temas personalizables
- [ ] Sincronización en la nube

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un [issue](https://github.com/tu-usuario/organizador-tareas-kanban/issues) en el repositorio.

---

⭐ Si te gustó el proyecto, ¡dale una estrella en GitHub!

