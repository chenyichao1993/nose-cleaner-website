// 动态加载页头和页脚组件
document.addEventListener('DOMContentLoaded', function() {
    // 加载页头组件
    const headerContainer = document.getElementById('header-container');
    if (headerContainer) {
        fetch('/components/header.html')
            .then(response => response.text())
            .then(html => {
                headerContainer.innerHTML = html;
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
            })
            .catch(error => console.error('Error loading footer:', error));
    }
});