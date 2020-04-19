import requests
from bs4 import BeautifulSoup as bs


session = requests.session()
endpoint = "https://www.supremenewyork.com/shop/all/sweatshirts"
response = session.get(endpoint)
soup = bs(response.text, "html.parser")
container = soup.find(id='container')
inner_article = (container.find_all(class_='inner-article'))
product_name = (container.find_all(class_='product-name'))
product_style = (container.find_all(class_='product-style'))
links = [item.find('a')['href'] for item in inner_article]
names = [item.find('a').get_text() for item in product_name]
colors = [item.find('a').get_text() for item in product_style]

print(names)