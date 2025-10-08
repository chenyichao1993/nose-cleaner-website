# Amazon产品信息自动更新系统

## 📋 功能说明

这个系统可以自动从Amazon页面抓取最新的产品信息（价格、评分、评论数量等）并更新到网站中。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4 schedule
```

### 2. 手动更新（一次性）

```bash
python update_amazon_data.py
```

### 3. 启动定时更新服务

```bash
python schedule_updates.py
```

## 📊 更新内容

- ✅ **价格信息**: 当前价格、原价、折扣百分比
- ✅ **评分信息**: 星级评分、评分数字、评论数量
- ✅ **产品标题**: 自动更新产品名称
- ✅ **更新时间**: 记录最后更新时间

## ⏰ 定时设置

默认设置：
- 每天上午 9:00 自动更新
- 每天下午 6:00 自动更新

### 修改更新频率

编辑 `schedule_updates.py` 文件：

```python
# 每小时更新
schedule.every().hour.do(run_update)

# 每30分钟更新
schedule.every(30).minutes.do(run_update)

# 每周更新
schedule.every().week.do(run_update)
```

## 🔧 配置说明

### 支持的Amazon产品

目前配置了以下产品：
- NeilMed Sinus Rinse Kit (ASIN: B000RDZFZ0)

### 添加新产品

1. 在 `update_amazon_data.py` 中添加新的产品URL
2. 修改 `main()` 函数中的产品列表
3. 确保HTML中有对应的产品卡片

## 📁 文件说明

- `update_amazon_data.py` - 主要更新脚本
- `schedule_updates.py` - 定时任务调度器
- `amazon_data.json` - 保存的产品数据（自动生成）
- `AMAZON_UPDATE_README.md` - 使用说明

## ⚠️ 注意事项

1. **Amazon反爬虫**: 如果更新失败，可能需要：
   - 更换User-Agent
   - 添加代理
   - 增加请求间隔

2. **数据准确性**: 
   - 价格和评分会实时变化
   - 建议设置合理的更新频率
   - 定期检查数据准确性

3. **服务器部署**:
   - 可以在VPS上运行定时任务
   - 使用cron job替代Python schedule
   - 考虑使用云函数（AWS Lambda等）

## 🛠️ 故障排除

### 常见问题

1. **网络连接失败**
   ```
   解决方案: 检查网络连接，尝试使用代理
   ```

2. **HTML解析失败**
   ```
   解决方案: Amazon可能更新了页面结构，需要更新选择器
   ```

3. **权限错误**
   ```
   解决方案: 确保有写入HTML文件的权限
   ```

### 日志查看

运行时会显示详细的更新日志，包括：
- 获取到的产品数据
- 更新成功/失败状态
- 错误信息

## 📈 扩展功能

### 可以添加的功能

1. **多产品支持**: 同时更新多个Amazon产品
2. **邮件通知**: 价格变化时发送邮件提醒
3. **数据库存储**: 保存历史价格数据
4. **Web界面**: 提供管理界面
5. **API接口**: 提供REST API获取数据

### 集成建议

1. **GitHub Actions**: 使用GitHub Actions定时运行
2. **Docker**: 容器化部署
3. **监控**: 添加健康检查和监控
4. **备份**: 定期备份数据

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本 (推荐3.7+)
2. 依赖包是否正确安装
3. 网络连接是否正常
4. Amazon页面是否可访问
