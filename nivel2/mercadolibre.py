from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20,
        'FEED_EXPORT_FIELDS': ['titulo', 'precio', 'descripcion'],
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    download_delay = 1
    allowed_domains = ['listado.mercadolibre.com.ec', 'articulo.mercadolibre.com.ec']
    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/perros-de-raza/perros_NoIndex_True']
    rules = (
        #* Paginación
        Rule(LinkExtractor(allow=r'^/perros(?:_Desde_\d+)?_NoIndex_True$')),

        #* Detalle de los productos
        Rule(LinkExtractor(allow=r'/MEC-'), follow=True, callback='parse_items')
    )

    def limpiarTexto(self, texto):
        nuevoTexto = texto.replace('\n', '').replace('\r', '').replace('\t', '').strip()
        return nuevoTexto

    def parse_items(self, response):        
        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo', '//h1/text()', MapCompose(self.limpiarTexto))
        item.add_xpath('precio', '//div[@id="price"]//span[@class="andes-money-amount__fraction"]/text()', MapCompose(self.limpiarTexto))
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()')
        yield item.load_item()

    

