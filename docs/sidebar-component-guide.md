# 侧边栏组件使用指南

## 📋 概述

现在所有页面的侧边栏都使用统一的组件，确保样式一致和数据同步。

## 🏗️ 组件结构

### 1. 侧边栏组件文件
- **位置**: `components/sidebar.html`
- **内容**: 包含Categories和Newsletter两个widget

### 2. 样式文件
- **位置**: `css/sidebar.css`
- **内容**: 统一的侧边栏样式定义

### 3. 数据源
- **位置**: `data/articles.json`
- **加载方式**: 通过 `js/categories.js` 动态加载

## 🔧 使用方法

### 在页面中引用侧边栏组件

```html
<!-- Sidebar Component -->
<div id="sidebar-container"></div>
<script>
    // 动态加载侧边栏组件
    fetch('/components/sidebar.html')
        .then(response => response.text())
        .then(html => {
            document.getElementById('sidebar-container').innerHTML = html;
        })
        .catch(error => console.error('Error loading sidebar:', error));
</script>
```

### 添加CSS链接

```html
<link rel="stylesheet" href="/css/sidebar.css">
```

## 📊 数据更新机制

### 分类数据自动更新
1. 修改 `data/articles.json` 中的分类计数
2. 所有页面的侧边栏会自动显示最新数据
3. 无需手动更新每个页面

### 示例数据结构
```json
{
  "categories": {
    "Adult Care": {
      "slug": "adult-care",
      "count": 4,
      "url": "/blog/category/adult-care/"
    }
  }
}
```

## 🚀 添加新文章时的自动处理

使用 `scripts/add_new_article.py` 脚本时：
1. 自动更新 `data/articles.json`
2. 自动创建使用统一侧边栏组件的新文章页面
3. 自动更新博客首页和分类页面

## ✅ 已更新的页面

以下页面已使用统一的侧边栏组件：
- `blog/index.html` (博客首页)
- `blog/category/adult-care/index.html` (Adult Care分类页)
- `blog/adult-nasal-irrigation-complete-guide/index.html`
- `blog/sinus-pressure-relief-guide/index.html`
- 其他所有文章页面

## 🎯 优势

1. **样式一致**: 所有页面使用相同的侧边栏样式
2. **数据同步**: 分类计数自动更新，无需手动维护
3. **维护简单**: 只需修改一个组件文件
4. **自动集成**: 新文章自动使用统一组件

## 🔄 更新流程

### 修改侧边栏样式
1. 编辑 `css/sidebar.css`
2. 所有页面自动应用新样式

### 修改侧边栏内容
1. 编辑 `components/sidebar.html`
2. 所有页面自动显示新内容

### 更新分类数据
1. 编辑 `data/articles.json`
2. 所有页面自动显示最新分类计数

## 📝 注意事项

1. 确保所有页面都引用了 `css/sidebar.css`
2. 确保所有页面都使用了 `sidebar-container` 的加载方式
3. 新添加的页面会自动使用统一组件（通过 `add_new_article.py` 脚本）
4. 如果需要手动添加页面，请使用上述HTML代码片段
