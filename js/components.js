/**
 * 组件加载器 - 动态加载共享组件
 */

class ComponentLoader {
    constructor() {
        this.components = new Map();
        this.loadPromises = new Map();
    }

    /**
     * 加载组件HTML内容
     * @param {string} componentPath - 组件文件路径
     * @returns {Promise<string>} - 组件HTML内容
     */
    async loadComponent(componentPath) {
        if (this.components.has(componentPath)) {
            return this.components.get(componentPath);
        }

        if (this.loadPromises.has(componentPath)) {
            return this.loadPromises.get(componentPath);
        }

        const loadPromise = fetch(componentPath)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load component: ${componentPath}`);
                }
                return response.text();
            })
            .then(html => {
                this.components.set(componentPath, html);
                this.loadPromises.delete(componentPath);
                return html;
            })
            .catch(error => {
                console.error(`Error loading component ${componentPath}:`, error);
                this.loadPromises.delete(componentPath);
                throw error;
            });

        this.loadPromises.set(componentPath, loadPromise);
        return loadPromise;
    }

    /**
     * 将组件插入到指定元素中
     * @param {string} selector - 目标元素选择器
     * @param {string} componentPath - 组件文件路径
     */
    async insertComponent(selector, componentPath) {
        try {
            const html = await this.loadComponent(componentPath);
            const targetElement = document.querySelector(selector);
            
            if (targetElement) {
                targetElement.innerHTML = html;
            } else {
                console.warn(`Target element not found: ${selector}`);
            }
        } catch (error) {
            console.error(`Failed to insert component ${componentPath} into ${selector}:`, error);
        }
    }

    /**
     * 批量加载组件
     * @param {Object} components - 组件映射 {selector: componentPath}
     */
    async loadComponents(components) {
        const promises = Object.entries(components).map(([selector, componentPath]) => 
            this.insertComponent(selector, componentPath)
        );
        
        await Promise.all(promises);
    }
}

// 创建全局实例
window.componentLoader = new ComponentLoader();

/**
 * 自动加载侧边栏组件
 */
document.addEventListener('DOMContentLoaded', async function() {
    // 检查是否有侧边栏容器
    const sidebarContainer = document.querySelector('.blog-sidebar');
    if (sidebarContainer) {
        try {
            await window.componentLoader.insertComponent('.blog-sidebar', '/components/sidebar.html');
        } catch (error) {
            console.error('Failed to load sidebar component:', error);
        }
    }
});

/**
 * 工具函数：动态更新文章数据
 */
window.updateArticleData = async function() {
    try {
        const response = await fetch('/data/articles.json');
        const data = await response.json();
        
        // 更新Categories
        const categoryElements = document.querySelectorAll('.category-list li');
        categoryElements.forEach(li => {
            const link = li.querySelector('a');
            const span = li.querySelector('span');
            if (link && span) {
                const categoryName = link.textContent.split(' ')[0];
                const categoryData = data.categories[categoryName];
                if (categoryData) {
                    span.textContent = `(${categoryData.count})`;
                }
            }
        });

        // 更新Recent Posts
        const recentPostsContainer = document.querySelector('.recent-posts');
        if (recentPostsContainer && data.articles) {
            const recentArticles = data.articles.slice(0, 5); // 取最新5篇
            recentPostsContainer.innerHTML = recentArticles.map(article => `
                <li>
                    <a href="${article.url}">
                        <img src="/images/responsive/${article.image.mobile}" alt="${article.shortTitle}" width="60" height="60">
                        <div>
                            <h4>${article.shortTitle}</h4>
                            <span>${article.displayDate}</span>
                        </div>
                    </a>
                </li>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to update article data:', error);
    }
};
