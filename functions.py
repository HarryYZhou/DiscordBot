"""
Basic function to find the current voice channel of a user, return None if user not in a voice channel
"""
def findChannel(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        return ctx.author.voice.channel
    return None
    
"""
Basic function to get all members in a voice channel, return None if no members in channel
"""
def findMembers(chnl):
    return chnl.members

"""
Basic function to swap pickers, used for map and team election
"""
def swapPickers(pickerOne, pickerTwo, currentPicker):
    if currentPicker == pickerOne:
        currentPicker = pickerTwo
    elif currentPicker == pickerTwo:
        currentPicker = pickerOne

"""
Function to reset global election variables
"""
def resetGlobals(bot):
    bot.electedCaptainA, bot.electedCaptainB = None, None
    bot.firstPicker, bot.secondPicker, bot.currentPicker = None, None, None
    bot.pickMaps, bot.pickPhase, bot.mapPool = False, 0, {}