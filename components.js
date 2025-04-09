// Function to include HTML components
function includeHTML() {
    const headerElement = document.getElementById('shared-header');
    
    if (headerElement) {
        fetch('/header.html')
            .then(response => response.text())
            .then(data => {
                headerElement.innerHTML = data;
                
                // Highlight the current page in the navigation menu
                const currentPage = window.location.pathname;
                let activePage = '';
                
                if (currentPage === '/' || currentPage === '/index.html') {
                    activePage = 'home';
                } else if (currentPage.includes('about')) {
                    activePage = 'about';
                } else if (currentPage.includes('projects')) {
                    activePage = 'projects';
                } else if (currentPage.includes('blog')) {
                    activePage = 'blog';
                } else if (currentPage.includes('memoir')) {
                    activePage = 'memoir';
                }
                
                // Add active class to the current page link
                if (activePage) {
                    const activeLink = headerElement.querySelector(`.site-nav-link[data-page="${activePage}"]`);
                    if (activeLink) {
                        activeLink.classList.add('active');
                    }
                }
            })
            .catch(error => {
                console.error('Error loading header:', error);
                headerElement.innerHTML = '<div class="site-header-container"><a href="/" class="site-brand">Ziyad Mir</a></div>';
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
                footerElement.innerHTML = '<div class="site-footer-container"><p class="site-footer-text">&copy; 2025 Ziyad Mir</p></div>';
            });
    }
}

// Execute when DOM is fully loaded
document.addEventListener('DOMContentLoaded', includeHTML);