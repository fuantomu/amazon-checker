import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from check import get_product
from helper.discord import (
    AmazonChecker,
    set_context,
    set_current_message,
    update_embedded_post,
)
import sys

load_dotenv(override=True)

intents = discord.Intents.default() 
intents.message_content = True
bot = commands.Bot(intents=intents)

current_check = None

@bot.slash_command(
    name="track",
    description="Tracks amazon availability",
    guild_ids=os.getenv("GUILD_IDS").split(","),
)
async def track(ctx, url, time_in_minutes=0.1):
    set_context(ctx)

    await ctx.defer()
    set_current_message(await ctx.followup.send("Checking Product..."))

    product = get_product(url)
    await update_embedded_post(url, product)
    
    global current_check
    current_check = AmazonChecker(bot, url, float(time_in_minutes))

@bot.slash_command(
    name="stop_track",
    description="Stops the tracking",
    guild_ids=os.getenv("GUILD_IDS").split(","),
)
async def stop_track(ctx):
    global current_check
    if current_check is not None:
        current_check.cog_unload()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Running discord bot")
        bot.run(os.getenv("BOT_TOKEN"))
