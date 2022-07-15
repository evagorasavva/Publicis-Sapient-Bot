from json.decoder import JSONDecodeError
from itertools import product
from dotenv import load_dotenv
import discord
import json
import os

load_dotenv()

token = os.getenv('BOT_TOKEN')
EngID = os.getenv('ENG_ID')
ProdID = os.getenv('PROD_ID')
ProdinID = os.getenv('PRODINTERN_ID')
JuniorEng = os.getenv('JUNIOR_ID')
L1Eng = os.getenv('L1_ID')
L2Eng = os.getenv('L2_ID')
L3Eng = os.getenv('L3_ID')
SeniorEng = os.getenv('SENIOR_ID')

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    guild = client.guilds[0]
    on_ready.Engrole = discord.utils.get(guild.roles, id=int(EngID))
    on_ready.Prodrole = discord.utils.get(guild.roles, id=int(ProdID))
    on_ready.Juniorrole = discord.utils.get(guild.roles, id=int(JuniorEng))
    on_ready.L1role = discord.utils.get(guild.roles, id=int(L1Eng))
    on_ready.L2role = discord.utils.get(guild.roles, id=int(L2Eng))
    on_ready.L3role = discord.utils.get(guild.roles, id=int(L3Eng))
    on_ready.Seniorrole = discord.utils.get(guild.roles, id=int(SeniorEng))
    on_ready.Prodintrole = discord.utils.get(guild.roles, id=int(ProdinID))


@client.event
async def on_member_join(member):
    if not member.bot:
        with open('users.json', 'r') as f:
            users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.author.bot:
        with open('users.json', 'r') as f:
                 users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        if(on_ready.Engrole in user.roles ):
            if (lvl_end == 1):
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. You are a Junior Engineer !')
                await user.add_roles(on_ready.Juniorrole)
            elif (lvl_end == 10):
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. You are a L1 Engineer !')
                await user.add_roles(on_ready.L1role)
                await user.remove_roles(on_ready.Juniorrole)
            elif (lvl_end == 20):
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. You are a L2 Engineer')
                await user.add_roles(on_ready.L2role)
                await user.remove_roles(on_ready.L1role)
            elif (lvl_end == 30):
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. You are a L3 Engineer')
                await user.add_roles(on_ready.L3role)
                await user.remove_roles(on_ready.L2role)
            elif (lvl_end == 40):
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. You are a Senior Engineer. Congratulations !!!!!!!')
                await user.add_roles(on_ready.Seniorrole)
                await user.remove_roles(on_ready.L3role)
            else:
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}.')

        elif (on_ready.Prodrole in user.roles):
            if (lvl_end == 1):
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. You are a Product Manager intern')
                await user.add_roles(on_ready.Prodintrole)
            else:
                await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}.')

        else:
            await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}. Go grab your job role !!!! ')
    users[f'{user.id}']['level']=lvl_end
client.run(token)
