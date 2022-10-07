import nextcord
from nextcord.ext import commands
import json
import os
from dotenv import load_dotenv
import mysql.connector


def DBConnect():
    db = mysql.connector.connect(
        host='DATABASE HOSTNAME', # Edit this with your database hostname
        user='DATABASE USERNAME', # Edit this with your database username
        password='DATABASE PASSWORD', # Edit this with your database password
        database='DATABASE NAME', # Edit this with your database name
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()
    return db, cursor


PREFIX = '&' # You can edit prefix here! (You will need to add intents code to work well & verify your bot after passing 100 Servers)
client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')


@client.command(help="OWNER_COMMAND", hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.reply(f'Loaded **{extension}**!')


@client.command(help="OWNER_COMMAND", hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.reply(f'UN-Loaded **{extension}**!')


@client.command(help="OWNER_COMMAND", hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.reply(f'Reloaded **{extension}**!')


@client.command(help="OWNER_COMMAND", hidden=True)
@commands.is_owner()
async def modules(ctx):
    modulesList = []
    for filename in os.listdir('./islamBot/cogs'):
        if filename.endswith('.py'):
            modulesList.append(filename[:-3])
    embed = nextcord.Embed(title="Bot Modules", description="\n".join(
        i for i in modulesList), color=0x00FF00)
    await ctx.reply(embed=embed)


for filename in os.listdir('./islamBot/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@load.error
async def load_error(ctx, error):
    if isinstance(error, nextcord.ext.commands.errors.ExtensionAlreadyLoaded):
        error = nextcord.Embed(color=0xdf1111)
        error.add_field(
            name="ERROR", value=f"**Command Invoke Error!** This Extension is already loaded", inline=False)
        await ctx.reply(embed=error)


@unload.error
async def unload_error(ctx, error):
    if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
        error = nextcord.Embed(color=0xdf1111)
        error.add_field(
            name="ERROR", value=f"**Command Invoke Error!** This Extension is already unloaded", inline=False)
        await ctx.reply(embed=error)


client.run("YOUR APPLICATION TOKEN") # Paste your application token here
