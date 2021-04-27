"""Main file the discord bot"""

import sys
import os
import discord
from discord.ext import commands
from loguru import logger
from settings import DEFAULT_ROLE, TOKEN

__version__ = "0.7.0"

# pylint settings:
# pylint: disable=C0301
# pylint: disable=E1101

logger.add(
    "DEBUG.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="8 MB",
    compression="zip",
    encoding="utf-8",
)

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@logger.catch
@client.event
async def on_ready():
    """
    on_ready - This code is executed immediately after starting the bot.
    """
    logger.info("We have logged in as {0.user}".format(client))
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"!manual | v{__version__} | https://discord.gg/CvswN4t"),
    )


@logger.catch
@client.event
async def on_member_join(member):
    """This feature is only triggered if a member joins the server"""
    role = discord.utils.get(member.guild.roles, id=int(DEFAULT_ROLE))
    await member.add_roles(role)
    logger.info(f"{member} joined to server! Role: {role.id}")


@logger.catch
@client.command(pass_content=True)
async def manual(ctx):
    """!manual - displays the manual for the bot"""
    author = ctx.message.author
    manual_as_an_embed = discord.Embed(
        title="Bot manual",
        description="""!manual - displays the manual for the bot
        !echo - repeats the message
        !hello - greets the caller
        !clear [arg] - deletes messages, replace [arg] with the number of messages to delete
        !kick - for kick user
        !ban - for ban user""",
    )
    manual_as_an_embed.set_author(
        name="RIDERIUS",
        url="https://github.com/riderius",
        icon_url="https://cdn.discordapp.com/avatars/518031210644242433/81e47876e62fac858786b893bdd3c5b9.png",
    )
    await ctx.send(embed=manual_as_an_embed)
    logger.info("!Manual print by: " + str(author))


@logger.catch
@client.command(pass_content=True)
async def hello(ctx):
    """!hello - greets the caller"""
    author = ctx.message.author
    await ctx.send("Hello, " + str(author.mention) + "!")
    logger.info("!Hello print by: " + str(author))


@logger.catch
@client.command(pass_content=True)
async def echo(ctx, *arg):
    """!echo - repeats the message"""
    author = ctx.message.author
    await ctx.channel.purge(limit=1)
    await ctx.send(f'Message from {author.mention}: {" ".join(arg)}')
    logger.info(
        f'!Echo print by: {ctx.message.author}\nSended echo message: {" ".join(arg)}'
    )


@logger.catch
@client.command(pass_content=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=0):
    """!clear [arg] - deletes messages, replace [arg] with the number of messages to delete."""
    logger.info(f"!clear print by: {ctx.message.author}\namount = {amount}")
    if amount == 0:
        await ctx.send(
            "Add an argument to the command. The argument is the number of messages to delete. Example command: !Clear 5. The example demonstrates a command that will delete 5 messages."
        )
    else:
        await ctx.channel.purge(limit=amount)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """!kick - for kick user"""
    await member.kick(reason=reason)
    await ctx.send(f"Kick user {member.mention}. Reason {reason}")
    logger.info(
        f"User kicked {member.mention}\nReason: {reason} \n!kick print by: {ctx.message.author}"
    )


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """!ban - for ban user"""
    await member.ban(reason=reason)
    await ctx.send(f"Ban user {member.mention}. Reason {reason}")
    logger.info(
        f"User banned {member.mention}\nReason: {reason} \n!ban print by: {ctx.message.author}"
    )


@logger.catch
def main() -> None:
    """Main function in the discord bot"""

    logger.info("Version bot: " + __version__)
    logger.info("OS: " + sys.platform)
    if sys.platform == "linux":
        logger.info(f"Uname: {os.uname()}")
    logger.info("Python version: " + sys.version)
    logger.info("Version discord.py: " + discord.__version__)
    client.run(TOKEN)


main()
