from discord.ext import commands
from discord.commands import Option
import discord



class Command(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("[ COG ] Command is set")
    

    
    @commands.slash_command(name="avatar")
    async def user_avatar(self, inter:discord.Interaction, user:Option(discord.Member, default=None)):
        user:discord.Member = user or inter.user        
        user_effective_avatar, user_literal_avatar = user.display_avatar, user.avatar

        e = discord.Embed(
            description="**%s's Avatar**" % user.mention
        )

        if user_effective_avatar != user_literal_avatar:
            e.set_image(url=user_effective_avatar)
            e.set_thumbnail(url=user_literal_avatar)
        else:
            e.set_image(url=user_effective_avatar)
        
        await inter.response.send_message(embeds=[e])
        



def setup(bot:commands.Bot):
    return bot.add_cog(Command(bot))