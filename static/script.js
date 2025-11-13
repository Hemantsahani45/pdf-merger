// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        
        // Remove active class from all tabs and contents
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        btn.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});

// File upload area interactions
function setupFileUpload(uploadAreaId, inputId, isMultiple = false) {
    const uploadArea = document.getElementById(uploadAreaId);
    const fileInput = document.getElementById(inputId);
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#8b5cf6';
        uploadArea.style.transform = 'scale(1.02)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#6366f1';
        uploadArea.style.transform = 'scale(1)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#6366f1';
        uploadArea.style.transform = 'scale(1)';
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect(inputId, isMultiple);
        }
    });
    
    fileInput.addEventListener('change', () => handleFileSelect(inputId, isMultiple));
}

function handleFileSelect(inputId, isMultiple) {
    const fileInput = document.getElementById(inputId);
    const fileList = document.getElementById(inputId.replace('File', 'FileList').replace('Files', 'FileList'));
    
    if (fileList) {
        fileList.innerHTML = '';
        
        Array.from(fileInput.files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <i class="fas fa-file-pdf"></i>
                <span>${file.name} (${formatFileSize(file.size)})</span>
            `;
            fileList.appendChild(fileItem);
        });
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Setup all file upload areas
setupFileUpload('mergeUploadArea', 'mergeFiles', true);
setupFileUpload('splitUploadArea', 'splitFile');
setupFileUpload('rotateUploadArea', 'rotateFile');
setupFileUpload('extractUploadArea', 'extractFile');
setupFileUpload('compressUploadArea', 'compressFile');
setupFileUpload('watermarkUploadArea', 'watermarkFile');

// Form submissions
document.getElementById('mergeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('mergeForm', '/merge', true);
});

document.getElementById('splitForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('splitForm', '/split', true);
});

document.getElementById('rotateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('rotateForm', '/rotate', true);
});

document.getElementById('extractForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('extractForm', '/extract-text', false);
});

document.getElementById('compressForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('compressForm', '/compress', true);
});

document.getElementById('watermarkForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('watermarkForm', '/watermark', true);
});

async function submitForm(formId, endpoint, isFileDownload) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    
    showLoading();
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        
        if (isFileDownload) {
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = response.headers.get('Content-Disposition')?.split('filename=')[1]?.replace(/"/g, '') || 'output.pdf';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                showNotification('File processed successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'An error occurred', 'error');
            }
        } else {
            const data = await response.json();
            if (response.ok) {
                // Display extracted text
                const textOutput = document.getElementById('extractedText');
                const textContent = document.getElementById('textContent');
                textContent.value = data.text;
                textOutput.style.display = 'block';
                showNotification('Text extracted successfully!', 'success');
            } else {
                showNotification(data.error || 'An error occurred', 'error');
            }
        }
    } catch (error) {
        showNotification('Network error: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification ' + (type === 'error' ? 'error' : '');
    notification.style.display = 'block';
    
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

function copyText() {
    const textContent = document.getElementById('textContent');
    textContent.select();
    document.execCommand('copy');
    showNotification('Text copied to clipboard!', 'success');
}

