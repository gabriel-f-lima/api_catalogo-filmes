function showLoading(msg = 'Processando...') {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.querySelector('p').innerText = msg;
        overlay.style.display = 'flex';
    }
}

// Global initialization if needed, but triggers are usually page-specific.
// We can provide a standard way to attach them.
window.Loading = {
    show: showLoading,
    attachToForms: function(msg) {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', () => showLoading(msg));
        });
    },
    attachToLinks: function(selector, msg) {
        document.querySelectorAll(selector).forEach(link => {
            link.addEventListener('click', () => showLoading(msg));
        });
    }
};
