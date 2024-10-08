import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
respuesta = requests.get(url, headers=headers)
soup = BeautifulSoup(respuesta.text, 'lxml')
lista_de_noticias = soup.find_all('tr', class_='athing')
for noticia in lista_de_noticias:
    titulo = noticia.find('span', class_='titleline').text
    url = noticia.find('span', class_='titleline').find('a').get('href')
    metadata = noticia.find_next_sibling()
    score = 0
    comentarios = 0
    try:
        score_tmp = metadata.find('span', 'score').text
        score_tmp = score_tmp.replace('points', '').replace('point', '').strip()
        score = int(score_tmp)
    except:
        print('No hay score')
    try:
        comentarios_tmp = metadata.find('span', attrs={'class': 'subline'}).text
        comentarios_tmp = comentarios_tmp.split('|')[-1]
        comentarios_tmp = comentarios_tmp.replace('comments', '').replace('comment', '').strip()        
        comentarios = int(comentarios_tmp)
    except:
        print('No hay comentarios')

    print(titulo)
    print(url)
    print(score)
    print(comentarios)
    print()
