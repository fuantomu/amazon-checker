import bs4
import requests
from helper.product import Product


def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup


def check_soup(soup):
    div_case = soup.find("div", id="availability")
    add_to_cart = soup.find("input", id="add-to-cart-button")
    delivery_date = soup.find("div", id="mir-layout-DELIVERY_BLOCK")
    check = str(div_case).lower()
    delivery_check = str(delivery_date).lower()

    if "stock" in check or (add_to_cart is not None and "delivery" in delivery_check):
        print("IN STOCK")
        return True
    return False


def get_product(url):
    soup = get_soup(url)
    return Product(soup)
