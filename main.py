import discord
import asyncio
from discord.ext import commands
import aiohttp
from github import getCommits
from discord.utils import get
from gofundme import getDonations
from hours import getHours
from money import getMoney
from go import getAll
from badwords import arrBad

TOKEN = open("token.txt").readlines()[0].strip()
ADMINUSERSID = [509895698330943497, 270778324861583362, 146276564726841344, 250059159381344256, 542835636588118036, 398399749192941568]
warnings = {}

vote = {}
voted = {}
voteOwner = {}
owner = ["bananajojo#4243"]


categories = ["Name: ", "Build Season Hours: ", "Travel Requirements: ", "Letter Requirements: ", "Fundraising Hours: ", "Additional Hours: ", "Volunteering w/ FIRST Event: ", "Volunteer Hours: ", "Fundraising Amount: "]

prefix = "~"
client = discord.Client()
# @client.event
# async def on_message(message):
#     m = message.content.lower()
#     if m == "jk":
#         await client.send_message(message.channel, "THAT'S NOT OK TO SAY!")
bot = commands.Bot(command_prefix=prefix, description="Having Fun")



# SKILLZ

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	global warnings, ADMINUSERSID
	message.content = message.content.lower()
	messageStuff = message.content.split(" ")
	for i in messageStuff:
		if i in arrBad and str(message.author.display_name) != "Marwin":
			if(message.author.id not in warnings):
				warnings[message.author.id] = 1
			else:
				warnings[message.author.id] += 1
			await bot.send_message(bot.get_channel("544377549367672842"), message.author.mention + " recieved a warning. Reason: Bad Word. Message: " + str(message.content))
			await bot.send_message(message.channel, message.author.mention + " said a bad word. They have recieved a warning! They have " + str(warnings[message.author.id]) + " warnings!")
			await bot.delete_message(message)
			if(warnings[message.author.id] > 5):
				for i2 in ADMINUSERSID:
					user = await bot.get_user_info(i2)
					await bot.send_message(user, message.author.display_name + " has recieved " + str(warnings[message.author.id]-1) + " warnings. All future warnings will now be reported!")
	

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	print(discord.utils.oauth_url(bot.user.id))

@bot.command(pass_context=True, hidden=True)
async def setname(ctx, *, name:str):
    if ctx.message.author.id not in owner:
        return
    name = name.strip()
    if name != "":
        try:
            await bot.edit_profile(username=name)
        except:
            await bot.say("Failed to change name")
        else:
            await bot.say("Successfuly changed name to {}".format(name))
    else:
        await bot.send_cmd_help(ctx)


@bot.command(pass_context=True, no_pm=True, hidden=True)
async def prefix(ctx, *, prefixSet:str):
	""" Changing the Prefix (ADMIN ONLY) """
	global bot, ADMINUSERSID, warnings
	u = str(ctx.message.author.id)
	if(u in ADMINUSERSID):
		bot.command_prefix = prefixSet
		await bot.reply("Changed Prefix to: " + prefixSet.strip() + " They are a freaking god!")
	else:
		if(ctx.message.author.id not in warnings):
			warnings[ctx.message.author.id] = 1
		else:
			warnings[ctx.message.author.id] += 1
			await bot.say(ctx.message.author.display_name + " made a fool of themselves by trying to run a command that they can't! They now have " + str(warnings[ctx.message.author.id]) + " warnings!")
    

@bot.command(pass_context=True)
async def github():
    """ Getting Team 3216 Github Commits """
    await bot.reply("The MRT Code Has " + getCommits("MRT3216", "MRT3216-2019-DeepSpace") + " commits")

@bot.command(pass_context=True)
async def createvote(ctx, *, name:str):
    global vote, voteOwner, voted
    p = str(ctx.message.author.display_name)
    """ Random Voting """
    if(name not in vote):
        vote[name] = 0
        voteOwner[p] = name
        await bot.reply("Created voting for " + name + ". Use votefor (name) to vote for " + name + ".")
    else:
        await bot.reply(name + " already exists!")

@bot.command(pass_context=True)
async def hours(ctx):
    """ get hours """
    global vote, voteOwner, voted
    p = str(ctx.message.author.display_name)
    await bot.reply("I am sending them to you")
    await bot.whisper("You have: " + getHours(p) + " hours.")

@bot.command(pass_context=True)
async def warning(ctx):
	""" get your warnings """
	global warnings
	p = str(ctx.message.author.id)
	if p in warnings:
		pWarnings = warnings[p]
		await bot.reply("I am sending them to you")
		await bot.whisper("You have: " + str(pWarnings) + " warnings.")
	else:
		await bot.reply("you have no warnings!")

@bot.command(pass_context=True)
async def delwarning(ctx, *, user:discord.User):
	""" delete a warning (ADMIN ONLY) """
	global warnings, ADMINUSERSID
	p = str(user.id)
	u = int(ctx.message.author.id)
	print(u)
	if(u in ADMINUSERSID):
		if p in warnings:
			warnings[p] -= 1
			await bot.say("Removed a warning for " + user.display_name + ".")
			await bot.send_message(user, "One warning has been removed for you! You now have: " + str(warnings[p]) + " warnings.")
			if(warnings[p] < 1):
				warnings.pop(p)
		else:
			await bot.reply("They have no warnings!")
	else:
		if(ctx.message.author.id not in warnings):
			warnings[ctx.message.author.id] = 1
		else:
			warnings[ctx.message.author.id] += 1
		await bot.say(ctx.message.author.display_name + " made a fool of themselves by trying to run a command that they can't! They now have " + str(warnings[ctx.message.author.id]) + " warnings!")

