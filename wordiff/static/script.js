function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = 'WordDiff 오류: ' + message;
    errorDiv.style.display = 'block';
} 