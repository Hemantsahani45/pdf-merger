# PDF Toolkit - Advanced PDF Operations

A beautiful and powerful web application built with Flask and Python for performing various PDF operations. This application provides an intuitive user interface for common PDF tasks.

## Features

- **Merge PDFs**: Combine multiple PDF files into a single document
- **Split PDF**: Extract specific pages from a PDF document
- **Rotate PDF**: Rotate all pages in a PDF (90°, 180°, 270°)
- **Extract Text**: Extract all text content from a PDF document
- **Compress PDF**: Reduce the file size of PDF documents
- **Add Watermark**: Add text watermarks to PDF documents

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Use the application**:
   - Select a tab for the operation you want to perform
   - Upload your PDF file(s)
   - Configure any additional options
   - Click the action button to process your PDF

## Features in Detail

### Merge PDFs
- Upload multiple PDF files
- Files will be merged in the order they are selected
- Download the merged PDF

### Split PDF
- Upload a single PDF file
- Optionally specify page ranges (e.g., "1-3,5,7-9")
- Extract specific pages or the first page

### Rotate PDF
- Upload a PDF file
- Select rotation angle (90°, 180°, or 270°)
- All pages will be rotated accordingly

### Extract Text
- Upload a PDF file
- Extract all text content
- Copy the extracted text to clipboard

### Compress PDF
- Upload a PDF file
- Reduce file size by compressing content streams
- Download the compressed PDF

### Add Watermark
- Upload a PDF file
- Enter custom watermark text
- Add watermark to all pages

## Technologies Used

- **Backend**: Flask (Python web framework)
- **PDF Processing**: PyPDF2, ReportLab
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Design**: Modern gradient design with smooth animations

## File Structure

```
pdf-toolkit/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # Stylesheet
    └── script.js         # JavaScript functionality
```

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Limitations

- Maximum file size: 50MB per file
- Text extraction quality depends on PDF structure
- Some PDFs with complex layouts may not extract text perfectly

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

For issues or questions, please open an issue on the repository.

