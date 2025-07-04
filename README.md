# 🎬 Aplicación de Compartir Videos

Una aplicación web sencilla desarrollada en Python con Flask para subir, almacenar y compartir videos de forma fácil.

## 📋 Características

- ✅ **Subida de videos**: Soporta formatos MP4, AVI, MOV, MKV, WEBM
- ✅ **Reproducción web**: Reproductor HTML5 integrado
- ✅ **Enlaces de compartición**: Genera enlaces únicos para cada video
- ✅ **Gestión simple**: Lista, visualiza y elimina videos
- ✅ **Interfaz responsive**: Funciona en desktop y móvil
- ✅ **Sin base de datos**: Usa archivos JSON para simplicidad

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes git instalado
   git clone <url-del-repositorio>
   cd proyecto_app_video
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**
   - Ve a: `http://localhost:5000`
   - ¡La aplicación estará lista para usar!

## 📱 Cómo usar la aplicación

### Subir un video
1. En la página principal, completa el formulario:
   - **Título**: Escribe un nombre descriptivo para tu video
   - **Archivo**: Selecciona un video desde tu computadora
2. Haz clic en "Subir Video"
3. El video aparecerá en la lista de videos subidos

### Ver un video
1. En la lista de videos, haz clic en "Ver Video"
2. Se abrirá una página con el reproductor y la información del video

### Compartir un video
1. Haz clic en el botón "Compartir" junto al video
2. Se abrirá un modal con un enlace único
3. Copia el enlace y compártelo con quien quieras
4. Cualquier persona con el enlace podrá ver el video

### Eliminar un video
1. Haz clic en "Eliminar" junto al video que quieras borrar
2. Confirma la acción en el diálogo que aparece
3. El video se eliminará permanentemente

## 📁 Estructura del Proyecto

```
proyecto_app_video/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias de Python
├── README.md          # Este archivo
├── videos_data.json   # Base de datos JSON (se crea automáticamente)
├── templates/         # Plantillas HTML
│   ├── index.html     # Página principal
│   └── video.html     # Página de visualización de video
├── static/           # Archivos estáticos
│   └── style.css     # Estilos CSS
└── uploads/          # Carpeta donde se guardan los videos
```

## ⚙️ Configuración

### Límites de archivo
- **Tamaño máximo**: 100MB por video
- **Formatos soportados**: MP4, AVI, MOV, MKV, WEBM

### Personalización
Puedes modificar estos valores en `app.py`:

```python
# Cambiar tamaño máximo (en bytes)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Agregar más formatos
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'}

# Cambiar puerto
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 🔧 Tecnologías Utilizadas

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Almacenamiento**: Sistema de archivos + JSON
- **Reproductor**: HTML5 Video
- **Estilos**: CSS personalizado + Font Awesome

## 📝 Notas Importantes

- Los videos se almacenan localmente en la carpeta `uploads/`
- La información de los videos se guarda en `videos_data.json`
- No hay autenticación de usuarios (aplicación simple)
- Los enlaces de compartición son públicos
- Para uso en producción, considera agregar autenticación y usar una base de datos real

## 🚨 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install flask
```

### Error: "Permission denied" al subir archivos
- Verifica que la carpeta `uploads/` tenga permisos de escritura

### El video no se reproduce
- Verifica que el formato sea compatible con tu navegador
- Algunos formatos pueden requerir códecs adicionales

### Puerto 5000 ocupado
- Cambia el puerto en `app.py`: `app.run(port=8000)`
- O usa: `python app.py` y especifica otro puerto

## 🎯 Ideas para Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] Base de datos real (SQLite/PostgreSQL)
- [ ] Conversión automática de formatos
- [ ] Thumbnails automáticos
- [ ] Sistema de comentarios
- [ ] Categorías y etiquetas
- [ ] Búsqueda de videos
- [ ] Límites por usuario
- [ ] Estadísticas de visualización

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**¡Disfruta compartiendo tus videos!** 🎥✨
