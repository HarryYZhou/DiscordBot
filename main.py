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

functions.resetGlobals(bot)

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
    - If pick phase initiated:
        If a captain is currently picking, they will be prompted to ban maps.
        After there is one map left, that map will be selected as the map to play.
        If anything other than an index is entered, nothing will happen.
        Cannot exit pick phase until it is completed. @TODO Allow early termination of pick phase
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
        if bot.firstPicker or bot.secondPicker:
            if message.author == bot.currentPicker:
                if bot.pickPhase > 0:               
                    if message.content in bot.mapPool:
                        mapBanned = bot.mapPool.pop(message.content)
                        print(bot.mapPool)
                        await message.channel.send(f'Banned {mapBanned}')
                        # When 3 maps are banned, swap pickers
                        if len(bot.mapPool) == len(CS_MAPS) - 3:
                            bot.currentPicker = functions.swapPickers(bot.firstPicker, bot.secondPicker, bot.currentPicker)
                            await message.channel.send(functions.reiteratePool(bot.currentPicker, bot.mapPool))
                        # When 3 maps are banned again, swap pickers
                        elif len(bot.mapPool) == len(CS_MAPS) - 6:
                            bot.currentPicker = functions.swapPickers(bot.firstPicker, bot.secondPicker, bot.currentPicker)
                            await message.channel.send(functions.reiteratePool(bot.currentPicker, bot.mapPool))
                        # When 2 maps are banned, swap pickers
                        elif len(bot.mapPool) == len(CS_MAPS) - 8:
                            bot.currentPicker = functions.swapPickers(bot.firstPicker, bot.secondPicker, bot.currentPicker)
                            await message.channel.send(functions.reiteratePool(bot.currentPicker, bot.mapPool))
                if len(bot.mapPool) == 1:
                    for key in bot.mapPool:
                        await message.channel.send(f'The chosen map is {bot.mapPool[key]}!')
                    # After a map is picked, reset all bot variables to default levels
                    functions.resetGlobals(bot)


    # Need to process commands to avoid breaking command functionality\
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
Function will reset all bot variables, should be used to elect new captains, new teams and a new map.
Return - The two elected capatins
"""
@bot.command(name='elect')
async def electCaptain(ctx):
    functions.resetGlobals(bot)
    curChannel = functions.findChannel(ctx)
    if curChannel:
        members = functions.findMembers(curChannel)
        # @TODO, fix captain process after testing is completed
        if len(members) >= 2:
            bot.electedCaptainA, bot.electedCaptainB = random.sample(members, 2)
            await ctx.send(f'{bot.electedCaptainA.display_name} has been elected as the captain of Alpha team!')
            await ctx.send(f'{bot.electedCaptainB.display_name} has been elected as the captain of Bravo team!')
        else:
            await ctx.send('You need to get at least one friend before you elect team captains :(')
        # bot.electedCaptainA = random.choice(members)

        # await ctx.send(f'{bot.electedCaptainA.display_name} has been elected as the captain of Alpha team!')
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
    if bot.pickMaps == True:
        await ctx.send("You are already in the pick phase!")
        return
    else:
        if ctx.author == bot.electedCaptainA or ctx.author == bot.electedCaptainB:
            bot.firstPicker = ctx.author
            # Assign firstPicker and secondPicker depending on who types in the /pick command
            if ctx.author == bot.electedCaptainA:
                bot.secondPicker = bot.electedCaptainB
            else:
                bot.secondPicker = bot.electedCaptainA
            bot.pickMaps = True
            bot.currentPicker = bot.firstPicker
            bot.pickPhase = 1
            # Create a dictionary to store all maps and their values
            for i in range(len(CS_MAPS)):
                bot.mapPool[str(i + 1)] = CS_MAPS[i]
            messageToSend = functions.reiteratePool(ctx.author, bot.mapPool)
            await ctx.send(messageToSend)

# Run the discord bot
bot.run(token)