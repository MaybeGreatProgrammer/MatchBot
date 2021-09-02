from discord.ext import commands

from utils import allowlist, backend_commands, error_handler, config

import discord
from discord.ext.commands import Bot

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().default()
intents.members = True

bot = Bot(command_prefix="!",
          intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="DM me! | !start"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    if not os.path.isfile(config.db_path):
        await backend_commands.create_default_tables()
        print('Built DB')
    allowlist.load()
    print('------')


@bot.event
async def on_command_error(context: commands.Context, error: commands.CommandError):
    if hasattr(context.command, 'on_error'):
        return
    await error_handler.handle_error(context, error)


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(TOKEN)
