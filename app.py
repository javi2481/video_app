# ===================================================================
# APLICACIÓN DE COMPARTIR VIDEOS
# Desarrollada con Flask para subir, almacenar y compartir videos
# ===================================================================

# Importación de librerías necesarias
import os          # Para operaciones del sistema de archivos
import json        # Para manejar datos en formato JSON
import uuid        # Para generar identificadores únicos
from datetime import datetime  # Para manejar fechas y horas
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename  # Para nombres de archivo seguros

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Clave secreta para sesiones (cambiar en producción)

# ===================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ===================================================================

UPLOAD_FOLDER = 'uploads'  # Carpeta donde se guardan los videos
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}  # Formatos de video permitidos
MAX_FILE_SIZE = 100 * 1024 * 1024  # Tamaño máximo: 100MB
VIDEOS_DATA_FILE = 'videos_data.json'  # Archivo donde se guarda información de videos

# Configuración de Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ===================================================================
# FUNCIONES AUXILIARES
# ===================================================================

def allowed_file(filename):
    """
    Verifica si el archivo tiene una extensión permitida
    
    Args:
        filename (str): Nombre del archivo a verificar
        
    Returns:
        bool: True si la extensión está permitida, False en caso contrario
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_videos_data():
    """
    Carga la información de los videos desde el archivo JSON
    
    Returns:
        dict: Diccionario con información de todos los videos, 
              o diccionario vacío si no existe el archivo
    """
    if os.path.exists(VIDEOS_DATA_FILE):
        with open(VIDEOS_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_videos_data(data):
    """
    Guarda la información de los videos en el archivo JSON
    
    Args:
        data (dict): Diccionario con información de videos a guardar
    """
    with open(VIDEOS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===================================================================
# RUTAS DE LA APLICACIÓN
# ===================================================================

@app.route('/')
def index():
    """
    Página principal de la aplicación
    
    Muestra:
    - Formulario para subir nuevos videos
    - Lista de todos los videos subidos
    - Opciones para ver, compartir y eliminar videos
    
    Returns:
        str: HTML renderizado de la página principal
    """
    # Cargar datos de todos los videos
    videos_data = load_videos_data()
    
    # Renderizar la página principal pasando los datos de videos
    return render_template('index.html', videos=videos_data)

@app.route('/upload', methods=['POST'])
def upload_video():
    """
    Maneja la subida de videos desde el formulario
    
    Proceso:
    1. Valida que se haya seleccionado un archivo
    2. Verifica que se haya ingresado un título
    3. Comprueba que el formato sea permitido
    4. Genera un nombre único para evitar conflictos
    5. Guarda el archivo en la carpeta uploads
    6. Almacena la información en el archivo JSON
    
    Returns:
        redirect: Redirección a la página principal con mensaje de éxito/error
    """
    # Verificar que se haya enviado un archivo
    if 'video' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    # Obtener el archivo y el título del formulario
    file = request.files['video']
    title = request.form.get('title', '').strip()
    
    # Validar que se haya seleccionado un archivo
    if file.filename == '':
        flash('No se seleccionó ningún archivo')
        return redirect(url_for('index'))
    
    # Validar que se haya ingresado un título
    if not title:
        flash('Por favor ingresa un título para el video')
        return redirect(url_for('index'))
    
    # Verificar que el archivo tenga una extensión permitida
    if file and allowed_file(file.filename):
        # Obtener la extensión del archivo original
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        
        # Generar un ID único para evitar conflictos de nombres
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.{file_extension}"
        
        # Crear la ruta completa donde se guardará el archivo
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Guardar el archivo físicamente en el servidor
        file.save(filepath)
        
        # Cargar los datos existentes de videos
        videos_data = load_videos_data()
        
        # Crear entrada para el nuevo video con toda su información
        videos_data[unique_id] = {
            'id': unique_id,                           # ID único del video
            'title': title,                            # Título ingresado por el usuario
            'filename': filename,                      # Nombre del archivo en el servidor
            'original_filename': file.filename,        # Nombre original del archivo
            'upload_date': datetime.now().isoformat(), # Fecha y hora de subida
            'file_size': os.path.getsize(filepath)     # Tamaño del archivo en bytes
        }
        
        # Guardar los datos actualizados en el archivo JSON
        save_videos_data(videos_data)
        
        # Mostrar mensaje de éxito y redirigir
        flash(f'Video "{title}" subido exitosamente!')
        return redirect(url_for('index'))
    else:
        # Mostrar error si el formato no está permitido
        flash('Tipo de archivo no permitido. Use: MP4, AVI, MOV, MKV, WEBM')
        return redirect(url_for('index'))

@app.route('/video/<video_id>')
def view_video(video_id):
    """
    Página para visualizar un video específico
    
    Muestra:
    - Reproductor de video HTML5
    - Información detallada del video
    - Opciones para compartir, descargar y eliminar
    
    Args:
        video_id (str): ID único del video a mostrar
        
    Returns:
        str: HTML renderizado de la página de video o redirección si no existe
    """
    # Cargar todos los datos de videos
    videos_data = load_videos_data()
    
    # Verificar que el video existe
    if video_id not in videos_data:
        flash('Video no encontrado')
        return redirect(url_for('index'))
    
    # Obtener los datos del video específico
    video = videos_data[video_id]
    
    # Renderizar la página de visualización del video
    return render_template('video.html', video=video)

@app.route('/stream/<video_id>')
def stream_video(video_id):
    """
    Sirve el archivo de video para streaming en el navegador
    
    Esta ruta es utilizada por el elemento <video> HTML5 para
    cargar y reproducir el contenido del video.
    
    Args:
        video_id (str): ID único del video a transmitir
        
    Returns:
        file: Archivo de video para streaming o error 404
    """
    # Cargar datos de videos
    videos_data = load_videos_data()
    
    # Verificar que el video existe en los datos
    if video_id not in videos_data:
        return "Video no encontrado", 404
    
    # Obtener información del video
    video = videos_data[video_id]
    
    # Construir la ruta completa al archivo de video
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video['filename'])
    
    # Verificar que el archivo físico existe
    if not os.path.exists(video_path):
        return "Archivo de video no encontrado", 404
    
    # Enviar el archivo para streaming
    return send_file(video_path)

@app.route('/delete/<video_id>', methods=['POST'])
def delete_video(video_id):
    """
    Elimina un video del sistema
    
    Proceso:
    1. Busca el video en los datos
    2. Elimina el archivo físico del servidor
    3. Remueve la entrada de los datos JSON
    4. Actualiza el archivo de datos
    
    Args:
        video_id (str): ID único del video a eliminar
        
    Returns:
        redirect: Redirección a la página principal con mensaje de confirmación
    """
    # Cargar datos actuales de videos
    videos_data = load_videos_data()
    
    # Verificar que el video existe
    if video_id in videos_data:
        # Obtener información del video
        video = videos_data[video_id]
        
        # Construir ruta al archivo físico
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video['filename'])
        
        # Eliminar archivo físico del servidor si existe
        if os.path.exists(video_path):
            os.remove(video_path)
        
        # Eliminar entrada de los datos JSON
        del videos_data[video_id]
        
        # Guardar datos actualizados
        save_videos_data(videos_data)
        
        flash('Video eliminado exitosamente')
    else:
        flash('Video no encontrado')
    
    # Redirigir a la página principal
    return redirect(url_for('index'))

# ===================================================================
# FUNCIONES AUXILIARES PARA TEMPLATES
# ===================================================================

def format_file_size(size_bytes):
    """
    Convierte bytes a formato legible para mostrar en la interfaz
    
    Ejemplos:
    - 1024 bytes -> "1.0 KB"
    - 1048576 bytes -> "1.0 MB"
    - 1073741824 bytes -> "1.0 GB"
    
    Args:
        size_bytes (int): Tamaño en bytes
        
    Returns:
        str: Tamaño formateado en unidades legibles
    """
    if size_bytes == 0:
        return "0B"
    
    # Unidades de medida en orden ascendente
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    # Dividir por 1024 hasta encontrar la unidad apropiada
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    # Retornar con un decimal y la unidad correspondiente
    return f"{size_bytes:.1f} {size_names[i]}"

# Registrar filtro personalizado para usar en templates Jinja2
app.jinja_env.filters['filesize'] = format_file_size

# ===================================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ===================================================================

if __name__ == '__main__':
    # Crear carpeta de uploads si no existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Mostrar información de inicio
    print("🎬 Aplicación de Compartir Videos")
    print("📁 Carpeta de uploads:", UPLOAD_FOLDER)
    print("🌐 Servidor iniciando en http://localhost:5000")
    print("🔧 Modo debug activado")
    print("📋 Formatos permitidos:", ', '.join(ALLOWED_EXTENSIONS).upper())
    print("📏 Tamaño máximo por archivo: 100MB")
    
    # Iniciar servidor Flask
    # debug=True: Reinicia automáticamente al cambiar código
    # host='0.0.0.0': Permite acceso desde otras IPs en la red local
    # port=5000: Puerto donde correrá la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
