from helper.product import Product
from discord import Embed

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
