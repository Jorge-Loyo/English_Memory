# 🚀 Guía para Subir English Memory a GitHub

## ✅ Pre-requisitos

1. Tener Git instalado
2. Tener una cuenta de GitHub
3. Crear un repositorio en GitHub (público o privado)

## 📋 Verificación Pre-Subida

Ejecuta el script de verificación:

```bash
python verificar_proyecto.py
```

Este script verifica que todos los archivos necesarios estén presentes.

## 🔧 Pasos para Subir al Repositorio

### 1. Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Click en "New repository"
3. Nombre: `english-memory`
4. Descripción: "Aplicación educativa para aprender vocabulario en inglés"
5. Público o Privado (tu elección)
6. **NO** inicialices con README, .gitignore o LICENSE (ya los tenemos)
7. Click en "Create repository"

### 2. Inicializar Git Local

```bash
# Navegar a la carpeta del proyecto
cd C:\git\Popurri\Diccionario

# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Verificar qué se agregará
git status

# Hacer commit inicial
git commit -m "feat: Initial release v1.0.0 - English Memory

- Gestión completa de vocabulario
- Modo práctica interactivo
- 9 pestañas funcionales
- Soporte Windows y Linux
- Documentación completa"
```

### 3. Conectar con GitHub

```bash
# Reemplaza 'tu-usuario' con tu nombre de usuario de GitHub
git remote add origin https://github.com/tu-usuario/english-memory.git

# Verificar que se agregó correctamente
git remote -v

# Renombrar rama a main (si es necesario)
git branch -M main
```

### 4. Subir al Repositorio

```bash
# Primera subida
git push -u origin main

# Si pide autenticación, usa tu token de GitHub
# (No uses contraseña, GitHub ya no lo permite)
```

### 5. Crear Tag de Versión

```bash
# Crear tag para v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Subir el tag
git push origin v1.0.0
```

### 6. Crear Release en GitHub

1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `English Memory v1.0.0`
5. Descripción:
```markdown
## 🎉 Primera Release - English Memory v1.0.0

Aplicación educativa multiplataforma para aprender vocabulario en inglés.

### ✨ Características
- 📚 Gestión completa de vocabulario
- 🎯 Modo práctica interactivo
- 🔊 Pronunciación fonética
- ✍️ Práctica de caligrafía
- 📍 47 preposiciones
- 📅 58 términos de tiempo
- 🔢 Conversor de números
- 📊 Estadísticas

### 📦 Descargas
- Windows: `English Memory.exe`
- Linux: `English Memory`

### 📖 Documentación
Ver [README.md](README.md) para instrucciones completas.
```

6. Adjuntar ejecutables (si los tienes):
   - `dist/English Memory.exe` (Windows)
   - `dist/English Memory` (Linux)

7. Click en "Publish release"

## 📝 Actualizaciones Futuras

Para subir cambios nuevos:

```bash
# Ver cambios
git status

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "tipo: descripción breve

Descripción detallada si es necesario"

# Subir cambios
git push origin main
```

### Tipos de Commit

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato (no afecta código)
- `refactor:` Refactorización
- `test:` Tests
- `chore:` Mantenimiento

## 🔐 Configurar Token de GitHub

Si GitHub pide autenticación:

1. Ve a GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Selecciona scopes: `repo`, `workflow`
5. Copia el token
6. Úsalo como contraseña cuando Git lo pida

## 📊 Después de Subir

### Configurar GitHub Pages (opcional)

Para documentación web:

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs
4. Save

### Agregar Topics

En la página principal del repo:
- Click en ⚙️ (Settings)
- Agregar topics: `python`, `education`, `english`, `vocabulary`, `tkinter`, `learning`

### Configurar About

- Description: "Aplicación educativa para aprender vocabulario en inglés"
- Website: (si tienes)
- Topics: (agregar relevantes)

### Crear Issues Templates

Para que usuarios reporten bugs o sugieran funcionalidades.

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Git inicializado localmente
- [ ] Todos los archivos agregados
- [ ] Commit inicial realizado
- [ ] Remote configurado
- [ ] Push exitoso
- [ ] Tag v1.0.0 creado
- [ ] Release publicado
- [ ] README visible en GitHub
- [ ] .gitignore funcionando
- [ ] LICENSE visible

## 🎉 ¡Listo!

Tu proyecto ahora está en GitHub y listo para que otros lo descarguen y usen.

### Compartir el Proyecto

URL del repositorio:
```
https://github.com/tu-usuario/english-memory
```

Comando para clonar:
```bash
git clone https://github.com/tu-usuario/english-memory.git
```

## 📞 Ayuda

Si tienes problemas:
- 📧 administrador@agilizesoluciones.com
- 📱 +54 11 6168-2555

## 📚 Recursos Útiles

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)
