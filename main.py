from config import TOKEN, COGS
from discord.ext import commands
import discord

bot = commands.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("[ BOT ] %s on ready" % bot.user)


"""
@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    e = discord.Embed(description=error, color=discord.Color.red())
    await ctx.respond(embeds=[e], ephemeral=True)
"""



if __name__ == "__main__":
    for cog in COGS:
        bot.load_extension(cog)
        
    bot.run(TOKEN)