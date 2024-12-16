class Product:

    def __init__(self, soup):
        self.title = soup.select_one("#productTitle").text.strip()
        self.image = soup.select_one("#landingImage").attrs.get("src")
        self.price = (
            soup.select_one("span.a-offscreen").text
            if soup.select_one("span.a-offscreen") is not None
            else None
        )

    def __repr__(self):
        return str(self.__dict__)
