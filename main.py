import discord
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

# Start the discord client
client = discord.Client(intents=intents)

# Log if the discord bot has logged in correctly
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Test function ("Hello")
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Run the discord bot
client.run(token)