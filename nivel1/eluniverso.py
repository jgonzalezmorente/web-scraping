from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):
    titular = Field()
    descripcion = Field()

class ElUniversoSpider(Spider):
    name = 'MiSegundoSpider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    start_urls = ['https://www.eluniverso.com/deportes']
    def parse(self, response):
        # sel = Selector(response)
        # noticias = sel.xpath('//div[contains(@class, "card-content")][.//h2]')
        # for noticia in noticias:
        #     item = ItemLoader(Noticia(), noticia)
        #     item.add_xpath('titular', './/h2/a/text()')
        #     item.add_xpath('descripcion', './/p/text()')
        #     yield item.load_item()

        soup = BeautifulSoup(response.body, 'html.parser')
        noticias = soup.find_all(lambda tag: tag.name == 'div' and 'card-content' in tag.get('class', []) and tag.find('h2'))
        for noticia in noticias:
            item = ItemLoader(Noticia(), response.body)
            titular = noticia.find('h2').find('a').text
            descripcion = noticia.find('p')
            item.add_value('titular', titular )
            item.add_value('descripcion', descripcion.text if descripcion else 'N/A' )
            yield item.load_item()








