import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import aiohttp
import asyncio
import json
import logging



intents = discord.Intents.default()
load_dotenv()
token = os.getenv("TOKEN")

# show warning if token is not found
if token is None:
    raise ValueError("No token found in .env file")

# set up bot and intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# show when bot is ready and synced
@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    print("syncing slash commands...")
    try:
        await bot.sync_commands()
        print("Slash commands synced to guild")
        print("Slash commands synced")
    except Exception as e:
            print(f"Error syncing slash commands: {e}")

#Hello Slash Command
# This command responds with "Hello" when invoked.
@bot.slash_command(name="hello", description="Says hello")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello")
    return

#Random Cat Slash Command
# This command fetches a random cat image from the cataas API and sends it in an embed.
@bot.slash_command(name="meow", description="Sends a cat image")
async def meow(ctx: discord.ApplicationContext):
    await ctx.defer()
    await fetch_cat_image(ctx)

async def fetch_cat_image(ctx: discord.ApplicationContext):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cataas.com/cat?json=true", timeout=10) as resp:
                if resp.status != 200:
                    await ctx.respond("Could not fetch a cat image 😿")
                    return

                data = await resp.json()
                print("Recieved JSON:", data)  # Debugging line

                image_url = data.get("url")
                if not image_url:
                    print(f"Error: No Image path found in respojne. Data: {data}")
                    await ctx.respond("No image found")
                    return

                # Construct the final image URL
                cat_url = image_url
                print("Final cat URL:", cat_url)  # Debugging line

                embed = discord.Embed(title="Meow!")
                embed.set_image(url=cat_url)
            await ctx.respond(embed=embed)

    except asyncio.TimeoutError:
        await ctx.respond("Request timed out. Please try again later.")
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")


    
 

bot.run(token)

