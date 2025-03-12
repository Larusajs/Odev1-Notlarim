import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import time
from typing import Dict, List, Optional

class AmazonScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.base_url = "https://www.amazon.com.tr"
        
    def _get_headers(self) -> Dict[str, str]:
        """Rastgele bir user agent ile header oluşturur."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def search_products(self, keyword: str, max_pages: int = 1) -> List[Dict]:
        """
        Verilen anahtar kelimeye göre ürün araması yapar.
        
        Args:
            keyword: Aranacak ürün adı
            max_pages: Taranacak maksimum sayfa sayısı
            
        Returns:
            Bulunan ürünlerin listesi
        """
        products = []
        
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/s?k={keyword}&page={page}"
            
            try:
                response = requests.get(url, headers=self._get_headers(), timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for card in product_cards:
                    product = self._extract_product_info(card)
                    if product:
                        products.append(product)
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"Sayfa {page} taranırken hata oluştu: {str(e)}")
                continue
                
        return products
    
    def _extract_product_info(self, card) -> Optional[Dict]:
        """Ürün kartından bilgileri çıkarır."""
        try:
            # ASIN (Amazon Standard Identification Number)
            asin = card.get('data-asin')
            
            # Ürün başlığı
            title_element = card.find('h2', {'class': 'a-size-mini'})
            title = title_element.get_text().strip() if title_element else None
            
            # Fiyat
            price_element = card.find('span', {'class': 'a-price-whole'})
            price = price_element.get_text().strip() if price_element else None
            
            # Ürün linki
            link_element = card.find('a', {'class': 'a-link-normal s-no-outline'})
            link = self.base_url + link_element.get('href') if link_element else None
            
            # Yıldız değerlendirmesi
            rating_element = card.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.get_text().split()[0] if rating_element else None
            
            # Değerlendirme sayısı
            review_count_element = card.find('span', {'class': 'a-size-base s-underline-text'})
            review_count = review_count_element.get_text() if review_count_element else None
            
            return {
                'asin': asin,
                'title': title,
                'price': price,
                'rating': rating,
                'review_count': review_count,
                'url': link
            }
            
        except Exception as e:
            print(f"Ürün bilgisi çıkarılırken hata oluştu: {str(e)}")
            return None

def main():
    scraper = AmazonScraper()
    
    # Örnek kullanım
    keyword = input("Aramak istediğiniz ürünü girin: ")
    max_pages = int(input("Kaç sayfa taramak istiyorsunuz? "))
    
    products = scraper.search_products(keyword, max_pages)
    
    # Sonuçları JSON dosyasına kaydet
    with open('amazon_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"\nToplam {len(products)} ürün bulundu.")
    print("Sonuçlar 'amazon_products.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    main() 