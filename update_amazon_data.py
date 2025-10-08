#!/usr/bin/env python3
"""
Amazon产品信息自动更新脚本
定期从Amazon页面抓取最新的价格、评分等信息并更新网站
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class AmazonDataUpdater:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_product_data(self, url):
        """从Amazon页面获取产品数据"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取价格信息
            price_data = self.extract_price(soup)
            
            # 提取评分信息
            rating_data = self.extract_rating(soup)
            
            # 提取产品标题
            title = self.extract_title(soup)
            
            return {
                'title': title,
                'price': price_data['current_price'],
                'original_price': price_data['original_price'],
                'discount': price_data['discount'],
                'rating': rating_data['rating'],
                'review_count': rating_data['review_count'],
                'stars': rating_data['stars'],
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return None
    
    def extract_price(self, soup):
        """提取价格信息"""
        price_data = {
            'current_price': None,
            'original_price': None,
            'discount': None
        }
        
        # 查找当前价格
        price_selectors = [
            '.a-price-whole',
            '.a-price .a-offscreen',
            '#price_inside_buybox',
            '.a-price-range'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text().strip()
                # 提取数字
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    price_data['current_price'] = f"${price_match.group()}"
                    break
        
        # 查找原价
        original_price_elem = soup.select_one('.a-text-price .a-offscreen')
        if original_price_elem:
            original_text = original_price_elem.get_text().strip()
            price_match = re.search(r'[\d,]+\.?\d*', original_text)
            if price_match:
                price_data['original_price'] = f"${price_match.group()}"
        
        # 查找折扣
        discount_elem = soup.select_one('.a-badge-text')
        if discount_elem:
            discount_text = discount_elem.get_text().strip()
            discount_match = re.search(r'-?\d+%', discount_text)
            if discount_match:
                price_data['discount'] = discount_match.group()
        
        return price_data
    
    def extract_rating(self, soup):
        """提取评分信息"""
        rating_data = {
            'rating': None,
            'review_count': None,
            'stars': None
        }
        
        # 查找评分
        rating_elem = soup.select_one('.a-icon-alt')
        if rating_elem:
            rating_text = rating_elem.get_text().strip()
            rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+5', rating_text)
            if rating_match:
                rating_data['rating'] = rating_match.group(1)
                
                # 生成星级
                rating_float = float(rating_match.group(1))
                full_stars = int(rating_float)
                half_star = 1 if rating_float - full_stars >= 0.5 else 0
                empty_stars = 5 - full_stars - half_star
                
                stars = '★' * full_stars + '☆' * half_star + '☆' * empty_stars
                rating_data['stars'] = stars
        
        # 查找评论数量
        review_elem = soup.select_one('#acrCustomerReviewText')
        if review_elem:
            review_text = review_elem.get_text().strip()
            review_match = re.search(r'([\d,]+)', review_text)
            if review_match:
                rating_data['review_count'] = review_match.group(1)
        
        return rating_data
    
    def extract_title(self, soup):
        """提取产品标题"""
        title_elem = soup.select_one('#productTitle')
        if title_elem:
            return title_elem.get_text().strip()
        return None
    
    def update_html_file(self, product_data, html_file='index.html'):
        """更新HTML文件中的产品信息"""
        if not product_data:
            return False
            
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新价格
            if product_data['price']:
                content = re.sub(
                    r'<span class="price">\$[\d,]+\.?\d*</span>',
                    f'<span class="price">{product_data["price"]}</span>',
                    content
                )
            
            # 更新原价
            if product_data['original_price']:
                content = re.sub(
                    r'<span class="original-price">\$[\d,]+\.?\d*</span>',
                    f'<span class="original-price">{product_data["original_price"]}</span>',
                    content
                )
            
            # 更新折扣
            if product_data['discount']:
                content = re.sub(
                    r'<span class="discount">-\d+%</span>',
                    f'<span class="discount">{product_data["discount"]}</span>',
                    content
                )
            
            # 更新评分
            if product_data['rating'] and product_data['review_count']:
                rating_pattern = r'<span class="rating-text">\d+\.?\d*/5 \([\d,]+ reviews\)</span>'
                replacement = f'<span class="rating-text">{product_data["rating"]}/5 ({product_data["review_count"]} reviews)</span>'
                content = re.sub(rating_pattern, replacement, content)
            
            # 更新星级
            if product_data['stars']:
                content = re.sub(
                    r'<span class="stars">[★☆]+</span>',
                    f'<span class="stars">{product_data["stars"]}</span>',
                    content
                )
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 成功更新 {html_file}")
            return True
            
        except Exception as e:
            print(f"❌ 更新HTML文件失败: {e}")
            return False
    
    def save_data_to_json(self, product_data, filename='amazon_data.json'):
        """保存数据到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(product_data, f, indent=2, ensure_ascii=False)
            print(f"✅ 数据已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存数据失败: {e}")

def main():
    """主函数"""
    updater = AmazonDataUpdater()
    
    # NeilMed产品URL
    neilmed_url = "https://www.amazon.com/NeilMed-100-Sinus-Rinse-Complete/dp/B000RDZFZ0"
    
    print("🔄 开始更新Amazon产品数据...")
    
    # 获取产品数据
    product_data = updater.get_product_data(neilmed_url)
    
    if product_data:
        print("📊 获取到的产品数据:")
        for key, value in product_data.items():
            print(f"  {key}: {value}")
        
        # 更新HTML文件
        updater.update_html_file(product_data)
        
        # 保存数据到JSON
        updater.save_data_to_json(product_data)
        
        print("✅ 更新完成!")
    else:
        print("❌ 获取产品数据失败")

if __name__ == "__main__":
    main()
