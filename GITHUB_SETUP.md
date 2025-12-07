# 🚀 Guía para Subir el Proyecto a GitHub

Esta guía te ayudará a subir tu proyecto Organizador de Tareas Kanban a GitHub paso a paso.

## 📋 Prerrequisitos

1. ✅ Tener una cuenta de GitHub (crea una en https://github.com si no tienes)
2. ✅ Tener Git instalado (ya lo tienes: `git version 2.49.0.windows.1`)
3. ✅ Tener acceso a PowerShell/CMD

## 🔧 Pasos para Subir el Proyecto

### Paso 1: Verificar que estás en la carpeta correcta

Asegúrate de estar en la carpeta del proyecto:

```bash
cd C:\Users\pc\Desktop\Python_Project
```

### Paso 2: Inicializar el repositorio Git

```bash
git init
```

### Paso 3: Verificar qué archivos se van a agregar

```bash
git status
```

Deberías ver todos los archivos `.py`, `.qss`, `.md`, etc. listos para agregar.
**IMPORTANTE**: No deberías ver `tasks.db` ni archivos `__pycache__` (están en .gitignore).

### Paso 4: Agregar todos los archivos al repositorio

```bash
git add .
```

### Paso 5: Configurar Git (si es la primera vez)

Si es la primera vez que usas Git, configura tu nombre y email:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"
```

### Paso 6: Hacer el primer commit

```bash
git commit -m "Initial commit: Organizador de Tareas Kanban completo con PyQt5"
```

### Paso 7: Crear el repositorio en GitHub

1. Ve a https://github.com e inicia sesión
2. Haz clic en el botón **"+"** (esquina superior derecha) → **"New repository"**
3. Configura el repositorio:
   - **Repository name**: `organizador-tareas-kanban` (o el nombre que prefieras)
   - **Description**: "Aplicación de escritorio para gestionar tareas estilo Kanban con PyQt5"
   - **Visibilidad**: 
     - ✅ **Public** (cualquiera puede verlo)
     - ✅ **Private** (solo tú y personas que invites)
   - ⚠️ **NO marques** "Add a README file" (ya tenemos uno)
   - ⚠️ **NO marques** "Add .gitignore" (ya tenemos uno)
   - ⚠️ **NO marques** "Choose a license" (ya tenemos uno)
4. Haz clic en **"Create repository"**

### Paso 8: Conectar tu repositorio local con GitHub

GitHub te mostrará comandos. Ejecuta estos (reemplaza `tu-usuario` con tu nombre de usuario de GitHub):

```bash
git remote add origin https://github.com/tu-usuario/organizador-tareas-kanban.git
git branch -M main
git push -u origin main
```

**Si GitHub te pide autenticación:**

#### Opción A: Personal Access Token (Recomendado)

1. Ve a GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Haz clic en **"Generate new token (classic)"**
3. Dale un nombre como "Organizador Tareas"
4. Selecciona el scope **`repo`** (acceso completo a repositorios)
5. Haz clic en **"Generate token"**
6. **Copia el token** (solo lo verás una vez)
7. Cuando Git te pida la contraseña, usa el token en lugar de tu contraseña

#### Opción B: GitHub CLI (más fácil)

Instala GitHub CLI desde: https://cli.github.com/

Luego ejecuta:

```bash
gh auth login
```

Y sigue las instrucciones.

### Paso 9: Verificar que todo se subió correctamente

Ve a tu repositorio en GitHub: `https://github.com/tu-usuario/organizador-tareas-kanban`

Deberías ver todos los archivos del proyecto.

## ✅ Checklist Antes de Subir

- [x] README.md creado con instrucciones completas
- [x] .gitignore configurado para excluir archivos innecesarios
- [x] LICENSE agregado (MIT)
- [x] requirements.txt actualizado
- [x] Base de datos (tasks.db) en .gitignore
- [x] Archivos __pycache__ en .gitignore

## 📝 Comandos Git Útiles para el Futuro

### Ver el estado actual
```bash
git status
```

### Ver qué archivos cambiaron
```bash
git diff
```

### Agregar cambios específicos
```bash
git add nombre_archivo.py
```

### Hacer commit de cambios
```bash
git commit -m "Descripción de los cambios realizados"
```

### Subir cambios a GitHub
```bash
git push
```

### Ver el historial de commits
```bash
git log --oneline
```

### Actualizar desde GitHub (si trabajas en otra computadora)
```bash
git pull
```

## 🎯 Estructura Final del Repositorio

Tu repositorio en GitHub debería tener esta estructura:

```
organizador-tareas-kanban/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── main.py
├── view_database.py
├── DATABASE_VIEWER.md
├── GITHUB_SETUP.md
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── note_model.py
│   ├── controller.py
│   ├── note_controller.py
│   └── utils.py
└── ui/
    ├── __init__.py
    ├── main_window.py
    ├── sidebar.py
    ├── kanban_view.py
    ├── kanban_column.py
    ├── task_card.py
    ├── notepad_view.py
    ├── note_card.py
    ├── stats_view.py
    ├── calendar_view.py
    └── styles.qss
```

**NOTA**: Los siguientes archivos NO deberían aparecer en GitHub (están en .gitignore):
- `tasks.db` (base de datos)
- `__pycache__/` (archivos compilados)
- `notepad.txt` (si existe)

## 🎉 ¡Listo!

Una vez subido, tu proyecto estará disponible en GitHub y podrás:

- ✨ Compartirlo con otros desarrolladores
- 🤝 Colaborar en el proyecto
- 📊 Hacer seguimiento de cambios
- 🔄 Sincronizar entre diferentes computadoras
- 🌟 Mostrar tu trabajo en tu portfolio

## 📞 Problemas Comunes

### Error: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/tu-usuario/organizador-tareas-kanban.git
```

### Error: "Permission denied"
- Verifica que estés usando el token de acceso correcto
- Asegúrate de tener permisos en el repositorio

### Error: "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

**¡Felicitaciones! Tu proyecto está listo para compartirse en GitHub.** 🚀
