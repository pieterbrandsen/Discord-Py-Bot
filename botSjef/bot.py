import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

TOKEN = "NzI1MDYxMDc4NjY4NjczMDk0.XvWRYg.nYKPDaqDwQbTOAGnhOy5ZiYMSXM"
client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def ban(ctx, member:discord.Member, *, reason = None):
    await member.ban(reason=reason);


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!hallo':
        if str(message.author) == 'Panda!#9088':
            await message.channel.send('Je krijgt 2 euro van Sjef')
        elif str(message.author) == 'Sjef#7333':
            await message.channel.send('Hou je bek stinkhoer')
        else:
            await message.channel.send('Je krijgt 1 euro van Sjef')

    elif message.content == 'pls meme':
       await message.channel.send('Al het water stroomt als we niks doen binnen 20 jaar van de aarde af!') 


    elif message.content == '!oprotten':
        await message.channel.send('Rot zelf op of ik ga je pakken!')
##
##    elif str(message.author) == 'Sjef#7333':
##        await message.channel.send('Je bent een kut Sjef, wist je dat al?')
##    elif str(message.author) == 'Ovium#6472':
##        await message.channel.send('Ga maar naar de basisschool, pas je heel goed bij.')
##    elif str(message.author) == 'collin#0752':
##        await message.channel.send('haha grappig, je leven is grappig')
        
    elif message.content.__contains__('kut bot'):
        await message.channel.send('Je bent zelf kut!')
    elif message.content == 'raid':
        embed = discord.Embed(title="Have You Heard About RAID: Shadow Legends Yet?",
                              description="Then Here Is A Description.", color=0x00ff00)
        embed.add_field(name="---", value="""
            Today's video is sponsored by Raid Shadow Legends, 
            one of the biggest mobile role-playing games of 2019 and it's totally free! 
            Currently almost 10 million users have joined Raid over the last six months, 
            and it's one of the most impressive games in its class with detailed models, 
            environments and smooth 60 frames per second animations! 
            All the champions in the game can be customized with unique gear that changes your 
            strategic buffs and abilities! 
            The dungeon bosses have some ridiculous skills of their own and figuring out the perfect party 
            and strategy to overtake them's a lot of fun! Currently with over 300,000 reviews, 
            """, inline=False)
        embed.add_field(name="---", value="""
            Raid has almost a perfect score on the Play Store! 
            The community is growing fast and the highly anticipated new faction wars feature is now live, 
            you might even find my squad out there in the arena! It's easier to start now than ever with 
            rates program for 
            new players you get a new daily login reward for the first 90 days that you play in the game! So what are 
            you 
            waiting for? Go to the video description, click on the special links and you'll get 50,000 silver and a 
            free 
            epic champion as part of the new player program to start your journey! Good luck and I'll see you there! 
        """, inline=False)
        embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/6/60/RAID_Shadow_Legends_logo.png")
        embed.url = "https://raidshadowlegends.com/"
        await message.channel.send(embed=embed)
    elif message.content.__contains__('je bent dik'):
        await message.channel.send('haha ik ben ' +  str(message.author.name) + " lalalalalala je bent dik pffffff")






client.run(TOKEN)
