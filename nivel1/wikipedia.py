import requests
from lxml import html

encabezados = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = 'https://www.wikipedia.org/'
respuesta = requests.get(url, headers=encabezados)
respuesta.encoding = 'utf-8'
parser = html.fromstring(respuesta.text)

# ingles = parser.get_element_by_id('js-link-box-en')
# print(ingles.text_content())

# idiomas = parser.xpath('//div[contains(@class, "central-featured-lang")]//strong/text()')
# for idioma in idiomas:
#     print(idioma)

idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())
