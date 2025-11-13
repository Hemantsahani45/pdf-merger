from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    try:
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        pdf_writer = PdfWriter()
        
        for file in files:
            if file and allowed_file(file.filename):
                file_stream = io.BytesIO(file.read())
                pdf_reader = PdfReader(file_stream)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='merged.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/split', methods=['POST'])
def split_pdf():
    try:
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        page_range = request.form.get('page_range', '')
        file_stream = io.BytesIO(file.read())
        pdf_reader = PdfReader(file_stream)
        
        pdf_writer = PdfWriter()
        
        if page_range:
            # Parse page range (e.g., "1-3,5,7-9")
            pages = []
            for part in page_range.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    pages.extend(range(start - 1, end))
                else:
                    pages.append(int(part) - 1)
            
            for page_num in pages:
                if 0 <= page_num < len(pdf_reader.pages):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
        else:
            # Split all pages into separate PDFs
            # For simplicity, return first page
            pdf_writer.add_page(pdf_reader.pages[0])
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='split.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rotate', methods=['POST'])
def rotate_pdf():
    try:
        file = request.files['file']
        angle = int(request.form.get('angle', 90))
        
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        file_stream = io.BytesIO(file.read())
        pdf_reader = PdfReader(file_stream)
        pdf_writer = PdfWriter()
        
        for page in pdf_reader.pages:
            rotated_page = page.rotate(angle)
            pdf_writer.add_page(rotated_page)
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='rotated.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        file_stream = io.BytesIO(file.read())
        pdf_reader = PdfReader(file_stream)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
        
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compress', methods=['POST'])
def compress_pdf():
    try:
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        file_stream = io.BytesIO(file.read())
        pdf_reader = PdfReader(file_stream)
        pdf_writer = PdfWriter()
        
        for page in pdf_reader.pages:
            page.compress_content_streams()
            pdf_writer.add_page(page)
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='compressed.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/watermark', methods=['POST'])
def add_watermark():
    try:
        file = request.files['file']
        watermark_text = request.form.get('text', 'WATERMARK')
        
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        file_stream = io.BytesIO(file.read())
        pdf_reader = PdfReader(file_stream)
        pdf_writer = PdfWriter()
        
        # Create watermark PDF
        watermark_pdf = io.BytesIO()
        c = canvas.Canvas(watermark_pdf, pagesize=letter)
        c.setFont("Helvetica", 50)
        c.setFillColorRGB(0.7, 0.7, 0.7, alpha=0.3)
        c.rotate(45)
        c.drawString(200, 100, watermark_text)
        c.save()
        watermark_pdf.seek(0)
        watermark_reader = PdfReader(watermark_pdf)
        watermark_page = watermark_reader.pages[0]
        
        for page in pdf_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='watermarked.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

