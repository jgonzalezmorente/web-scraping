from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = 'Hoteles'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
    download_delay = 2
    rules = (
        Rule(LinkExtractor(allow=r'/Hotel_Review-'), follow=True, callback='parse_hotel'),
    )

    def quitarSimboloDolar(self, texto):
        nuevoTexto = texto.replace('$', '')
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r', '').replace('\t', '')
        return nuevoTexto

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@data-automation="finalPrice"]/text()',
                       MapCompose(self.quitarSimboloDolar))
        item.add_xpath('descripcion', '//div[@id="ABOUT_TAB"]//div[contains(@class, "fIrGe _T")]//text()',
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities', '//div[contains(@data-test-target, "amenity_text")]/text()')
        yield item.load_item()

