from datetime import datetime
import random
import discord
from discord.ext import commands, tasks
from discord.ext.commands import command, Greedy
from typing import Optional
from discord import Embed
import json
import os
import random
from random import choice


TOKEN = "NzU2ODA0MzE3NTU3Njg2Mjky.X2XK8g.9h8LPEPdO1DNDmUurbp_BBjj-yA"

client = commands.Bot(command_prefix = '|')

mainshop = [{"name": "Rhino BP", "price":100000, "description": "Blueprint for the Rhino Warframe."},
                    {"name": "Ash BP", "price":100000, "description": "Blueprint for the Ash Warframe."},
                    {"name": "Hydroid BP", "price":100000, "description": "Blueprint for the Hydroid Warframe."}]

  


statuss = ['Synthesising thots!', 'WARFRAME', 'Working', 'Finding targets...', 'Lotus(mmmmm)']
        
#Ready?
@client.event
async def on_ready():
    change_status.start()
    print('Bot is online.')

#status_change
@tasks.loop(seconds=20)
async def change_status():
        await client.change_presence(status=discord.Status.online, activity=discord.Game(choice(statuss)))



                                 
#We delete default help command
client.remove_command('help')
#Embeded help with list and details of commands
@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.green())
    embed.set_author(name='List of commands available:')
    embed.add_field(name='|8ball (question)', value='Play magic 8ball', inline=False)
    embed.add_field(name='|hello', value='Replies with "Hi!"', inline=False)
    embed.add_field(name='|ping', value='Replies with "Pong!"', inline=False)
    embed.add_field(name='|RC_Q', value='Replies with funny or offensive(if ur Rakshan) RC jumper quotes from WatchDogs 2', inline=False)
    embed.add_field(name='|vote_kick @member', value='Vote to kick a member', inline=False)
    embed.add_field(name='**Warframe card game**', value='|account\n|slots\n|beg\n|c_account(see another member account)\n|rob', inline=False)

    embed.add_field(name='**MOD COMMANDS**', value='|kick and |ban(member)/|unban + reason\n|clear + #of messages\n|mute/unmute (member)', inline=False)
    
    await ctx.send(embed=embed)

#VOTE KICK INITIATED
@client.command()
@commands.has_any_role("ADMIN","Moderators", "Staff", "Skida")
async def vote_kick(ctx, member : discord.Member, *, reason=None):
    reactions = ['✅']
    embed = discord.Embed(
        colour = discord.Colour.red())
    embed.set_author(name=member)
    embed.add_field(name='**THIS MEMBER HAS BEEN VOTED!**', value='Vote with tick if you would like to kick this member', inline=False)
        
    count = 0
        
    channel = client.get_channel(754658395683815484)
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

    
        

    




