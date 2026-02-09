// Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadArea = document.querySelector('.upload-area');
const previewArea = document.getElementById('preview-area');
const actions = document.getElementById('actions');
const loading = document.getElementById('loading');
const originalImage = document.getElementById('original-image');
const svgContainer = document.getElementById('svg-container');
const downloadBtn = document.getElementById('download-btn');
const resetBtn = document.getElementById('reset-btn');

let currentSvgString = '';

// Drag & Drop Events
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    uploadArea.classList.add('dragover');
}

function unhighlight() {
    uploadArea.classList.remove('dragover');
}

dropZone.addEventListener('drop', handleDrop, false);
uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'image/png') {
            processFile(file);
        } else {
            alert('Please upload a PNG image.');
        }
    }
}

function processFile(file) {
    // UI Updates
    uploadArea.style.display = 'none';
    loading.style.display = 'flex';
    
    const reader = new FileReader();
    reader.readAsDataURL(file);
    
    reader.onloadend = function() {
        originalImage.src = reader.result;
        
        // Convert using ImageTracer
        // Options can be tweaked for better results
        const options = {
            ltr: true,
            numberofcolors: 16,
            mincolorratio: 0.02,
        };
        
        ImageTracer.imageToSVG(reader.result, function(svgstr) {
            currentSvgString = svgstr;
            displayResult(svgstr);
        }, options);
    }
}

function displayResult(svgString) {
    loading.style.display = 'none';
    previewArea.style.display = 'flex';
    actions.style.display = 'flex';
    
    // Inject SVG
    svgContainer.innerHTML = svgString;
    
    // Fix SVG dimensions if needed
    const svgElement = svgContainer.querySelector('svg');
    if (svgElement) {
        svgElement.setAttribute('width', '100%');
        svgElement.setAttribute('height', '100%');
    }
    
    // Setup Download
    downloadBtn.onclick = function() {
        const blob = new Blob([svgString], {type: 'image/svg+xml'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'converted.svg';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };
}

resetBtn.addEventListener('click', () => {
    uploadArea.style.display = 'block';
    previewArea.style.display = 'none';
    actions.style.display = 'none';
    fileInput.value = '';
    svgContainer.innerHTML = '';
    originalImage.src = '';
    currentSvgString = '';
});
