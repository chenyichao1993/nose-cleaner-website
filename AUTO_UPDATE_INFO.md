# 🤖 自动更新系统说明

## ✅ 已启用GitHub Actions自动更新

### 📊 自动更新内容
- **价格信息**: 当前价格、原价、折扣百分比
- **评分信息**: 星级评分、评分数字、评论数量
- **更新时间**: 记录最后更新时间

### 🚫 不自动更新的内容
- **产品标题**: 保持手动设置
- **产品描述**: 保持手动优化
- **产品图片**: 保持手动设置

### ⏰ 更新频率
- 每天自动更新2次（北京时间9:00和18:00）
- 支持手动触发更新

### 🚀 使用方法
1. 推送代码到GitHub
2. GitHub Actions自动运行
3. 产品信息自动更新
4. 更新自动提交到仓库

### 📁 相关文件
- `.github/workflows/update-amazon-prices.yml` - GitHub Actions工作流
- `update_all_products.py` - 产品数据更新脚本
- `all_products_data.json` - 产品数据存储文件（自动生成）

### 🎯 支持的产品
- NeilMed Sinus Rinse Kit
- NoseFrida Baby Nasal Aspirator
- Naväge Nasal Care Starter Kit

---
**无需手动操作，完全自动化！** 🎉
