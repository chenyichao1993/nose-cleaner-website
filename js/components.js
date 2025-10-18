// 动态加载页头和页脚组件
document.addEventListener('DOMContentLoaded', function() {
    // 加载页头组件
    const headerContainer = document.getElementById('header-container');
    if (headerContainer) {
        fetch('/components/header.html')
            .then(response => response.text())
            .then(html => {
                headerContainer.innerHTML = html;
                // 执行页头组件中的JavaScript
                const scripts = headerContainer.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    newScript.textContent = script.textContent;
                    document.head.appendChild(newScript);
                });
            })
            .catch(error => console.error('Error loading header:', error));
    }
    
    // 加载页脚组件
    const footerContainer = document.getElementById('footer-container');
    if (footerContainer) {
        fetch('/components/footer.html')
            .then(response => response.text())
            .then(html => {
                footerContainer.innerHTML = html;
                // 执行页脚组件中的JavaScript
                const scripts = footerContainer.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    newScript.textContent = script.textContent;
                    document.head.appendChild(newScript);
                });
            })
            .catch(error => console.error('Error loading footer:', error));
    }
    
    // 加载侧边栏组件
    const sidebarContainer = document.getElementById('sidebar-container');
    if (sidebarContainer) {
        fetch('/components/sidebar.html')
            .then(response => response.text())
            .then(html => {
                sidebarContainer.innerHTML = html;
                // 执行侧边栏组件中的JavaScript
                const scripts = sidebarContainer.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    newScript.textContent = script.textContent;
                    document.head.appendChild(newScript);
                });
            })
            .catch(error => console.error('Error loading sidebar:', error));
    }
});