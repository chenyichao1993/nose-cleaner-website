#!/usr/bin/env python3
"""
创建鼻清洁器网站的专业占位符图片
使用PIL库生成高质量的占位符图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_images():
    """创建各种尺寸的占位符图片"""
    
    # 创建images目录
    os.makedirs('images', exist_ok=True)
    
    # 定义图片规格
    image_specs = [
        # (文件名, 宽度, 高度, 描述)
        ('hero-nose-cleaner', 800, 600, 'Best nasal irrigators and nose cleaners'),
        ('baby-nose-cleaner', 400, 300, 'Baby nose cleaner'),
        ('adult-nose-cleaner', 400, 300, 'Adult nose cleaner'),
        ('allergy-relief', 400, 300, 'Allergy relief nose cleaner'),
        ('navage-device', 300, 300, 'Naväge Nasal Irrigator'),
        ('neilmed-device', 300, 300, 'NeilMed Sinus Rinse'),
        ('baby-aspirator', 300, 300, 'Baby Nasal Aspirator'),
        ('safety-guide', 600, 400, 'Nasal Irrigation Safety Guide'),
        ('comparison-chart', 800, 500, 'Nose Cleaner Comparison Chart'),
        ('logo', 200, 60, 'Nose Cleaner Logo')
    ]
    
    for filename, width, height, description in image_specs:
        # 创建图片
        img = Image.new('RGB', (width, height), color='#f8f9fa')
        draw = ImageDraw.Draw(img)
        
        # 添加边框
        draw.rectangle([0, 0, width-1, height-1], outline='#dee2e6', width=2)
        
        # 添加中心图标（简单的医疗设备图标）
        center_x, center_y = width // 2, height // 2
        
        # 绘制简单的鼻清洁器图标
        if 'logo' in filename:
            # Logo样式
            draw.ellipse([center_x-20, center_y-15, center_x+20, center_y+15], 
                        fill='#007bff', outline='#0056b3', width=2)
            draw.text((center_x-30, center_y+25), 'NOSE', fill='#007bff', 
                     font_size=12, anchor='mm')
            draw.text((center_x-30, center_y+40), 'CLEANER', fill='#007bff', 
                     font_size=12, anchor='mm')
        else:
            # 产品图标
            # 主体
            draw.ellipse([center_x-30, center_y-20, center_x+30, center_y+20], 
                        fill='#e3f2fd', outline='#2196f3', width=3)
            # 喷嘴
            draw.rectangle([center_x-5, center_y-35, center_x+5, center_y-20], 
                          fill='#2196f3', outline='#1976d2', width=2)
            # 手柄
            draw.rectangle([center_x-15, center_y+20, center_x+15, center_y+35], 
                          fill='#2196f3', outline='#1976d2', width=2)
        
        # 添加描述文字
        if width > 200:  # 只在较大的图片上添加文字
            text_y = height - 40
            # 分割长文本
            words = description.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 25:  # 每行最多25个字符
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            for i, line in enumerate(lines[:2]):  # 最多显示2行
                draw.text((center_x, text_y + i*20), line, fill='#6c757d', 
                         font_size=14, anchor='mm')
        
        # 保存图片
        img.save(f'images/{filename}.png', 'PNG', optimize=True)
        print(f"✅ 创建图片: {filename}.png ({width}x{height})")

if __name__ == "__main__":
    create_placeholder_images()
    print("\n🎉 所有占位符图片创建完成！")
    print("📁 图片保存在 images/ 目录中")
