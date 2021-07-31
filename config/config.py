import json
from dotenv import load_dotenv
from os import getenv
load_dotenv()

with open("config/config.json", "r") as file:
    config = json.load(file)

token = getenv("TOKEN")
prefix = getenv("PREFIX")
guild_id = int(getenv("GUILD_ID"))
owner_ids = [int(i) for i in config['owner_id']]
submit_channel = config['submit']['channel']
submit_stats = config['submit']['open_or_close']
coder_role_name = config["coder_role"]['name']
coder_role_id = int(config["coder_role"]['id'])
mention_code_role = config['mention_code_role']
welcome_channel = config['welcome']
mongo_url = getenv("MONGO_URL")
key_pastbin = getenv("KEY_PASTBIN")


async def update(key, value):
    available = [
        "token", "prefix", "guild_id", "submit_channel", "coder_role_name", "mention_code_role", "welcome_channel"]
    if key not in available:
        raise TypeError("The '%s' not in available keys" % key)
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
        file.close()


