#!/usr/bin/env python3
"""
图片优化脚本
- 压缩图片文件大小
- 转换为WebP格式
- 生成不同尺寸的响应式图片
"""

from PIL import Image
import os
import glob

def optimize_images():
    """优化所有图片"""
    
    # 确保输出目录存在
    os.makedirs('images/webp', exist_ok=True)
    os.makedirs('images/responsive', exist_ok=True)
    
    # 获取所有PNG图片
    png_files = glob.glob('images/*.png')
    
    for png_file in png_files:
        filename = os.path.basename(png_file).replace('.png', '')
        print(f"🔄 优化图片: {filename}")
        
        # 打开原图
        with Image.open(png_file) as img:
            # 1. 转换为WebP格式（高质量）
            webp_path = f'images/webp/{filename}.webp'
            img.save(webp_path, 'WebP', quality=85, optimize=True)
            
            # 2. 生成响应式尺寸
            responsive_sizes = [
                (400, 300, 'mobile'),
                (800, 600, 'tablet'),
                (1200, 900, 'desktop')
            ]
            
            for width, height, size_name in responsive_sizes:
                # 保持宽高比缩放
                img_resized = img.copy()
                img_resized.thumbnail((width, height), Image.Resampling.LANCZOS)
                
                # 保存为PNG和WebP
                png_resized = f'images/responsive/{filename}_{size_name}.png'
                webp_resized = f'images/responsive/{filename}_{size_name}.webp'
                
                img_resized.save(png_resized, 'PNG', optimize=True)
                img_resized.save(webp_resized, 'WebP', quality=85, optimize=True)
            
            # 3. 特别处理logo（保持原始比例）
            if 'logo' in filename:
                logo_sizes = [(100, 30), (150, 45), (200, 60)]
                for w, h in logo_sizes:
                    logo_resized = img.copy()
                    logo_resized.thumbnail((w, h), Image.Resampling.LANCZOS)
                    
                    logo_png = f'images/responsive/{filename}_{w}x{h}.png'
                    logo_webp = f'images/responsive/{filename}_{w}x{h}.webp'
                    
                    logo_resized.save(logo_png, 'PNG', optimize=True)
                    logo_resized.save(logo_webp, 'WebP', quality=90, optimize=True)
        
        print(f"  ✅ WebP: {filename}.webp")
        print(f"  ✅ 响应式: {filename}_mobile, {filename}_tablet, {filename}_desktop")
    
    print("\n🎉 图片优化完成！")
    print("📁 WebP格式: images/webp/")
    print("📁 响应式图片: images/responsive/")

def generate_image_manifest():
    """生成图片清单文件"""
    manifest = {
        "images": {
            "hero": {
                "desktop": "images/webp/hero-nose-cleaner.webp",
                "tablet": "images/responsive/hero-nose-cleaner_tablet.webp",
                "mobile": "images/responsive/hero-nose-cleaner_mobile.webp"
            },
            "products": {
                "baby": {
                    "desktop": "images/webp/baby-nose-cleaner.webp",
                    "mobile": "images/responsive/baby-nose-cleaner_mobile.webp"
                },
                "adult": {
                    "desktop": "images/webp/adult-nose-cleaner.webp",
                    "mobile": "images/responsive/adult-nose-cleaner_mobile.webp"
                },
                "allergy": {
                    "desktop": "images/webp/allergy-relief.webp",
                    "mobile": "images/responsive/allergy-relief_mobile.webp"
                }
            },
            "devices": {
                "navage": "images/webp/navage-device.webp",
                "neilmed": "images/webp/neilmed-device.webp",
                "baby_aspirator": "images/webp/baby-aspirator.webp"
            },
            "guides": {
                "safety": "images/webp/safety-guide.webp",
                "comparison": "images/webp/comparison-chart.webp"
            },
            "logo": {
                "desktop": "images/responsive/logo_200x60.webp",
                "tablet": "images/responsive/logo_150x45.webp",
                "mobile": "images/responsive/logo_100x30.webp"
            }
        }
    }
    
    import json
    with open('images/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("📋 图片清单已生成: images/manifest.json")

if __name__ == "__main__":
    optimize_images()
    generate_image_manifest()
