import scrapy

class BbcSpider(scrapy.Spider):
    name = "bbc"
    start_urls = [
        "https://www.bbc.com/news/articles/c511vl9yjwwo",
        "https://www.bbc.com/news/articles/cjqqnwnqnxko",
        "https://www.bbc.com/news/articles/cv225l8l7jzo",
        "https://www.bbc.com/news/articles/c6pp08q513do",
        "https://www.bbc.com/news/articles/c1vv6p9k1z1o",
        "https://www.bbc.com/news/articles/crggk5rvqd1o",
        "https://www.bbc.com/news/articles/cj7793exd15o",
        "https://www.bbc.com/news/articles/cy00gykj13zo",
        "https://www.bbc.com/news/articles/c4nnr9945vmo",
        "https://www.bbc.com/news/articles/clwwz7rlgrgo",
    ]

    def parse(self, response):
        yield {
            'title': response.css('.bWszMR ::text').get(),
            'publication_date': response.css('.WPunI ::text').get(),
            'author': response.css('.hhBctz ::text').extract()[1].strip() if len(response.css('.hhBctz ::text').extract()) > 1 else None,
            'news': ' '.join(response.css('#main-content .fYAfXe ::text').getall()).replace('\n', ' ').replace('\xa0', ' ').strip()
        }