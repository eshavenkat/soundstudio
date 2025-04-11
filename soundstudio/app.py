from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import librosa
import numpy as np
from utils.audio_processor import AudioProcessor
from utils.analyzer import AudioAnalyzer
from utils.visualizer import AudioVisualizer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clustering')
def clustering():
    return render_template('clustering.html')

@app.route('/analysis/<track_id>')
def analysis(track_id):
    return render_template('analysis.html', track_id=track_id)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the audio file
        processor = AudioProcessor(filepath)
        analyzer = AudioAnalyzer(processor)
        visualizer = AudioVisualizer(analyzer)
        
        # Get analysis results
        analysis_results = analyzer.analyze()
        visualizations = visualizer.create_visualizations()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'analysis': analysis_results,
            'visualizations': visualizations
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5002) 