#KICK
@client.command()
@commands.has_any_role("ADMIN","Moderators", "Staff", "Skida")
#@command(name="kick")
async def kick(ctx, member : discord.Member, *, reason=None):
    channel = client.get_channel(754658395683815484)
    await member.kick(reason=reason)

    embed = Embed(title="Member kicked", colour = 0xff5050, timestamp=datetime.utcnow())

    embed.set_thumbnail(url=member.avatar_url)

    fields = [("Member", f"{member.name} a.k.a {member.display_name}", False), ("Actioned by", ctx.author.display_name, False), ("Reason", reason, False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
            
    await channel.send(embed=embed)


#BAN
@client.command()
@commands.has_any_role("ADMIN","Moderators", "Staff", "Skida")
async def ban(ctx, member : discord.Member, *, reason=None):
    channel = client.get_channel(754658395683815484)
    await member.ban(reason=reason)

    embed = Embed(title="Member banned", colour = 0xDD2222, timestamp=datetime.utcnow())

    embed.set_thumbnail(url=member.avatar_url)

    fields = [("Member", f"{member.name} a.k.a {member.display_name}", False), ("Actioned by", ctx.author.display_name, False), ("Reason", reason, False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
            
    await channel.send(embed=embed)

#mute
@client.command()
@commands.has_any_role("ADMIN","Moderators", "Staff", "Skida")
async def mute(ctx, member: discord.Member=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send("Please specify a member so I may deal with them for not synthesising")
        return
    await member.add_roles(role)
    await ctx.send("Added roles!")

#Unmute
@client.command()
@commands.has_any_role("ADMIN","Moderators", "Staff", "Skida")
async def unmute(ctx, member: discord.Member=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not member:
        await ctx.send("Please specify a member so I may deal with them for not synthesising")
        return
    await member.remove_roles(role)
    await ctx.send("Role removed!")
    

#Unban
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
    
#ErrorCheck
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Incorrect command **HUNTER**. Try |help ({error})')

#RC jumper quotes
@client.command()
async def RC_Q(ctx):
    quotes = ['Come at meee brooooo',
              'Got ur wallet',
              '**WASTE OF SPACE**',
              'Damn, u r **UGLY**',
              'ur PATHETIC',
              'Over here **asshole**',
              "I see you haven't tamed your **SHREWWWW**"]
    await ctx.send(random.choice(quotes))

#ping
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
#8ball
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt',
                 'Maybe maybe',
                 'Of course not',
                 'Highly unlikely',
                 'Impossible',
                 'Not sure',
                 'It is uncertain',
                 'I can not foresee such an event!',
                 '**NEVER**',
                 "Like that's ever gonna happen!",
                 "Better out than in I always say",
                 "How the fuck will I know?!",
                 "Ask urself!",
                 "IDK just getta **JOB**",
                 "Yeah in like 100 years",
                 "Hmmmmm I may require maintenance after all",
                 "It's best you don't ask!"
                 ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    
 #hi                
@client.command()
async def hello(ctx):
    await ctx.send('Hi!')

#clear
@commands.has_any_role("ADMIN","Moderators", "Staff", "Skida")
@client.command()
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    if amount > 0:
        await ctx.send('I have removed ' + str(amount) + ' messages')
    if amount == 0:
        await ctx.send("Dumb fuc - you can't remove 0 messages")

#welcome
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Enjoy your stay {member.name}\nPlease read the rules!\nFailure to comply WILL result in a ban!'
    )

#----------------------------------------------------------------------------------------------------------------------WARFRAME_TEXT-----------------------------------------------------------------------------------------------------------------
@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")
    
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"{price} credits | {desc}")
    await ctx.send(embed = em)

#BUY
@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")

@client.command()
async def inv(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Inventory")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)
    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"Credits")

    return [True,"Worked"]

    

@client.command()
async def account(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    cred_amt = users[str(user.id)]["Credits"]
    plat_amt = users[str(user.id)]["Platinum"]
    start_f = users[str(user.id)]["Starter_Warframe"]
    
    em = discord.Embed(title = f"{ctx.author.name}'s **DE** account",color = discord.Color.blue())
    em.add_field(name = "Credits",value = cred_amt)
    em.add_field(name = "Platinum",value = plat_amt)
    em.add_field(name = "Starter Warframe",value = f"{start_f}")

    try:
        await ctx.send(embed = em)
    except:
        await ctx.send("Select a starter warframe hunter!")



#Check other user balance
@client.command()
async def c_account(ctx,member:discord.Member):

    await open_account(member)
    users = await get_bank_data()

    cred_amt = users[str(member.id)]["Credits"]
    plat_amt = users[str(member.id)]["Platinum"]
    start_f = users[str(member.id)]["Starter_Warframe"]

    em = discord.Embed(title = f"{member}'s **DE** account",color = discord.Color.blue())
    em.add_field(name = "Credits",value = cred_amt)
    em.add_field(name = "Platinum",value = plat_amt)
    em.add_field(name = "Starter Warframe",value = f"{start_f}")
    try:
        await ctx.send(embed = em)
    except:
        await ctx.send(f"{member} hasn't selected a starter warframe - What a **nub**!")
    

@client.command()
async def Excalibur(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if users[str(user.id)]["Starter_Warframe"] != "":
        await ctx.send("You cannot change **FOOL** ha ha ha ha")

    else:   
        await ctx.send("Your starter warframe has been set to Excalibur!")

        users[str(user.id)]["Starter_Warframe"] = "Excalibur"

        with open("mainbank.json", "w") as f:
            json.dump(users,f)
    
@client.command()   
async def Mag(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if users[str(user.id)]["Starter_Warframe"] != "":
        await ctx.send("You cannot change **FOOL** ha ha ha ha")
    else:
        await ctx.send("Your starter warframe has been set to Mag!")

        users[str(user.id)]["Starter_Warframe"] = "Mag"

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

@client.command()   

async def Volt(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    if users[str(user.id)]["Starter_Warframe"] != "":
        await ctx.send("You cannot change **FOOL** ha ha ha ha")
    else:
        

        
        await ctx.send("Your starter warframe has been set to Volt!")

        users[str(user.id)]["Starter_Warframe"] = "Volt"

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

@client.command()
async def loc(ctx, number):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    resources = ['Rubedo','Ferrite','Salvage','Neurodes']
    amount_r = random.randrange(50,400)
    
    if users[str(user.id)]["Location"] < bal[3]:
        await ctx.send(f"Your have not unlocked this location {ctx.author}!")
    else:
        rewards = [random.sample(resources,1)+ amount_r]
        em = discord.Embed(title = f"Mission Successful",color = discord.Color.green())
        em.add_field(name = "Resources obtained:",value = f"{rewards}")

    


@client.command()
@commands.cooldown(1, 0.1, commands.BucketType.user)
async def beg(ctx):
    NPC = ['Lotus', 'Teshin', 'Cephalon Simaris', 'Nef Anyo', 'Eudico', 'Your mother']
    
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    
    earnings = random.randrange(1,101)

    await ctx.send(f"{choice(NPC)} gave you {earnings} credits out of pity!")



    users[str(user.id)]["Credits"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    


async def open_account(user): #-------------------------------------
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Credits"] = 0
        users[str(user.id)]["Platinum"] = 100
        users[str(user.id)]["Starter_Warframe"] = ""
        users[str(user.id)]["Location"] = 0


    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user,change = 0,mode = "Credits"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["Credits"], users[str(user.id)]["Platinum"],users[str(user.id)]["Location"] ]
    return bal

#DONATE
@client.command()
async def donate(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You are too **pore**!")
        return
    if amount<0:
        await ctx.send("You fool - you cannot donate a negative amount!")
        return

    await update_bank(ctx.author, -1*amount, "Credits")
    await update_bank(member,amount,"Credits")

    await ctx.send(f"You gave {amount} credits to {member}!")

#Starter Warframe
@client.command()
async def starter_warframe(ctx):

    em = discord.Embed(title = f"{ctx.author.name} **CHOOSE YOUR WARFRAME**",color = discord.Color.blue())
    em.add_field(name = "Excalibur",value = "|Excalibur")
    em.add_field(name = "Mag",value = "|Mag")
    em.add_field(name = "Volt",value = "|Volt")
    em.add_field(name = "**WARNING**",value = "You can only choose once - choose wisely!")

    await ctx.send(embed = em)




@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def rob(ctx,member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)

    if bal[0]<100:
        await ctx.send("Why rob such a useless specimen!")
        return
    
    earnings = random.randrange(0, bal[0])
    

    rob_chance = random.choice([0,1,2,3,4,5])
    if rob_chance == 0:
        
        await update_bank(ctx.author, earnings)
        await update_bank(member,-1*earnings,"Credits")

        await ctx.send(f"You robbed {earnings} from {member}!")
    else:
        await ctx.send(f"You have **failed** to rob {member}!")
        return




#SLOTS
@client.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def slots(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Hunter you are **pore**!")
        return
    if amount<0:
        await ctx.send("You fool - you can't gamble a negative number!")
        return

    final = []
    for i in range(3):
        a = random.choice(['🍎', '🍒', '🍌', '🍋', '🥧', '🍓'])
        
        
        
        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_bank(ctx.author, 2*amount)
        await ctx.send("You **won**!")
        if final[0] == final[1] == final[2]:
            multiplier = random.randint(2,10)
            await update_bank(ctx.author, multiplier*amount)
            await ctx.send("You **won 3 in a ROW**!")
            await ctx.send("You got " +str(multiplier) + " times your bet!!!")

    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send("You **lost**!")

        


    
client.run(TOKEN)

