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
Basic function to swap pickers, used for map and team election. Returns the non-current picker.
"""
def swapPickers(pickerOne, pickerTwo, currentPicker):
    if currentPicker == pickerOne:
        return pickerTwo
    elif currentPicker == pickerTwo:
        return pickerOne
    else:
        return currentPicker

"""
Function to reset global election variables
"""
def resetGlobals(bot):
    bot.electedCaptainA, bot.electedCaptainB = None, None
    bot.firstPicker, bot.secondPicker, bot.currentPicker = None, None, None
    bot.pickMaps, bot.pickPhase, bot.mapPool = False, 0, {}

"""
Function to send message to captains to pick from a map pool:
"""
def reiteratePool(currentPicker, dictToPass):
        messageToSend = f"Captain {currentPicker.display_name}, please ban 3 maps from the following list (To ban a map, type the numbers in one by one):\n"
        for key, val in dictToPass.items():
            messageToSend += f"{key}. {val}\n"
        print(messageToSend)
        return messageToSend