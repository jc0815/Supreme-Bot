import requests
from bs4 import BeautifulSoup
from config import *

# TODO: parse names of future releases
session = requests.session()
url = "https://www.supremenewyork.com/shop/all/sweatshirts"
response = session.get(url)

bs = BeautifulSoup(response.text, "html.parser")
container = bs.find(id = "container")

articles_containers = container.find_all(class_ = "inner-article")
product_names_containers = container.find_all(class_ = "product-name")
product_styles_containers = container.find_all(class_ = "product-style")

product_links = [article.find("a")["href"] for article in articles_containers]
names = [product_name.find("a").get_text() for product_name in product_names_containers]
colours = [product_style.find("a").get_text() for product_style in product_styles_containers]

print("Product names: ", names)