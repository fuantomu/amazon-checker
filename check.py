import bs4
import requests
from helper.product import Product
from random import randint

def get_soup(url):
    headers = {
        "User-Agent": f"Mozilla/6.0 (Windows NT 6.1) AppleWebKit/537.{randint(0,99)} (KHTML, like Gecko) Chrome/41.0.{randint(2000,3000)}.{randint(0,9)} Safari/537.{randint(0,99)}",
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

if __name__ == "__main__":
    url = "https://www.amazon.de/-/en/dp/B0DKFMSMYK"
    print(get_soup(url))