@bot.command(pass_context=True)
async def getuid(ctx, *, user:discord.User):
	""" get a user's id """
	await bot.reply("The id of " + str(user.display_name) + " is " + str(user.id))


@bot.command(pass_context=True)
async def addwarning(ctx, user:discord.User, reason:str):
	""" add a warning "Name" + "reason" (ADMIN ONLY) """
	global warnings, ADMINUSERSID
	p = str(user.id)
	u = int(ctx.message.author.id)
	if(u in ADMINUSERSID):
		if(u in warnings):
			warnings[p] += 1
			await bot.send_message(bot.get_channel("544377549367672842"), user.mention + "       recieved a warning. Reason: " + reason + ". Message: " + str(ctx.message.content))
			await bot.say(user.mention + " has recieved a warning from " + ctx.message.author.display_name)
			await bot.send_message(user, "One warning has been given to you! You now have: " + str(warnings[p]) + " warnings.")
		else:
			warnings[p] = 1
			await bot.send_message(bot.get_channel("544377549367672842"), user.mention + " recieved a warning. Reason: " + reason + ". Message: " + str(ctx.message.content))
			await bot.say(str(user.display_name) + " has recieved a warning from " + str(ctx.message.author.display_name))
			await bot.send_message(user, "One warning has been given to you! You now have: " + str(warnings[p]) + " warnings.")
	else:
		if(u not in warnings):
			warnings[u] = 1
		else:
			warnings[u] += 1
		await bot.say(ctx.message.author.display_name + " made a fool of themselves by trying to run a command that they can't! They now have " + str(warnings[ctx.message.author.id]) + " warnings!")


@bot.command(pass_context=True)
async def money(ctx):
    """ get money """
    p = str(ctx.message.author.display_name)
    await bot.reply("I am sending them to you")
    lettM = getMoney(p).replace("," , "")
    lettM = lettM.replace("$" , "")
    lettM = lettM.strip()
    lettM = int(lettM)
    compM = lettM
    lettM = 400 - lettM
    compM = 300 - compM
    if lettM < 0:
        await bot.whisper("You have " + getMoney(p) + ". You are done with everything money related. Good job!")
    elif compM < 0:    
        await bot.whisper("You have " + getMoney(p) + ". You are done with the travel requirements. You are also " + str(lettM) + " away from lettering.")
    else:
        await bot.whisper("You have " + getMoney(p) + ". You have " + "$" + str(compM) + " left to raise in order to travel." + " You are also " + "$" + str(lettM) + " away from lettering.")            	


@bot.command(pass_context=True)
async def votefor(ctx, *, name:str):
    global vote, voted, voteOwner
    p = str(ctx.message.author.display_name)
    """ vote for (thing) """
    if(name in vote):
        if(p in voted):
            if(voted[p] == name):
                await bot.reply("You have already voted for " + name + ".")
        else:
            voted[p] = name
            vote[name] = str((int(vote[name]) + 1))
            await bot.reply("Added a vote to " + name + "." + " It has " + vote[name] + " votes")
    else:
        await bot.reply(name + " doesn't exist.")

@bot.command(pass_context=True)
async def gov(ctx):
    """ get all requirements """
    global categories
    p = str(ctx.message.author.display_name)
    await bot.reply("I am sending them to you")
    list1 = getAll(p)
    i2 = 0
    for i in list1:
        await bot.whisper(categories[i2] + i)
        i2 += 1



@bot.command(pass_context=True)
async def delvote(ctx, *, name:str):
    p = str(ctx.message.author.display_name)
    global vote, voteOwner, voted
    """ Random Voting """
    if(name in vote):
        if(p in voteOwner):
            if (voteOwner[p] == name):
                vote.pop(name)
                voteOwner.pop(p)
                await bot.reply(name + " is deleted.")
            else:
                await bot.reply("You don't have the power to do that!")
        else:
            await bot.reply("You don't have the power to do that!")
    else:
        await bot.reply(name + " vote doesn't exist.")

@bot.command(pass_context=True)
async def donations(ctx):
    """ gets from gofundme """
    global getDonations
    await bot.reply("We have: " + getDonations() + " from GoFundMe.")

@bot.command(pass_context=True)
async def terminate(ctx):
	""" stops the bot (ADMIN ONLY) """
	global ADMINUSERSID, client
	u = int(ctx.message.author.id)
	if(u in ADMINUSERSID):
		client.close()
	else:
		



@bot.command()
async def invite():
    """Bot Invite"""
    await bot.say("\U0001f44d")
    await bot.whisper("Add me with this link {}".format(discord.utils.oauth_url(bot.user.id)))
@bot.command(pass_context=True)
async def ping():
    """Pong!"""
    await bot.reply("Pong!")

bot.run('NTQzMjY2NzgyNjAxOTM2ODk4.Dz-Bog.7krYeVzdyBP79qdWVs6wJScTJI4')

