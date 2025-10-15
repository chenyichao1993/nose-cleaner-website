// 动态加载分类数据
function loadCategories() {
    fetch('/data/articles.json')
        .then(response => response.json())
        .then(data => {
            const categoriesList = document.getElementById('categories-list');
            if (categoriesList) {
                categoriesList.innerHTML = '';
                
                // 按分类名称排序
                const sortedCategories = Object.entries(data.categories)
                    .sort(([a], [b]) => a.localeCompare(b));
                
                sortedCategories.forEach(([categoryName, categoryData]) => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="${categoryData.url}">${categoryName} <span>(${categoryData.count})</span></a>`;
                    categoriesList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('加载分类数据失败:', error);
        });
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', loadCategories);
