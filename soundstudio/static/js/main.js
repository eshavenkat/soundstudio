// Common functionality for SoundStudio

// File upload handling
function handleFileUpload(uploadArea, fileInput, onFileSelect) {
    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2980b9';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#3498db';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3498db';
        const files = e.dataTransfer.files;
        onFileSelect(files);
    });
    
    // File input handler
    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        onFileSelect(files);
    });
}

// Loading spinner management
function showLoadingSpinner(spinner) {
    spinner.classList.remove('d-none');
}

function hideLoadingSpinner(spinner) {
    spinner.classList.add('d-none');
}

// Error handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(errorDiv, document.querySelector('.row'));
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Success message handling
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show';
    successDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(successDiv, document.querySelector('.row'));
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Visualization helpers
function createVisualization(containerId, data, layout) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    Plotly.newPlot(containerId, data, layout, {
        responsive: true,
        displayModeBar: false
    });
}

// Format duration helper
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// File size formatting
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Audio file validation
function validateAudioFile(file) {
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/ogg'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!validTypes.includes(file.type)) {
        throw new Error('Please upload a valid audio file (MP3, WAV, or OGG)');
    }
    
    if (file.size > maxSize) {
        throw new Error('File size must be less than 16MB');
    }
    
    return true;
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Local storage helpers
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    get: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    },
    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// Export functions
window.soundstudio = {
    handleFileUpload,
    showLoadingSpinner,
    hideLoadingSpinner,
    showError,
    showSuccess,
    createVisualization,
    formatDuration,
    formatFileSize,
    validateAudioFile,
    debounce,
    storage
}; 