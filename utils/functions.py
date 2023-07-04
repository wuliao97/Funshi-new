import json
import discord
import datetime



def getNow():
    return datetime.datetime.now().strftime("%Y/%m/%d (%a) %H:%M:%S")


def quote(obj:str):
    return ">>> " + obj


def codeBlock(obj:str, lang:str=None):
    string = "```" + lang + "\n" if lang else "```"
    return string + obj + "```"


def getFile(fp):
    return json.load(open(fp, encoding="utf-16"))


