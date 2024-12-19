class Product:

    def __init__(self, soup):
        self.title = (
            soup.select_one("#productTitle").text.strip()
            if soup.select_one("#productTitle") is not None
            else None
        )
        self.image = (
            soup.select_one("#landingImage").attrs.get("src")
            if soup.select_one("#landingImage") is not None
            else None
        )
        self.price = (
            self.extract_price(soup.select_one("span.a-offscreen").text)
            if soup.select_one("span.a-offscreen") is not None
            else None
        )
        self.previous_price = None
        
    def extract_price(self, text):
        try:
            new_price = float(text[1:])
            self.previous_price = new_price
            return new_price
        except:
            if "Page" in text:
                return self.previous_price
            else:
                return text

    def __repr__(self):
        return str(self.__dict__)
