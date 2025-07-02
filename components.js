// Add Google Analytics
function addGoogleAnalytics() {
    // Google Analytics 4 (GA4)
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-NW46YVD2QH';
    document.head.appendChild(script);
    
    const configScript = document.createElement('script');
    configScript.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-NW46YVD2QH');
    `;
    document.head.appendChild(configScript);
}

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

// Insert CTA section before the shared footer
function insertCTA() {
    const footerElement = document.getElementById('shared-footer');
    if (!footerElement) return;

    fetch('/cta.html')
        .then(response => response.text())
        .then(data => {
            const wrapper = document.createElement('div');
            wrapper.innerHTML = data;
            footerElement.parentNode.insertBefore(wrapper.firstElementChild, footerElement);
        })
        .catch(error => {
            console.error('Error loading CTA:', error);
        });
}

// Execute when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    includeHTML();
    insertCTA();
    addGoogleAnalytics();
});