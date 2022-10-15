import requests
from bs4 import BeautifulSoup

string = input('¿Qué quieres buscar?')
r = requests.get('https://listado.mercadolibre.com.ec/{}#D[A:{}]'.format(string.replace(' ', '-'), string))
contenido = r.content

soup = BeautifulSoup(contenido, 'html.parser')

# Última página
try:
    last_page = soup.find('li', {'class': 'andes-pagination__page-count'}).text
    last_page_modified = int(last_page.replace('de ',''))
except:
    pass

# Array para añadir los objetos
products_array = []

for page in range(0, last_page_modified):
    
    initial_result = requests.get('https://listado.mercadolibre.com.ec/{}_Desde_{}_NoIndex_True'.format(string.replace(' ', '-'), (page*50)+1))
    content_pagination = initial_result.content
    
    soup_pagination = BeautifulSoup(content_pagination, 'html.parser')
    
    alldivs = soup_pagination.find_all('div', {'class': 'andes-card'})
    
    for item in alldivs:
        data = {}
        data['nombre articulo'] = item.find('h2', {'class': 'ui-search-item__title'}).text
        data['precio'] = item.find('span', {'class': 'price-tag-amount'}).text
        try:
            data['link'] = item.find('a', {'class': 'ui-search-result__content'})['href']
        except: 
            data['link'] = item.find('a', {'class': 'ui-search-link'})['href']

        products_array.append(data)

print(len(products_array))

import pandas
df = pandas.DataFrame(products_array)

# Guardar los resultados obtenidos en csv
df.to_csv("listado_mercado_libre_{}.csv".format(string))
