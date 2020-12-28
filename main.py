"""Main file the discord bot"""

import asyncio
import discord
from loguru import logger
from settings import TOKEN

__version__ = '0.2.0'

logger.add('DEBUG.log', format='{time} {level} {message}',
           level='DEBUG', rotation='8 MB', compression='zip')

client = discord.Client()


@logger.catch
@client.event
async def on_ready() -> None:
    """This function log about connected account"""

    logger.info('We have logged in as {0.user}'.format(client))


@logger.catch
@client.event
async def on_message(message) -> None:
    """This function use messages related events"""

    if message.author == client.user:
        return

    # Command hello
    if message.content.startswith('!hello'):
        await message.channel.send('Hello, ' + str(message.author.mention) + '!')
        logger.info('Hello print by: ' + str(message.author))

    # Command echo
    if message.content.startswith('!echo'):
        await message.channel.send(message.content.replace('!echo ', ''))
        logger.info('Echo print by: ' + str(message.author) +
                    '\n Sended echo message: ' + message.content.replace('!echo', ''))

    # Command type
    if message.content.startswith('!type'):
        original_message = message.content.replace('!type ', '')
        logger.info('Type print by: ' + str(message.author) +
                    '\nOriginal message: ' + original_message)
        number_symbol_in_message = len(original_message)
        sending_message = '▒'*number_symbol_in_message
        editon_message = await message.channel.send('Message by ' + str(message.author.mention) +
                                                    ': ' + sending_message)
        normal_message = ''
        await message.delete()
        for opened_symbols in range(number_symbol_in_message):
            opened_message = list(original_message)
            normal_message += opened_message[opened_symbols]
            sending_message = 'Message by ' + \
                str(message.author.mention) + ': ' + normal_message + \
                '▒'*(number_symbol_in_message-opened_symbols)
            await asyncio.sleep(0.05)
            await editon_message.edit(content=sending_message)
        end_message = 'Message by ' + \
            str(message.author.mention) + ': ' + normal_message
        await editon_message.edit(content=end_message)
        logger.info('End message: ' + end_message)


@logger.catch
def main() -> None:
    """Main function in the discord bot"""

    logger.info('Version: ' + __version__)
    logger.info('Version dircord.py: ' + discord.__version__)
    client.run(TOKEN)


main()
