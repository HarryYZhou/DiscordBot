# Basic function to find the current channel of a user, return None if user not in channel
def findChannel(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        return ctx.author.voice.channel
    return None
    
# Basic function to get all members in a voice channel, return None if no members in channel
def findMembers(chnl):
    return chnl.members