import json

import discord

import config
from config import token, prefix, ownerid, welcomeChannelId, suggestieChannelId
from discord.ext.commands import Bot, has_permissions
import asyncio

import sys, traceback

from PIL import Image, ImageDraw, ImageFilter, ImageDraw, ImageFont
import requests
from io import BytesIO

client = Bot(prefix)

# initial_extensions = ['commands.ip']
#
# # if __name__ == '__main__':
# for extension in initial_extensions:
#     client.load_extension(extension)

async def closeTicket(channel):
    for a in channel.members:
        await channel.set_permissions(a, read_messages=False,
                                      send_messages=False,
                                      add_reactions=False)


async def deleteTicket(channel):
    await channel.delete()
    with open("data.json") as f:
        data = json.load(f)

    index = data["ticket-channel-ids"].index(channel.id)
    del data["ticket-channel-ids"][index]
    del data["ticket-channel-names"][index]

    with open('data.json', 'w') as f:
        json.dump(data, f)


def welcomeFunction(member):
    im1 = Image.open('background.png')
    im3 = Image.open('profile.png')

    mask_im = Image.new("L", im3.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, 500, 500), fill=255, outline=(255))

    back_im = im1.copy()
    back_im.paste(im3, (750, 50), mask_im)

    draw = ImageDraw.Draw(back_im)
    txt = "Welkom " + member + " op Nijkerk Roleplay!"
    fontsize = 2  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.9

    font = ImageFont.truetype("OpenSans-Bold.ttf", fontsize)
    while font.getsize(txt)[0] < img_fraction * back_im.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("OpenSans-Bold.ttf", fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype("OpenSans-Bold.ttf", fontsize)

    draw.text((100, 700), txt, fill=(255, 255, 255), font=font)

    font = ImageFont.truetype("OpenSans-Bold.ttf", fontsize)

    back_im.save('output.png')


@client.event
async def on_ready():
    print("----------------------")
    print("Logged In As")
    print("Username: %s" % client.user.name)
    print("ID: %s" % client.user.id)
    print("----------------------")
    await client.change_presence(activity=discord.Activity(name='at play.nijkerkroleplay.nl', type=0))


@client.event
async def on_raw_reaction_add(payload):
    with open('data.json') as f:
        data = json.load(f)

    channel = client.get_channel(payload.channel_id)

    if payload.member.id == client.user.id:
        return

    if payload.emoji.name == "🔒":
        await closeTicket(channel)

        await channel.send("Ticket gesloten door " + payload.member.name)
        msg = await channel.send("Klik op het rode kruis om dit ticket te verwijderen.")
        await msg.add_reaction("❌")

    elif (payload.emoji.name == "❌"):
        channel = client.get_channel(payload.channel_id)
        await deleteTicket(channel)
    elif (payload.emoji.name == "📩"):
        await channel.send("!createTicket " + str(payload.member.id))
        msg = await channel.fetch_message(payload.message_id)

        for r in msg.reactions:
            if r.emoji == "📩":
                await r.remove(payload.member)



@client.command(pass_context=True)
async def suggestie(ctx):
    if ctx.message.author == client.user:
        return

    if ctx.message.content.__contains__('!suggestie') or ctx.message.channel.id == suggestieChannelId:
        if ctx.message.channel.id != suggestieChannelId:
            await ctx.message.delete()
        elif ctx.message.content.__contains__('!suggestie '):
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name='Mijn suggestie is: ', value=ctx.message.content.replace('!suggestie', ''))
            embed.set_footer(text="Suggestie van: " + str(ctx.message.author))

            msg = await ctx.message.channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name='Mijn suggestie: ', value=ctx.message.content.replace('!suggestie', ''))
            embed.set_footer(text="Suggestie van: " + str(ctx.message.author))

            msg = await ctx.message.channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name='Suggestie: ', value=ctx.message.content.replace('!suggestie', ''))
            embed.set_footer(text="Suggestie van: " + str(ctx.message.author))

            msg = await ctx.message.channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name=str(ctx.message.author),
                             icon_url='https://cdn.discordapp.com/attachments/328523940806787073/726498980497719377/nijkerk_oude_logo.png')
            embed.add_field(name='Mijn suggestie: ', value=ctx.message.content.replace('!suggestie', ''))

            msg = await ctx.message.channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            await ctx.message.delete()
        else:
            await ctx.message.delete()


@client.command(pass_context=True)
async def ip(ctx):
    if ctx.message.author == client.user:
        return

    await ctx.message.channel.send("""
Je kan met onze stad verbinden op de volgende manieren:
➤ In de serverlijst **Nijkerk** opzoeken
➤ F8 ➤ connect **play.nijkerkroleplay.nl**
    """)
    await ctx.message.delete()


# @client.command()
# async def test(ctx, member: discord.Member = None):
#     if ctx.message.author == client.user:
#         return
#
#     if not member:
#         member = ctx.message.author
#
#     response = requests.get(member.avatar_url)
#     img1 = Image.open(BytesIO(response.content))
#     img2 = img1.resize((500, 500), Image.ANTIALIAS)
#     img2.save('profile.png', quality=95)
#
#     welcomeFunction(str(ctx.message.author), ctx)
#
#     channel = client.get_channel(welcomeChannelId)
#     img = Image.open("output.png")
#     await channel.send(file=discord.File('output.png'))

