import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar en producción

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
VIDEOS_DATA_FILE = 'videos_data.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_videos_data():
    """Carga la información de los videos desde el archivo JSON"""
    if os.path.exists(VIDEOS_DATA_FILE):
        with open(VIDEOS_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_videos_data(data):
    """Guarda la información de los videos en el archivo JSON"""
    with open(VIDEOS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """Página principal con lista de videos y formulario de upload"""
    videos_data = load_videos_data()
    return render_template('index.html', videos=videos_data)

@app.route('/upload', methods=['POST'])
def upload_video():
    """Maneja la subida de videos"""
    if 'video' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    file = request.files['video']
    title = request.form.get('title', '').strip()
    
    if file.filename == '':
        flash('No se seleccionó ningún archivo')
        return redirect(url_for('index'))
    
    if not title:
        flash('Por favor ingresa un título para el video')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Generar nombre único para el archivo
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.{file_extension}"
        
        # Guardar archivo
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Guardar información del video
        videos_data = load_videos_data()
        videos_data[unique_id] = {
            'id': unique_id,
            'title': title,
            'filename': filename,
            'original_filename': file.filename,
            'upload_date': datetime.now().isoformat(),
            'file_size': os.path.getsize(filepath)
        }
        save_videos_data(videos_data)
        
        flash(f'Video "{title}" subido exitosamente!')
        return redirect(url_for('index'))
    else:
        flash('Tipo de archivo no permitido. Use: MP4, AVI, MOV, MKV, WEBM')
        return redirect(url_for('index'))

@app.route('/video/<video_id>')
def view_video(video_id):
    """Página para ver un video específico"""
    videos_data = load_videos_data()
    
    if video_id not in videos_data:
        flash('Video no encontrado')
        return redirect(url_for('index'))
    
    video = videos_data[video_id]
    return render_template('video.html', video=video)

@app.route('/stream/<video_id>')
def stream_video(video_id):
    """Sirve el archivo de video para streaming"""
    videos_data = load_videos_data()
    
    if video_id not in videos_data:
        return "Video no encontrado", 404
    
    video = videos_data[video_id]
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video['filename'])
    
    if not os.path.exists(video_path):
        return "Archivo de video no encontrado", 404
    
    return send_file(video_path)

@app.route('/delete/<video_id>', methods=['POST'])
def delete_video(video_id):
    """Elimina un video"""
    videos_data = load_videos_data()
    
    if video_id in videos_data:
        video = videos_data[video_id]
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video['filename'])
        
        # Eliminar archivo físico
        if os.path.exists(video_path):
            os.remove(video_path)
        
        # Eliminar de los datos
        del videos_data[video_id]
        save_videos_data(videos_data)
        
        flash('Video eliminado exitosamente')
    else:
        flash('Video no encontrado')
    
    return redirect(url_for('index'))

def format_file_size(size_bytes):
    """Convierte bytes a formato legible"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

# Filtro para usar en templates
app.jinja_env.filters['filesize'] = format_file_size

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("🎬 Aplicación de Compartir Videos")
    print("📁 Carpeta de uploads:", UPLOAD_FOLDER)
    print("🌐 Servidor iniciando en http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
