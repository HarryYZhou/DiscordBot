import discord
from discord.ext import commands
import dotenv
import os
import random
import functions

dotenv.load_dotenv()

# Store the token in a private .env file
token = os.getenv('TOKEN')

# Create an intents file in order to specify bot intentions
intents = discord.Intents.default()
intents.messages = True
intents.presences = True
intents.message_content = True
# Must enable guilds to access members in the server
intents.guilds = True

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
    await print("Bot has been logged out")


# Elect Team Captains (Random 2 people in the channel), must have at least 2 people in the channel
@bot.command(name='elect')
async def electCaptain(ctx):
    curChannel = functions.findChannel(ctx)
    if curChannel:
        members = functions.findMembers(curChannel)
        # Check if channel has at least 2 members
        if len(members) >= 2:
            electedCaptainA, electedCaptainB = random.sample(members, 2)
            await ctx.send(f'{electedCaptainA.display_name} has been elected as the captain of Alpha team!')
            await ctx.send(f'{electedCaptainB.display_name} has been elected as the captain of Bravo team!')
        else:
            await ctx.send('You need to get at least one friend before you elect team captains :(')
    else:
        await ctx.send('You must first join a channel before you can use this command!')

# Run the discord bot
bot.run(token)