@client.event
async def on_member_join(member: discord.Member = None):
    response = requests.get(member.avatar_url)
    img1 = Image.open(BytesIO(response.content))
    img2 = img1.resize((500, 500), Image.ANTIALIAS)
    img2.save('profile.png', quality=95)

    welcomeFunction(str(member))

    channel = client.get_channel(welcomeChannelId)
    img = Image.open("output.png")
    await channel.send(file=discord.File('output.png'))

@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command(pass_context=True)
async def setupTicketBot(ctx):
    if ctx.message.author == client.user:
        return

    embed = discord.Embed(colour=discord.Colour.blue())
    # embed.set_author()
    embed.add_field(name='Nijkerk Roleplay Support', value="Om een ticket aan te maken, klik op :envelope_with_arrow:")

    msg = await ctx.message.channel.send(embed=embed)
    await msg.add_reaction("📩")

    embed = discord.Embed(colour=discord.Colour.blue())
    embed.add_field(name='Nijkerk Roleplay Support', value="Om een ticket aan te maken, typ !ticket <bericht>")

    msg = await ctx.message.channel.send(embed=embed)
    await ctx.message.delete()


@client.command(pass_context=True)
async def helpTicket(ctx):
    with open("data.json") as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if ctx.author.guild_permissions.administrator or valid_user:

        em = discord.Embed(title="Nijkerk Ticket Bot Help", description="", color=discord.Colour.blue())
        em.add_field(name="`!ticket <bericht>`",
                     value="Dit maakt een nieuw ticket.")
        em.add_field(name="`!sluit`",
                     value="Dit sluit je ticket waarin dit command wordt gebruikt.")
        em.add_field(name="`!verwijder`",
                     value="Verwijder ticket uit server.")
        em.add_field(name="`!voegToegangToe <rol_id>`",
                     value="Verwijder toegang tot alle tickets voor rol id. Dit command kan alleen gebruikt worden door mensen met admin rol.")
        em.add_field(name="`!verwijderToegang <rol_id>`",
                     value="Verwijder toegang tot alle tickets voor rol id. Dit command kan alleen gebruikt worden door mensen met admin rol.")
        em.add_field(name="`!voegPingRol <rol_id>`",
                     value="Voeg rol toe aan lijst dat gepinged wordt bij ticket maken. Dit command kan alleen gebruikt worden door mensen met admin rol.")
        em.add_field(name="`!verwijderPingRol <rol_id>`",
                     value="Verwijder rol van lijst dat gepinged wordt bij ticket maken. Dit command kan alleen gebruikt worden door mensen met admin rol.")
        em.add_field(name="`!voegAdminRole <role_id>`",
                     value="!Geef rol toegang tot commands zoals `.voegPingRol` en `.voegToegangToe`. Dit command kan alleen gerund worden met administrator permissies.")
        em.add_field(name="`!verwijderAdminRol <role_id>`",
                     value="Verwijder rol toegang tot commands zoals `.voegPingRol` en `.voegToegangToe`. Dit command kan alleen gerund worden met administrator permissies.")

        await ctx.send(embed=em)
    else:
        await ctx.message.delete()


@client.command(pass_context=True)
async def ticket(ctx, *, args=None):
    await client.wait_until_ready()

    if args == None:
        message_content = "Wij zullen zo snel mogelijk bij u zijn."

    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)


    canCreateTicket = True
    ticketName2 = "ticket-{}".format(ctx.author.name)
    for ticketName in data["ticket-channel-names"]:
        if ticketName == ticketName2:
            canCreateTicket = False


    if canCreateTicket == True:
        ticket_number = int(data["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ctx.author.name))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True,
                                                 embed_links=True, attach_files=True, read_message_history=True,
                                                 external_emojis=True)

        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)

        em = discord.Embed(title="Ticket van {}".format(ctx.author.name),
                           description="{}".format(message_content), color=discord.Colour.blue())

        msg = await ticket_channel.send(embed=em)
        await msg.add_reaction("🔒")

        pinged_msg_content = ""
        non_mentionable_roles = []

        if data["pinged-roles"] != []:

            for role_id in data["pinged-roles"]:
                role = ctx.guild.get_role(role_id)

                pinged_msg_content += role.mention
                pinged_msg_content += " "

                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)

            await ticket_channel.send(pinged_msg_content)

            for role in non_mentionable_roles:
                await role.edit(mentionable=False)

        data["ticket-channel-names"].append("ticket-{}".format(ctx.author.name))
        data["ticket-channel-ids"].append(ticket_channel.id)

        data["ticket-counter"] = int(ticket_number)
        with open("data.json", 'w') as f:
            json.dump(data, f)

    await ctx.message.delete()



