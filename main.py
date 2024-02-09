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
bot.firstPicker = False
bot.secondPicker = False
bot.pickMaps = False

# Store MapData

CS_MAPS = ['Dust 2', 'Mirage', 'Inferno', 'Cache', 'Ancient', 'Anubis', 'Office', 'Vertigo', 'Overpass', 'Nuke']

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
    
    # Bot says hello
    if message.content.startswith('Hello'):
        await message.channel.send('Hello!')

    # Picking map initiated if captains are elected
    if bot.pickMaps == True:
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
        # @TODO remove line below this
        bot.electedCaptainA = members[0]
        await ctx.send(f'{bot.electedCaptainA.display_name} has been elected as the captain of Alpha team!')
    else:
        await ctx.send('You must first join a channel before you can use this command!')

    
 
"""
Function that flips a coin, used to determine who gets to pick for first/second pick
"""
@bot.command(name='coinflip')
async def coinFlip(ctx):
    await ctx.send("Flipping coin...")
    await ctx.send(random.choice(('Flipped Heads!', 'Flipped Tails!')))

"""
Function that initiates the map picking phase if two captains have been appointed.
Depending on which captain types this command, they will be able to go first. The /coinflip command can be used in conjunction with this to determine who goes first and second.
"""
@bot.command(name='pickmap')
async def pickMaps(ctx):
    if not bot.electedCaptainA and not bot.electedCaptainB:
        await ctx.send("You must first elect team captains! You can do this by typing in /elect in the chat.")
        return
    else:
        if ctx.author == bot.electedCaptainA or ctx.author == bot.electedCaptainB:
            bot.pickMaps == True
            bot.firstPicker = ctx.author
            # Assign firstPicker and secondPicker depending on who types in the /pick command
            if ctx.author == bot.electedCaptainA:
                bot.secondPicker == bot.electedCaptainB
            else:
                bot.secondPicker == bot.selectedCaptainA
            messageToSend = f"Captain {ctx.author.display_name}, please ban 3 maps from the following list (To ban a map, type the numbers in one by one):\n"
            for i in range(len(CS_MAPS)):
                
                messageToSend += f"{i+1}. {CS_MAPS[i]}\n"
            await ctx.send(messageToSend)






"""
Function that automates the whole team picking process, if possible, elect two captains and then allow those two captains to select team members. Teams are of size 10 for games like CSGO, DOTA2 and OVERWATCH.
A randomly selected captain will be asked to flip a coin. If their guess is correct, they can choose to pick first or second.
"""

# Run the discord bot
bot.run(token)