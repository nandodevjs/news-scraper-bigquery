import scrapy
import os


class BbcSpider(scrapy.Spider):
    
    name = "bbc"
    
    def start_requests(self):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', '..', 'urls.txt')

        with open(file_path, 'r') as f:
            urls = f.read().splitlines()
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('.bWszMR ::text').get(),
            'publication_date': response.css('.WPunI ::text').get(),
            'author': response.css('.hhBctz ::text').extract()[1].strip() if len(response.css('.hhBctz ::text').extract()) > 1 else None,
            'news': ' '.join(response.css('#main-content .fYAfXe ::text').getall()).replace('\n', ' ').replace('\xa0', ' ').strip()
        }