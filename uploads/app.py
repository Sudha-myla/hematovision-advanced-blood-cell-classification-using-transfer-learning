from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', result="No file part")

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', result="No selected file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Simulate prediction (Replace with your model logic)
            result = "Neutrophil"
            confidence = 94.5
            class_probs = [94.5, 2.3, 1.7, 1.5]
            class_names = ['Neutrophil', 'Eosinophil', 'Lymphocyte', 'Monocyte']

            return render_template(
                'index.html',
                result=result,
                confidence=confidence,
                image_file=f"uploads/{filename}",
                class_probs=class_probs,
                class_names=class_names
            )
        else:
            return render_template('index.html', result="Invalid file type")

    return render_template('index.html')

# Serve uploaded files
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
