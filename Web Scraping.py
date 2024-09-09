import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# تابعی برای استخراج اطلاعات از یک صفحه
def extract_page_data(page_number):
    url = f'https://bama.ir/car?page={page_number}'
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    cars = []

    # انتخاب تمام آگهی‌ها
    ads = soup.select('.car-item')
    for ad in ads:
        price_tag = ad.select_one('.price span')
        price = price_tag.text.strip() if price_tag else "توافقی"
        
        # رد کردن آگهی‌های با قیمت توافقی
        if price == "توافقی":
            continue
        
        model_tag = ad.select_one('.detail .title')
        model = model_tag.text.strip() if model_tag else ""
        
        kilometer_tag = ad.select_one('.detail .distance span')
        kilometer = kilometer_tag.text.strip() if kilometer_tag else ""
        
        year_tag = ad.select_one('.detail .year')
        year = year_tag.text.strip() if year_tag else ""
        
        city_tag = ad.select_one('.detail .location')
        city = city_tag.text.strip() if city_tag else ""

        price = re.sub(r'[^0-9]', '', price)  # حذف کاراکترهای غیر عددی از قیمت
        
        cars.append((model, kilometer, year, city, price))
    
    return cars

# ایجاد دیتابیس و جدول برای ذخیره‌سازی اطلاعات خودروها
conn = sqlite3.connect('cars.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY,
        model TEXT,
        kilometer TEXT,
        year TEXT,
        city TEXT,
        price INTEGER
    )
''')
conn.commit()

# استخراج و ذخیره‌سازی اطلاعات ۲۰۰ صفحه اول
for page in range(1, 201):
    cars = extract_page_data(page)
    c.executemany('''
        INSERT INTO cars (model, kilometer, year, city, price)
        VALUES (?, ?, ?, ?, ?)
    ''', cars)
    conn.commit()
    print(f'Page {page} done')

conn.close()
