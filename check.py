import threading
import bs4
import requests
import schedule
from time import sleep
from helper.product import Product


available = False


def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup


def check(soup):
    div_case = soup.find("div", id="availability")
    add_to_cart = soup.find("input", id="add-to-cart-button")
    delivery_date = soup.find("div", id="mir-layout-DELIVERY_BLOCK")
    check = str(div_case).lower()
    delivery_check = str(delivery_date).lower()

    if "stock" in check or (add_to_cart is not None and "delivery" in delivery_check):
        global available
        print("IN STOCK")
        available = True


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                global available
                if get_result():
                    available = False
                    break
                sleep(interval * 60 + 1)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def schedule_check(url, time_in_minutes=1):
    global available
    soup = get_soup(url)
    check(soup)

    if get_result():
        pass
    else:
        schedule.every(time_in_minutes).minutes.do(check, soup)
        return run_continuously()


def get_result():
    global available
    return available

def reset_available():
    global available
    available = False

def get_product(url):
    soup = get_soup(url)
    return Product(soup)
