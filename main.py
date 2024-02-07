import discord
from discord.ext import commands
import dotenv
import os
import random
import functions

# Load the .env file storing the bot's token details
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

# Store Global Captain variables for future use
bot.electedCaptainA = None
bot.electedCaptainB = None

# Store MapData

CS_MAPS = ['Dust 2', 'Mirage', 'Inferno', 'Cache', 'Ancient']

"""
Function that alerts the administrator that the bot has logged in correctly
"""
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

"""
Function that handles all potential message commands sent into the chat
    - If Hello is typed in the chat, the bot will respond with Hello! back
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('Hello'):
        await message.channel.send('Hello!')

    if message.author == bot.electedCaptainA:
        if message.content.startswith('pick'):
            mapChosen = False
            mapsAvailable = CS_MAPS.copy()
            while mapChosen == False:
                print("Reached here")
                await message.channel.send("Picked map!")
                await bot.process_commands(message)
                return

    # Need to process commands to avoid breaking command functionality
    await bot.process_commands(message)

"""
Function that shuts down the bot, only to be used for testing or if a bug occurs
"""
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    # Send a message indicating that the bot is shutting down
    await ctx.send('Shutting down TeamPicker!')
    await bot.close()
    await print("Bot has been logged out")

"""
Function that selects 2 team captains from a channel that the user is in if they type in the command.
If the user is not in a channel, the user will be prompted to join a channel.
If the user is in a channel, but there is only one user in that specific channel, the user will be mildly insulted.
Return - The two elected capatins
"""
@bot.command(name='elect')
async def electCaptain(ctx):
    curChannel = functions.findChannel(ctx)
    if curChannel:
        members = functions.findMembers(curChannel)
        # Check if channel has at least 2 members
        # @TODO UNCOMMENT THIS LATER, KEEP IT COMMENTED FOR TESTING PURPOSES
        # if len(members) >= 2:
        #     bot.electedCaptainA, bot.electedCaptainB = random.sample(members, 2)
        #     await ctx.send(f'{bot.electedCaptainA.display_name} has been elected as the captain of Alpha team!')
        #     await ctx.send(f'{bot.electedCaptainB.display_name} has been elected as the captain of Bravo team!')
        # else:
        #     await ctx.send('You need to get at least one friend before you elect team captains :(')
        bot.electedCaptainA = members[0]
        await ctx.send(f'{bot.electedCaptainA.display_name} has been elected as the captain of Alpha team!')
    else:
        await ctx.send('You must first join a channel before you can use this command!')

    
    

                



"""
Function that automates the whole team picking process, if possible, elect two captains and then allow those two captains to select team members. Teams are of size 10 for games like CSGO, DOTA2 and OVERWATCH.
A randomly selected captain will be asked to flip a coin. If their guess is correct, they can choose to pick first or second.
"""

# Run the discord bot
bot.run(token)