from typing import Iterable
import scrapy
from scrapy.http import Request


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://amazon.com"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }

    def start_requests(self):
        page = 1
        for page in range(1, 21):
            url = f'https://www.amazon.com/s?k=laptop&page={page}&ref=sr_pg_{page}'
            page += 1
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        result = response.css(
            "div[data-component-type = 's-search-result']")

        if result:
            for data in result:
                url = data.css(
                    "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal ::attr(href)").get()

                yield scrapy.Request(url=f'https://amazon.com{url}', headers=self.headers, callback=self.get_details)

    def get_details(self, response):

        title = response.css("span[id = 'productTitle'] ::text").get()
        store_name = response.css("a[id ='sellerProfileTriggerId'] ::text").get()
        description = response.css("div[id = 'productDescription'] p span ::text").getall()
        price = response.css("span.a-price-whole ::text").get()
        fraction_price = response.css("span.a-price-fraction ::text").get()
        discount = response.css("span.a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage ::text").get()
        rating = response.css("i.a-icon.a-icon-star.a-star-4-5.cm-cr-review-stars-spacing-big span.a-icon-alt ::text").get()
        review_count = response.css("span[data-hook = 'total-review-count'] ::text").get()
        availability = response.css("div[id = 'availability'] span.a-size-medium.a-color-success ::text").get()
        rows = response.css("div.a-expander-content.a-expander-section-content.a-section-expander-inner")

        for row in rows:
            cols = row.css("tr[class*='a'] ::text")
            if len(cols) == 2:
                key = cols[0].get()
                value = cols[1].get()

            yield {
                'title': title,
                'store_name': store_name,
                'description': description,
                'price': f'{price}.{fraction_price}',
                'discount': discount,
                'rating': rating,
                'review_count': review_count,
                'availability': availability,
                'url': response.url
                }
            
            # fix with shell later
                
                

        
