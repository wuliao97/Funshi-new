from discord.interactions import Interaction
from discord.ui.input_text import InputText
from discord.ui.item import Item
from utils.functions import getFile, codeBlock
from config import FUNSHI, verified_roles

from discord.ext import commands

import json
import discord
import datetime


class FunshiViewEdit(discord.ui.View):
    def __init__(self, data:dict, inter:Interaction, timeout: float | None = 180, disable_on_timeout: bool = False):
        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.data = data
        self.inter = inter
    
    async def interaction_check(self, interaction: Interaction):
        if (interaction.user) != self.inter.user:
            await interaction.response.send_message("あなたには実行権限がありません", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.green)
    async def test_callback(self, button, inter:Interaction):
        await inter.response.send_modal(FunshiModalEdit("憤死者名簿の編集", data=self.data))



class FunshiModalEdit(discord.ui.Modal):
    def __init__(self, title:str, data:dict, timeout:float=None):
        super().__init__(title=title, timeout=timeout)
        self.data = data
        
        self.add_item(InputText(
                style=discord.InputTextStyle.long,
                max_length=1_000,
                label="About user",
                value=data["about"]
            )
        )

    async def callback(self, interaction: Interaction):
        material = self.children[0]
        data = getFunshiFile()
        data[str(self.data["id"])]["about"] = material.value
        writeFunshi(data)
        
        e = base_embed("正常に編集されました", codeBlock(material.value))

        await interaction.response.send_message(embeds=[e])


def base_embed(title:str, about:str=None, data=None):
    
    e = discord.Embed(color=0xff0000)
    
    if title:
        e.title = title
    
    if about:
        e.description = about
    
    if data:
        e.set_footer(text=data)
    
    return e


def base_dict(user:discord.Member | str, about:str, id:int=None, nickname:str=None):
    date = datetime.datetime.now().strftime("%Y/%m/%d (%a) %H:%M:%S")
    
    if isinstance(user, discord.Member):
        return {
            "name":user.name,
            "nickname":user.display_name,
            "id":user.id,
            "about":about,
            "date":date
        }
        
    elif isinstance(user, str) and id:
        return {
            "name":user,
            "nickname":nickname,
            "id":id,
            "about":about, 
            "date":date
        }



def getFunshiFile():
    return getFile(FUNSHI)


def check(inter:discord.Interaction):
    return all(True for role in inter.user.roles if role in verified_roles)


def dumpJson():
    return json.dumps(getFile(FUNSHI), indent=4, ensure_ascii=False)



def writeFunshi(data:dict):
    with open(FUNSHI, "r+", encoding="utf-16") as f:
        f.seek(0)
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
        f.truncate()


def isAlready(user:discord.Member):
    if str(user.id) in getFunshiFile():
        return True
    return False