import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from check import get_product, schedule_check, get_result, reset_available
from helper.discord import (
    set_context,
    set_current_message,
    update_discord_post,
    update_embedded_post,
)
import sys
from time import sleep
import datetime

load_dotenv(override=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)


@bot.slash_command(
    name="track",
    description="Tracks amazon availability",
    guild_ids=os.getenv("GUILD_IDS").split(","),
)
async def track(ctx, url, time_in_minutes=0.1, role=None):
    set_context(ctx)
    await ctx.defer()
    set_current_message(await ctx.followup.send("Checking Product..."))

    product = get_product(url)
    await update_embedded_post(url, product)

    await update_discord_post(f"Last check at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Current Price: {product.price}")

    thread = schedule_check(url, float(time_in_minutes))

    while get_result() == 0:
        product = get_product(url)
        current_msg = f"Last check at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Current Price: {product.price}"
        print(current_msg)
        await update_discord_post(current_msg)
        sleep(time_in_minutes * 60 + 1)
    
    reset_available()
    if thread is not None:
        thread.set()

    await update_discord_post(
        f"IT'S AVAILABLE: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} at {product.price}"
    )

    if role is not None:
        await ctx.send(f"<@&{role}>")
    else:
        await ctx.send(f"<@{ctx.user.id}>")
    set_current_message(None)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Running discord bot")
        bot.run(os.getenv("BOT_TOKEN"))