@client.event # Ticket met command
async def on_message(message):
    if (str(message.content).startswith("!createTicket")):

        if message.author != client.user:
            return

        await client.wait_until_ready()

        argArray = message.content.replace('!createTicket ','')
        member = client.get_user(int(argArray))


        message_content = "Wij zullen zo snel mogelijk bij u zijn."


        with open("data.json") as f:
            data = json.load(f)

        canCreateTicket = True
        ticketName2 = "ticket-{}".format(member.name)
        for ticketName in data["ticket-channel-names"]:
            if ticketName2 == ticketName:
                canCreateTicket = False


        if canCreateTicket == True:
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1

            ticket_channel = await message.guild.create_text_channel("ticket-{}".format(member.name))
            await ticket_channel.set_permissions(message.guild.get_role(message.guild.id), send_messages=False, read_messages=False)

            for role_id in data["valid-roles"]:
                role = message.guild.get_role(role_id)

                await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)

            await ticket_channel.set_permissions(member, send_messages=True, read_messages=True, add_reactions=True,
                                                 embed_links=True, attach_files=True, read_message_history=True,
                                                 external_emojis=True)

            em = discord.Embed(title="Ticket van {}".format(member.name),
                               description="{}".format(message_content), color=discord.Colour.blue())

            msg = await ticket_channel.send(embed=em)
            await msg.add_reaction("🔒")

            pinged_msg_content = ""
            non_mentionable_roles = []

            if data["pinged-roles"] != []:

                for role_id in data["pinged-roles"]:
                    role = message.guild.get_role(role_id)

                    pinged_msg_content += role.mention
                    pinged_msg_content += " "

                    if role.mentionable:
                        pass
                    else:
                        await role.edit(mentionable=True)
                        non_mentionable_roles.append(role)

                await ticket_channel.send(pinged_msg_content)

                for role in non_mentionable_roles:
                    await role.edit(mentionable=False)

            data["ticket-channel-names"].append("ticket-{}".format(member.name))
            data["ticket-channel-ids"].append(ticket_channel.id)

            # data["ticket-counter"] = int(ticket_number)
            with open("data.json", 'w') as f:
                json.dump(data, f)

        await message.delete()
    await client.process_commands(message)

@client.command()
async def sluit(ctx):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:
        channel = ctx.channel
        await channel.send("Ticket gesloten door " + ctx.author.name)
        msg = await channel.send("Klik op het rode kruis om dit ticket te verwijderen.")
        await msg.add_reaction("❌")

        await ctx.message.delete()

        for a in channel.members:
            await channel.set_permissions(a, read_messages=False,
                                          send_messages=False)


@client.command()
async def verwijder(ctx):
    with open('data.json') as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if ctx.author.guild_permissions.administrator or valid_user:
        if ctx.channel.id in data["ticket-channel-ids"]:
            channel_ids = ctx.channel.id

            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_ids)
            del data["ticket-channel-ids"][index]
            del data["ticket-channel-names"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
    else:
        await ctx.message.delete()


@client.command()
async def voegToegangToe(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:
        role_id = int(role_id)

        if role_id not in data["valid-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["valid-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)
            except:
                pass
    else:
        await ctx.message.delete()


@client.command()
async def verwijderToegang(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            valid_roles = data["valid-roles"]

            if role_id in valid_roles:
                index = valid_roles.index(role_id)

                del valid_roles[index]

                data["valid-roles"] = valid_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)
        except:
            pass
    else:
        await ctx.message.delete()


@client.command()
async def voegPingRol(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:

        role_id = int(role_id)

        if role_id not in data["pinged-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["pinged-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)
            except:
                pass
    else:
        await ctx.message.delete()


@client.command()
async def verwijderPingRol(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            pinged_roles = data["pinged-roles"]

            if role_id in pinged_roles:
                index = pinged_roles.index(role_id)

                del pinged_roles[index]

                data["pinged-roles"] = pinged_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)
        except:
            pass
    else:
        await ctx.message.delete()


@client.command()
@has_permissions(administrator=True)
async def voegAdminRole(ctx, role_id=None):
    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        data["verified-roles"].append(role_id)

        with open('data.json', 'w') as f:
            json.dump(data, f)
    except:
        pass


@client.command()
@has_permissions(administrator=True)
async def verwijderAdminRol(ctx, role_id=None):
    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        admin_roles = data["verified-roles"]

        if role_id in admin_roles:
            index = admin_roles.index(role_id)

            del admin_roles[index]

            data["verified-roles"] = admin_roles

            with open('data.json', 'w') as f:
                json.dump(data, f)
    except:
        pass


@client.command()
async def claim(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)

    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if ctx.author.guild_permissions.administrator or valid_user:
        if ctx.channel.id in data["ticket-channel-ids"]:
            await ctx.channel.edit(name=ctx.channel.name + "-" + ctx.author.name,
                                   topic="Dit ticket is geclaimd door: " + ctx.author.name)
            await ctx.message.delete()
            await ctx.send("Dit ticket is nu geclaimd door " + ctx.author.name)
    else:
        await ctx.message.delete()





@client.event
async def on_Command_error(ctx, error):
    pass


client.run(token)
