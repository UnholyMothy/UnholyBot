import discord
import dotenv
from dotenv import load_dotenv
import os
from discord.ext import commands
import logging



intents = discord.Intents.default()
load_dotenv()
token = os.getenv("TOKEN")

# show warning if token is not found
if token is None:
    raise ValueError("No token found in .env file")

# set up bot and intents
intents = discord.Intents.default()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

@bot.slash_command(name="hello", description="Says hello")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello")
    return

bot.run(token)

