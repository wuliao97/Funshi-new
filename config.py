from dotenv import load_dotenv

import os
import json
from os.path import (
    join,
    dirname,
    abspath,
    splitext
)



"""PATHs"""
ROOT = abspath(dirname(__file__))

RESOURCE = join(ROOT, "resources")
FUNSHI_FOLDER = join(RESOURCE, "funshi_data")
FUNSHI = join(FUNSHI_FOLDER, "funshi.json")
COG_FOLDER = join(ROOT, "cogs")
CONFIG = join(ROOT, "config", "config.json")
ENV = join(ROOT, "config", ".env")




"""For BOT"""
load_dotenv(ENV, encoding="utf-16")

TOKEN = os.environ["token"]
SERVER = os.environ["verified_server"]
COGS = [
    "cogs.%s" % splitext(cog)[0] for cog in os.listdir(COG_FOLDER) if splitext(cog)[1] == ".py"
]


with open(CONFIG, encoding="utf-8") as f:
    CONFIG = json.load(f)

verified_roles = CONFIG["verified_roles"]
