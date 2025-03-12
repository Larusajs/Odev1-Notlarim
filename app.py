from flask import Flask, render_template, request, jsonify
from amazon_scraper import AmazonScraper
import json

app = Flask(__name__)
scraper = AmazonScraper()

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
        
        return jsonify({
            'success': True,
            'products': products,
            'total': len(products)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 