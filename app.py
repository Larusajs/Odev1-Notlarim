from flask import Flask, render_template, request, jsonify
from amazon_scraper import AmazonScraper
import json
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
scraper = AmazonScraper()

# Veritabanı bağlantısı
def get_db():
    db = sqlite3.connect('amazon_scraper.db')
    db.row_factory = sqlite3.Row
    return db

# Veritabanını oluştur
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                product_count INTEGER
            )
        ''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        max_pages = int(data.get('max_pages', 1))
        
        if not keyword:
            return jsonify({'error': 'Arama terimi gerekli'}), 400
            
        if max_pages < 1:
            return jsonify({'error': 'Sayfa sayısı en az 1 olmalıdır'}), 400
            
        products = scraper.search_products(keyword, max_pages)
        
        # Aramayı veritabanına kaydet
        db = get_db()
        db.execute('INSERT INTO searches (keyword, product_count) VALUES (?, ?)',
                  [keyword, len(products)])
        db.commit()
        
        return jsonify({
            'success': True,
            'products': products,
            'total': len(products)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    db = get_db()
    
    # Toplam arama sayısı
    total_searches = db.execute('SELECT COUNT(*) as count FROM searches').fetchone()['count']
    
    # Toplam bulunan ürün sayısı
    total_products = db.execute('SELECT SUM(product_count) as count FROM searches').fetchone()['count']
    
    # Son aramalar
    recent_searches = db.execute('''
        SELECT keyword, COUNT(*) as count 
        FROM searches 
        GROUP BY keyword 
        ORDER BY MAX(timestamp) DESC 
        LIMIT 5
    ''').fetchall()
    
    # Ortalama ürün sayısı
    avg_products = db.execute('SELECT AVG(product_count) as avg FROM searches').fetchone()['avg']
    
    stats_data = {
        'total_searches': total_searches,
        'total_products': total_products or 0,
        'avg_price': avg_products or 0,
        'recent_searches': [
            {'keyword': row['keyword'], 'count': row['count']} 
            for row in recent_searches
        ],
        'popular_categories': [
            {'name': 'Elektronik', 'count': 150},
            {'name': 'Kitap', 'count': 120},
            {'name': 'Giyim', 'count': 100},
            {'name': 'Ev', 'count': 80},
            {'name': 'Spor', 'count': 50}
        ]
    }
    
    return render_template('stats.html', stats=stats_data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    if not os.path.exists('amazon_scraper.db'):
        init_db()
    app.run(debug=True) 