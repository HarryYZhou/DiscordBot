import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

# Store the token in a private .env file
token = os.getenv('TOKEN')

# Create an intents file in order to specify bot intentions
intents = discord.Intents.default()
intents.messages = True
intents.presences = True
intents.message_content = True

# Intialize the discord bot with the defined intents
bot = commands.Bot(command_prefix = '/', intents = intents)

# Log if the discord bot has logged in correctly
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


# Test function ("Hello")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('Hello'):
        await message.channel.send('Hello!')

    # Need to process commands to avoid breaking command functionality
    await bot.process_commands(message)

# Allow owner/admin to shutdown the bot
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    # Send a message indicating that the bot is shutting down
    await ctx.send('Shutting down TeamPicker!')
    await bot.close()
    print("Bot has been logged out")

# Run the discord bot
bot.run(token)

