from utils.funshiUtil import (
    base_dict, 
    base_embed, 
    getFunshiFile,
    dumpJson, 
    writeFunshi, 
    isAlready, 
    check,
    FunshiViewEdit
)

from utils.functions import getNow, codeBlock
from config import SERVER, verified_roles

from discord.ext import commands
from discord.commands import Option

import discord



class FunshiCommand(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    funshi = discord.SlashCommandGroup("funshi", "various funshi command", SERVER)
    funshi_list = funshi.create_subgroup("list", "various funshi list command", SERVER)

    @commands.Cog.listener()
    async def on_ready(self):
        print("[ COG ] Funshi Command is set")
    



    @funshi.command(name="show")
    async def funshi_list_show(self, inter:discord.Interaction, raw:Option(bool, default=False)):
        
        if raw:
            description = "json\n"
            object = dumpJson()
        
        else:
            description = ""
            object:dict = getFunshiFile()

            for idx, obj in enumerate(object.values()):
                description  += f"[ {idx + 1} ] {obj['name']} - {obj['id']}\n"
            
        if description == "json\n":
            description = "There is no Member."
        
        e = base_embed("憤死者リスト",  codeBlock(description))
        await inter.response.send_message(embeds=[e])


    @funshi_list.command(name="add")
    async def funshi_list_add(
        self,
        inter:discord.Interaction,
        user:discord.Member,
        about:Option(str, max_length=2000)
    ):
        if (check(inter) is False):
            e = discord.Embed(description="あなたには実行する権限がありません")
            await inter.response.send_message(embeds=[e], ephemeral=True)
            return 

        data = getFunshiFile()
        label = "登録完了!"
        flag = False

        if isAlready(user):
            label = "すでに登録されています"
            flag = True
        else:
            base = base_dict(user, about, getNow())
            data[user.id] = base
            writeFunshi(data)

        e = base_embed(label, None, getNow())

        await inter.response.send_message(embeds=[e], ephemeral=flag)


    @commands.user_command(name="funshi list add")
    async def funshi_list_add_with_user(
        self,
        inter:discord.Interaction,
        user:discord.Member
    ):
        if (check(inter) is False):
            e = discord.Embed(description="あなたには実行する権限がありません")
            await inter.response.send_message(embeds=[e], ephemeral=True)
            return 

        data = getFunshiFile()
        label = "登録完了!"
        flag = False

        if isAlready(user):
            label = "すでに登録されています"
            flag = True
        else:
            base = base_dict(user, "（ユーザーコマンドから追加されました）", getNow())
            data[user.id] = base
            writeFunshi(data)

        e = base_embed(label, None, getNow())

        await inter.response.send_message(embeds=[e], ephemeral=flag)


    @funshi_list.command(name="remove")
    async def funshi_list_remove(
        self, inter:discord.Interaction, user:Option(discord.Member)
    ):
        if (check(inter) is False):
            e = discord.Embed(description="あなたには実行する権限がありません")
            await inter.response.send_message(embeds=[e], ephemeral=True)
            return 

        data = getFunshiFile()
        label = "正常に除外しました"
        flag = False

        if isAlready(user) is not True:
            label="ユーザーが見つかりませんでした"
            flag = True
        else:
            data.pop(str(user.id))
            writeFunshi(data)
        
        e = base_embed(label, None, getNow())

        await inter.response.send_message(embeds=[e], ephemeral=flag)



    @funshi_list.command(name="search")
    async def funshi_list_search(self, inter:discord.Interaction, user:discord.Member):
        data:dict = getFunshiFile()[str(user.id)]

        if isAlready(user) is not True:
            e = base_embed("404 Error", "ユーザーが見つかりませんでした") 
            flag = True
        else:
            e = base_embed("憤死者名簿")
            e.add_field(name="Name", value=codeBlock(data["name"]), inline=False)
            e.add_field(name="NickName", value=codeBlock(data["nickname"]), inline=False)
            e.add_field(name="About", value=codeBlock(data["about"]))
            e.add_field(name="Date", value=codeBlock(data["date"]), inline=False)
            e.set_footer(text="ID: %s" % str(data["id"]))
            flag = False

        await inter.response.send_message(embeds=[e], ephemeral=flag)


    @funshi_list.command(name="edit")
    async def funshi_list_edit(self, inter:discord.Interaction, user:discord.Member):
        if (check(inter) is False):
            e = discord.Embed(description="あなたには実行する権限がありません")
            await inter.response.send_message(embeds=[e], ephemeral=True)
            return 

        data:dict = getFunshiFile()[str(user.id)]

        if isAlready(user) is not True:
            e = base_embed("404 Error", "ユーザーが見つかりませんでした") 
            flag = True
            view = discord.ui.View()
        else:
            e = base_embed("憤死者名簿")
            e.add_field(name="Name", value=codeBlock(data["name"]), inline=False)
            e.add_field(name="NickName", value=codeBlock(data["nickname"]), inline=False)
            e.add_field(name="About", value=codeBlock(data["about"]))
            e.add_field(name="Date", value=codeBlock(data["date"]), inline=False)
            e.set_footer(text="ID: %s" % str(data["id"]))
            flag = False
            view = FunshiViewEdit(data=data, inter=inter)


        await inter.response.send_message(
            embeds=[e], view=view, ephemeral=flag
        )



def setup(bot:commands.Bot):
    return bot.add_cog(FunshiCommand(bot))