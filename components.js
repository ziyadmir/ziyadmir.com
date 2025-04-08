// Function to include HTML components
function includeHTML() {
    const headerElement = document.getElementById('shared-header');
    
    if (headerElement) {
        fetch('/header.html')
            .then(response => response.text())
            .then(data => {
                headerElement.innerHTML = data;
                
                // Highlight the current page in the navigation
                const currentPage = window.location.pathname;
                const navLinks = headerElement.querySelectorAll('nav a');
                
                navLinks.forEach(link => {
                    if (link.getAttribute('href') === currentPage || 
                        (currentPage === '/' && link.getAttribute('href') === '/') ||
                        (currentPage === '/index.html' && link.getAttribute('href') === '/')) {
                        link.classList.add('text-blue-300');
                    }
                });
            })
            .catch(error => {
                console.error('Error loading header:', error);
                headerElement.innerHTML = '<div class="container mx-auto px-4 py-3"><a href="/">Ziyad Mir</a></div>';
            });
    }
    
    const footerElement = document.getElementById('shared-footer');
    
    if (footerElement) {
        fetch('/footer.html')
            .then(response => response.text())
            .then(data => {
                footerElement.innerHTML = data;
            })
            .catch(error => {
                console.error('Error loading footer:', error);
                footerElement.innerHTML = '<div class="container mx-auto px-4 text-center"><p>&copy; 2025 Ziyad Mir</p></div>';
            });
    }
}

// Execute when DOM is fully loaded
document.addEventListener('DOMContentLoaded', includeHTML);