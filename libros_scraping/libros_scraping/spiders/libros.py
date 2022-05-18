import scrapy

#Links_libros = response.xpath('//div[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]/a/@href').getall()
 #Link_lectura = response.xpath('/html/body/div[1]/div/p[3]/a/@href').get()
#titulo = response.xpath('//h1[@class="title"]/text()').get()
#Contenido = response.xpath('//div[@class="col-xs-12"]/article//text()').getall()
#Siguiente = response.xpath('//div[@class="col-xs-2 col-sm-3 text-right"]/a/@href').get()

class Libros_scraping(scrapy.Spider):
    name= 'libros_scraping'
    start_urls = [
        "https://www.textos.info/libros"
    ]

    custom_settings = {
        'FEED_URI': 'libros_scraper.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 12, #Antes 24
        'USER_AGENT': 'MaxDamian'
    }

    def parse(self, response):
        links_books = response.xpath('//div[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]/a/@href').getall()

        for link in links_books:
            yield response.follow(link)

            link_ebook = response.xpath('/html/body/div[1]/div/p[3]/a/@href').get()

            if link_ebook:
                yield response.follow(link_ebook, callback=self.parse_text, cb_kwargs={'url': response.urljoin(link_ebook)})

                # link = link_ebook
                # title = response.xpath('//h1[@class="title"]/text()').get()
                # content = response.xpath('//div[@class="col-xs-12"]/article//text()').getall()

                # yield {
                # 'url': link,
                # 'title': title,
                # 'content': content
                # }
            
        next_pages = response.xpath('//div[@class="col-xs-2 col-sm-3 text-right"]/a/@href').get()
        if next_pages:
            yield response.follow(next_pages, callback=self.parse)

    # def parse_ebook(self, response):
    #     link_ebook = response.xpath('/html/body/div[1]/div/p[3]/a/@href').get()

    #     response.follow(link_ebook, callback=self.parse_text,cb_kwargs={'url':response.urljoin(link_ebook)})

    def parse_text(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="title"]/text()').get()
        content = response.xpath('//div[@class="col-xs-12"]/article//text()').getall()
        if content and title:
            yield {
                'url': link,
                'title': title,
                'content': content
            }