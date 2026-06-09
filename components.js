function addGoogleAnalytics() {
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=G-NW46YVD2QH";
    document.head.appendChild(script);

    const configScript = document.createElement("script");
    configScript.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-NW46YVD2QH');
    `;
    document.head.appendChild(configScript);
}

function activePageForPath(pathname) {
    if (pathname === "/" || pathname === "/index.html") return "home";
    if (pathname.includes("projects")) return "projects";
    if (pathname.includes("blog")) return "blog";
    return "";
}

function loadComponent(targetId, url, fallbackHtml) {
    const target = document.getElementById(targetId);
    if (!target) return Promise.resolve();

    return fetch(url)
        .then((response) => response.text())
        .then((html) => {
            target.innerHTML = html;
        })
        .catch((error) => {
            console.error(`Error loading ${url}:`, error);
            target.innerHTML = fallbackHtml;
        });
}

function insertCTA() {
    const footer = document.getElementById("shared-footer");
    if (!footer || document.querySelector(".cta-section")) return;

    fetch("/cta.html")
        .then((response) => response.text())
        .then((html) => {
            const wrapper = document.createElement("div");
            wrapper.innerHTML = html.trim();
            const cta = wrapper.firstElementChild;
            if (cta) footer.parentNode.insertBefore(cta, footer);
        })
        .catch((error) => {
            console.error("Error loading /cta.html:", error);
        });
}

document.addEventListener("DOMContentLoaded", function () {
    loadComponent(
        "shared-header",
        "/header.html",
        '<header class="site-header"><div class="site-header-container"><a href="/" class="site-brand">Ziyad Mir</a></div></header>'
    ).then(() => {
        const activePage = activePageForPath(window.location.pathname);
        if (!activePage) return;

        const header = document.getElementById("shared-header");
        const activeLink = header && header.querySelector(`.site-nav-link[data-page="${activePage}"]`);
        if (activeLink) activeLink.classList.add("active");
    });

    loadComponent(
        "shared-footer",
        "/footer.html",
        '<footer class="site-footer"><div class="site-footer-container"><p class="site-footer-text">&copy; 2011-2026 Ziyad Mir</p></div></footer>'
    );

    insertCTA();
    addGoogleAnalytics();
});
