import asyncio
from asyncio.tasks import sleep
from settings import TOKEN
import discord
from loguru import logger

__version__ = '0.0.2'

logger.add('DEBUG.log', format='{time} {level} {message}',
           level='DEBUG', rotation='8 MB', compression='zip', enqueue=True, backtrace=True, diagnose=True)

client = discord.Client()


@logger.catch
@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))


@logger.catch
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, ' + str(message.author.mention) + '!')
        logger.info('Hello print by: ' + str(message.author))

    if message.content.startswith('!echo'):
        await message.channel.send(message.content.replace('!echo ', ''))
        logger.info('Echo print by: ' + str(message.author) +
                    '\n Sended echo message: ' + message.content.replace('!echo', ''))

    if message.content.startswith('!type'):
        logger.info('Type print by: ' + str(message.author))
        original_message = message.content.replace('!type ', '')
        logger.info('Original message: ' + original_message)
        number_symbol_in_message = len(original_message)
        sending_message = '▒'*number_symbol_in_message
        editon_message = await message.channel.send('Message by ' + str(message.author.mention) + ': ' + sending_message)
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
def main():
    logger.info('Version: ' + __version__)
    logger.info('Version dircord.py: ' + discord.__version__)
    client.run(TOKEN)


main()
