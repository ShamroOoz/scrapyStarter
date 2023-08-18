import scrapy
from HeloScrapy.items import MyProducts


class QuotesSpider(scrapy.Spider):
    name = "QuotesSpider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

  

    def parse(self, response):
        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    
        
    def parse_author(self, response):
       products = MyProducts()
       
       def extract_with_css(query):
          return response.css(query).get(default="").strip()
      
       products["name"] = extract_with_css("h3.author-title::text")
       products["birthdate"] = extract_with_css(".author-born-date::text")
       products["bio"] = extract_with_css(".author-description::text")
       
       yield products
