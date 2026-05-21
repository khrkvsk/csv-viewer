import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Файл не выбран', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'Файл не выбран', 400
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)

        table_html = df.to_html(classes='dataframe', index=False)
        
        return render_template('result.html', table_html=table_html)
    else:
        return 'Неподдерживаемый формат. Загрузите CSV файл.', 400

if __name__ == '__main__':
    app.run(debug=True)