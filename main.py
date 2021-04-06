"""Main file the discord bot"""

import sys
import asyncio
import sqlite3 as sql
import discord
from loguru import logger
from settings import TOKEN

__version__ = "0.5-dev3"
__author__ = "RIDERIUS"

# pylint settings:
# pylint: disable=C0301

RIDERIUS_ICON_URL = "https://cdn.discordapp.com/avatars/518031210644242433/81e47876e62fac858786b893bdd3c5b9.png"

logger.add(
    "DEBUG.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="8 MB",
    compression="zip",
    encoding="utf-8",
)

client = discord.Client()


@logger.catch
def database(accound_id: int, time_in_voice: float):
    """
    database - function for working with a database

    Args:
        accound_id (int): this is the variable that stores the ID of the Discord account
        time_in_voice (float): it is a variable that stores the number of minutes in voice channels
    """

    connection = sql.connect("database.db")

    cursor = connection.cursor()

    try:
        cursor.execute("CREATE TABLE stocks (id TEXT, time_in_voice REAL)")
    except sql.OperationalError:
        pass

    data = (round(time_in_voice / 60, 1), accound_id)

    cursor.execute("Update stocks set time_in_voice = ? where id = ?", data)

    # accound_id = input('Enter the account id: ')
    # time_in_voice = input('Enter the time in voice: ')

    # cursor.execute(
    #     f"INSERT INTO stocks VALUES ('{accound_id}','{time_in_voice}')")

    connection.commit()

    cursor.execute("SELECT * FROM `stocks`")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], row[1])

    connection.close()


@logger.catch
@client.event
async def on_member_join(member):
    """This feature is only triggered if a member joins the server"""

    connection = sql.connect("database.db")

    cursor = connection.cursor()

    try:
        cursor.execute("CREATE TABLE stocks (id TEXT, time_in_voice REAL)")
    except sql.OperationalError:
        pass

    cursor.execute(f"INSERT INTO stocks VALUES ('{member.id}','0.0')")

    connection.commit()

    cursor.execute("SELECT * FROM `stocks`")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], row[1])

    connection.close()


@logger.catch
@client.event
async def on_ready() -> None:
    """This function log about connected account"""

    logger.info("We have logged in as {0.user}".format(client))
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game("!manual | v" + __version__)
    )


@logger.catch
@client.event
async def on_message(message) -> None:
    """This function use messages related events"""

    if message.author == client.user:
        return

    # Command hello or hi
    if message.content.startswith("!hello") or message.content.startswith("!hi"):
        await message.channel.send("Hello, " + str(message.author.mention) + "!")
        logger.info("Hello print by: " + str(message.author))

    # Command echo
    if message.content.startswith("!echo"):
        await message.delete()
        await message.channel.send(message.content.replace("!echo ", ""))
        logger.info(
            "Echo print by: "
            + str(message.author)
            + "\n Sended echo message: "
            + message.content.replace("!echo", "")
        )

    # Command type
    if message.content.startswith("!type"):
        original_message = message.content.replace("!type ", "")
        logger.info(
            "Type print by: "
            + str(message.author)
            + "\nOriginal message: "
            + original_message
        )
        number_symbol_in_message = len(original_message)
        sending_message = "▒" * number_symbol_in_message
        editon_message = await message.channel.send(
            "Message by " + str(message.author.mention) + ": " + sending_message
        )
        normal_message = ""
        await message.delete()
        for opened_symbols in range(number_symbol_in_message):
            opened_message = list(original_message)
            normal_message += opened_message[opened_symbols]
            sending_message = (
                "Message by "
                + str(message.author.mention)
                + ": "
                + normal_message
                + "▒" * (number_symbol_in_message - opened_symbols)
            )
            await asyncio.sleep(0.05)
            await editon_message.edit(content=sending_message)
        end_message = (
            "Message by " + str(message.author.mention) + ": " + normal_message
        )
        await editon_message.edit(content=end_message)
        logger.info("End message: " + end_message)

    # Command voice
    if message.content.startswith("!voice"):
        # user_id = message.author.id
        # user = await client.fetch_user(user_id)
        # user = <class 'discord.user.User'>
        logger.info("Voice print by: " + str(message.author))
        # database(user_id, 0.0)

    # Command profile
    # if message.content.startswith("!profile"):
    #     user_id = message.author.id
    #     user = await client.fetch_user(user_id)
    #     member = discord.ext.commands.MemberConverter(user)
    #     logger.debug(member, "\n", type(member))
    #     user = await client.fetch_user(user_id)
    #     user = <class 'discord.user.User'>
    #     profile = discord.Embed(
    #         title="Профиль" + str(message.author),
    #         description=f"""Nickname: {message.author}
    #         id: {message.author.id}
    #         Дата создания аккаунта: {user.created_at()}
    #         Дата входа на сервер: """,
    #     )
    #     await message.channel.send(embed=profile)

    # Command manual
    if message.content.startswith("!manual"):
        manual = discord.Embed(
            title="Bot manual",
            description="""!manual - displays the manual for the bot
            !type - Encrypts the message for a while
            !echo - repeats the message
            !hello | !hi - greets the caller""",
        )
        manual.set_author(
            name="RIDERIUS",
            url="https://github.com/riderius",
            icon_url=RIDERIUS_ICON_URL,
        )
        await message.channel.send(embed=manual)
        logger.info("Manual print by: " + str(message.author))


@logger.catch
def main() -> None:
    """Main function in the discord bot"""

    logger.info("Version bot: " + __version__)
    logger.info("OS: " + sys.platform)
    logger.info("Python version: " + sys.version)
    logger.info("Version dircord.py: " + discord.__version__)
    logger.info("Version sqlite3: " + sql.sqlite_version)
    client.run(TOKEN)


main()
