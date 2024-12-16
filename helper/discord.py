from helper.product import Product
from discord import Embed
from discord.ext import commands, tasks

current_message = None
context = None


def set_context(ctx):
    global context
    context = ctx


def set_current_message(msg):
    global current_message
    current_message = msg


async def update_embedded_post(url, product: Product):
    global current_message
    if current_message is not None:
        embedded_msg = Embed(
            title=product.title,
            url=url,
            image=product.image,
            description=f"Current Price: {product.price}",
        )
        await current_message.edit(embed=embedded_msg)


async def update_discord_post(msg):
    global current_message
    if current_message is not None:
        await current_message.edit(content=msg)


async def send_discord_post(msg):
    global context
    if context is not None:
        await context.send(f"{msg}")


from check import check_soup, get_soup, get_product
from datetime import datetime


class AmazonChecker(commands.Cog):
    loop_time = 1.0

    def __init__(self, bot, url, time_in_minutes=1.0):
        global loop_time
        loop_time = time_in_minutes
        self.url = url
        self.bot = bot
        self.soup = get_soup(self.url)
        self.check.start()

    def cog_unload(self):
        self.check.cancel()

    @tasks.loop(minutes=loop_time)
    async def check(self):
        product = get_product(self.url)
        current_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Current Price: {product.price}"
        await update_discord_post(current_msg)

        if check_soup(self.soup) == 0:
            print(f"Last check at: {current_msg}")
            await update_discord_post(f"Last check at: {current_msg}")
        else:
            await update_discord_post(f"IT'S AVAILABLE: {current_msg}")
            self.cog_unload()

    @check.before_loop
    async def before_check(self):
        print("waiting...")
        await self.bot.wait_until_ready()
        
    @check.after_loop
    async def after_check(self):
        global context
        await context.send(f"<@{context.user.id}>")
        set_current_message(None)
