from discord.ext import commands, tasks

current_message = None
context = None


def set_context(ctx):
    global context
    context = ctx


def set_current_message(msg):
    global current_message
    current_message = msg


async def update_discord_post(msg):
    global current_message
    if current_message is not None:
        current_message = await current_message.edit(content=msg)


async def send_discord_post(msg):
    global context
    global current_message
    if context is not None:
        if current_message is None:
            current_message = await context.send(f"{msg}")
        else:
            await context.send(f"{msg}")


from check import check_soup, get_soup, get_product
from datetime import datetime


class AmazonChecker(commands.Cog):

    def __init__(self, bot, url, update_time_in_minutes=1.0, ping_on_price_change=True):
        self.update_loop_time = update_time_in_minutes
        self.url = url
        self.bot = bot
        self.soup = get_soup(self.url)
        self.start_time = None
        self.last_price = None
        self.first_check = True
        self.ping_on_price_change = ping_on_price_change
        self.check.start()

    def cog_unload(self):
        self.check.cancel()

    @tasks.loop(seconds=30.0)
    async def check(self):
        product = get_product(self.url)
        current_time = datetime.now()
        current_msg = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Current Price: €{product.price}"

        if check_soup(self.soup) == 0:
            print(f"Last check at: {current_msg} - Not in stock")
            
            time_difference = current_time-self.start_time
            if self.first_check:
                await update_discord_post(f"Last check at: {current_msg} - Not in stock")
                self.first_check = False
            if time_difference.total_seconds() >= self.update_loop_time * 60.0:
                self.start_time = datetime.now()
                await update_discord_post(f"Last check at: {current_msg} - Not in stock")
            if product.price != self.last_price and self.last_price is not None:
                global context
                await send_discord_post(f"{'<@{context.user.id}>'if self.ping_on_price_change else ''}\nPrice has changed from €{self.last_price} to €{product.price}")
        else:
            await update_discord_post(f"IT'S AVAILABLE: {current_msg}")
            self.cog_unload()
            global context
            await send_discord_post(f"<@{context.user.id}>")
            set_current_message(None)
        self.last_price = product.price

    @check.before_loop
    async def before_check(self):
        print("waiting...")
        await self.bot.wait_until_ready()
        self.start_time = datetime.now()
