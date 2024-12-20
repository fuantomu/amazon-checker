import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from check import get_product
from helper.discord import AmazonChecker, send_discord_post, set_context
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
async def track(ctx, url, update_time_in_minutes=1, ping_on_price_change=False):
    set_context(ctx)

    await ctx.defer(ephemeral=False)
    product = get_product(url)

    await ctx.followup.send(
        embed=discord.Embed(
            title=product.title,
            url=url,
            image=product.image,
            description=f"Current Price: {product.price}",
        ),
        ephemeral=True,
    )
    await send_discord_post("Checking Availability")

    global current_check
    current_check = AmazonChecker(bot, url, update_time_in_minutes=float(update_time_in_minutes), ping_on_price_change=ping_on_price_change)


@bot.slash_command(
    name="stop",
    description="Stops the tracking",
    guild_ids=os.getenv("GUILD_IDS").split(","),
)
async def stop(ctx):
    await ctx.defer(ephemeral=False)
    global current_check
    if current_check is not None:
        await ctx.followup.send("Stopped tracking")
        current_check.cog_unload()
        current_check = None
    else:
        await ctx.followup.send("There was no tracking")
    


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Running discord bot")
        bot.run(os.getenv("BOT_TOKEN"))
