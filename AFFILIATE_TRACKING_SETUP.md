# Amazon Associates 转化跟踪设置指南

## 🎯 概述
本指南将帮助你在Google Analytics 4、Google Tag Manager和Microsoft Clarity中设置Amazon Associates转化跟踪。

## ✅ 已完成的设置

### 1. Amazon Associates账户
- ✅ 已申请Amazon Associates账户
- ✅ 已替换所有测试链接为真实affiliate链接
- ✅ 已添加转化跟踪JavaScript代码

### 2. 网站代码设置
- ✅ 已添加affiliate点击跟踪代码到 `js/main.js`
- ✅ 自动识别Amazon产品链接
- ✅ 提取产品名称和价格信息
- ✅ 发送事件到GA4、GTM和Clarity

## 📊 转化跟踪配置步骤

### 第一步：在Google Analytics 4中设置转化事件

1. **登录Google Analytics 4**
   - 访问：https://analytics.google.com/
   - 选择你的属性：Nose Cleaner

2. **创建自定义事件**
   - 进入 "Configure" → "Events"
   - 点击 "Create Event"
   - 事件名称：`affiliate_click`
   - 条件：`Event name equals affiliate_click`

3. **设置转化目标**
   - 进入 "Configure" → "Conversions"
   - 点击 "New conversion event"
   - 事件名称：`affiliate_click`
   - 点击 "Save"

### 第二步：在Google Tag Manager中设置转化跟踪

1. **登录Google Tag Manager**
   - 访问：https://tagmanager.google.com/
   - 选择容器：GTM-TRQ8QLR9

2. **创建转化跟踪标签**
   - 点击 "Tags" → "New"
   - 标签名称：`GA4 - Affiliate Conversion`
   - 标签类型：`Google Analytics: GA4 Event`
   - 配置标签：
     ```
     Event Name: affiliate_click
     Event Parameters:
     - event_category: Affiliate
     - event_label: {{Product Name}}
     - value: {{Product Price}}
     - currency: USD
     ```

3. **创建触发器**
   - 点击 "Triggers" → "New"
   - 触发器名称：`Affiliate Click`
   - 触发器类型：`Custom Event`
   - 事件名称：`affiliate_click`

4. **创建变量**
   - 点击 "Variables" → "New"
   - 变量名称：`Product Name`
   - 变量类型：`Data Layer Variable`
   - 数据层变量名称：`product_name`

   - 变量名称：`Product Price`
   - 变量类型：`Data Layer Variable`
   - 数据层变量名称：`product_price`

5. **发布更改**
   - 点击 "Submit" → "Publish"
   - 版本名称：`Affiliate Tracking Setup`
   - 发布说明：`Added affiliate conversion tracking`

### 第三步：在Microsoft Clarity中设置转化跟踪

1. **登录Microsoft Clarity**
   - 访问：https://clarity.microsoft.com/
   - 选择项目：Nose Cleaner

2. **设置转化目标**
   - 进入 "Goals" → "Create Goal"
   - 目标名称：`Affiliate Click`
   - 目标类型：`Custom Event`
   - 事件名称：`affiliate_click`

3. **设置转化漏斗**
   - 进入 "Funnels" → "Create Funnel"
   - 漏斗名称：`Affiliate Conversion Funnel`
   - 步骤1：`Page View` (首页访问)
   - 步骤2：`Custom Event` (affiliate_click)

## 🔍 验证转化跟踪

### 1. 实时测试
1. 访问你的网站：https://nosecleaner.online
2. 点击任意Amazon affiliate链接
3. 检查浏览器控制台是否显示：`Affiliate click tracked: [产品名称] [价格]`

### 2. Google Analytics 4验证
1. 进入GA4 → "Reports" → "Realtime"
2. 点击Amazon链接
3. 查看是否出现 `affiliate_click` 事件

### 3. Google Tag Manager验证
1. 进入GTM → "Preview" 模式
2. 访问你的网站
3. 点击Amazon链接
4. 查看是否触发 `affiliate_click` 事件

### 4. Microsoft Clarity验证
1. 进入Clarity → "Recordings"
2. 查看用户会话
3. 确认点击事件被记录

## 📈 转化跟踪数据

### 跟踪的产品信息
- **Naväge Nasal Care Starter Kit** - $99.88
- **NeilMed Sinus Rinse Kit** - $10.49
- **NoseFrida Baby Saline Kit** - $13.97
- **Frida Baby Aspirator** - $14.99
- **GROWNSY Electric Nasal Aspirator** - $31.99
- **Dr. Talbot's Silicone Nasal Aspirator** - $7.86

### 发送的事件数据
```javascript
{
    event: 'affiliate_click',
    product_name: '产品名称',
    product_price: 价格数字,
    affiliate_platform: 'Amazon',
    currency: 'USD'
}
```

## 🎯 转化优化建议

### 1. 监控关键指标
- **点击率 (CTR)**：affiliate链接点击次数 / 页面访问次数
- **转化率**：Amazon购买次数 / affiliate点击次数
- **收入**：Amazon佣金收入

### 2. 优化策略
- **A/B测试**：测试不同的按钮文案和位置
- **热力图分析**：使用Clarity分析用户点击行为
- **转化漏斗**：识别用户流失的关键环节

### 3. 定期检查
- **每周**：检查GA4中的affiliate_click事件数据
- **每月**：分析转化率和收入趋势
- **每季度**：优化转化跟踪设置

## 🚨 注意事项

1. **隐私合规**：确保转化跟踪符合GDPR和CCPA要求
2. **数据准确性**：定期验证跟踪数据的准确性
3. **Amazon政策**：遵守Amazon Associates的跟踪政策
4. **性能影响**：监控跟踪代码对网站性能的影响

## 📞 技术支持

如果遇到问题，请检查：
1. 浏览器控制台是否有JavaScript错误
2. GA4、GTM、Clarity是否正确配置
3. Amazon affiliate链接是否有效
4. 网络连接是否正常

---

**🎉 转化跟踪设置完成！现在你可以全面监控Amazon Associates的转化效果了！**
