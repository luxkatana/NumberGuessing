import discord
import dotenv
import asqlite

from discord.ext import commands
import os
dotenv.load_dotenv()
import random
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="./", intents=intents)

SERVERS = []

@bot.event
async def on_ready():
    bot.number = False
    bot.outgoing_channel = 0
    bot.num_range = 5
    bot.playing = False
    print(f"logged in as {bot.user}")

@bot.slash_command(name="game", guild_ids=SERVERS) # in case you want the command global remove the 'guild_ids' keyword from the decorator
# NOTE THAT MAKING A COMMAND GLOBAL WILL TAKE ENOUGH TIME TO REGISTER MIGHT TAKE 1 HOUR

async def game(ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel, required=True)):
    get = bot.num_range
    if get == 5:
        is_p = bot.playing
        if is_p == True:
            e = discord.Embed(title="Failed", description="There is already a game started before", colour=discord.Color.red())
            await ctx.respond(embed=e, ephemeral=True)
            return
        randnum = random.randint(1, 5)
        if randnum == 1:
            randnum+=1
        elif randnum == 5:
            randnum-=1
        
        bot.number = randnum
        bot.num_range += 1
        bot.playing = True
        embed=discord.Embed(title="lets play a game!", description="Lets do guess the number, you got choices between 1 and 5")
        await ctx.respond("Game started in {}".format(channel.mention), ephemeral=True)

        await channel.send(embed=embed)
        bot.outgoing_channel = channel.id
        def message_check(message: discord.Message) -> bool:
            if message.content.isnumeric() and message.channel.id == channel.id and bot.playing == True:
                return True
            else:
                return False


        while True:
            message = await bot.wait_for("message", check=message_check)
            if int(message.content) == randnum:
                await message.add_reaction("🟢")
                bot.playing = False
                bot.number = 0
                bot.outgoing_channel = 0
                success = discord.Embed(title=f"{message.author} just found the answer!", description=f"big applause to **{message.author}**\n the number was {randnum}", colour=discord.Color.green())

                await message.reply(embed=success)
                break
            else:
                await message.add_reaction("🔴")
    else:
        is_p =  bot.playing
        if is_p == True:
            e = discord.Embed(title="Failed", description="There is already a game started before", colour=discord.Color.red())
            await ctx.respond(embed=e, ephemeral=True)
            return
        randnum = random.randint(1, get)
        if randnum == 1:
            randnum += 1
        elif randnum == get:
            randnum -=1
        bot.number = randnum
        bot.playing = True
        embed=discord.Embed(title="lets play a game!", description="Lets do guess the number, you got choices between 1 and {}".format(get))
        await ctx.respond("game started in {}".format(channel.mention), ephemeral=True)
        await channel.send(embed=embed)
        bot.num_range += 1
        bot.outgoing_channel = channel.id

        def message_check(message: discord.Message) -> bool:
            if message.content.isnumeric() and message.channel.id == bot.outgoing_channel and bot.playing == True:
                return True
            else:
                return False
        while True:
            message = await bot.wait_for("message", check=message_check)

            if int(message.content) == randnum:
                bot.number = 0
                bot.outgoing_channel = 0
                success = discord.Embed(title=f"{message.author} just found the answer!",
                                        description=f"big applause to **{message.author}**\n the number was {randnum}",
                                        colour=discord.Color.green())
                await message.reply(embed=success)
                bot.playing = False
                await message.add_reaction("🟢")
                break
            else:
                await message.add_reaction("🔴")
        await change_outgoing_channel(ctx.guild.id, channel.id)


bot.run(TOKEN)
 