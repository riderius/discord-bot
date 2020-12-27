from settings import TOKEN
import discord
from loguru import logger

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
        await message.channel.send(message.content.replace('!echo', ''))
        logger.info('Echo print by: ' + str(message.author) + '\n Sended echo message: ' + message.content.replace('!echo', ''))

@logger.catch
def main():
    logger.info('Version: 0.0.1')
    logger.info('Version dircord.py: ' + discord.__version__)
    client.run(TOKEN)


main()
