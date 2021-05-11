import pymongo
from datetime import datetime
import requests


db_client = pymongo.MongoClient("mongodb+srv://ottawa:IT7GyTLDPsEMcCOC@test.yvxou.mongodb.net/test")
db = db_client['ottawa']
col_users = db["user"]
col_codes = db["codes"]
col_vip = db["vip"]


class DatabaseUsers:
    def __init__(self, client, _id: int):
        self.id = _id
        self.client = client

    def insert(self):
        json = {
            "_id": self.id,
            "name": str(self.client.get_user(self.id)),
            "thanks": 0,
            "xp": 0,
            "description": None
        }
        try:
            x = col_users.insert_one(json)
            return x
        except Exception as error:
            return error

    @property
    def info(self):
        x = col_users.find_one({"_id": self.id})
        return x

    def update_xp(self):
        old_xp = self.info.get("xp")
        col_users.update_one({"_id": self.id}, {"$set": {"xp": old_xp+1}})

    def update_where(self, module: str, new_value):
        col_users.update_one({"_id": self.id}, {"$set": {module: new_value}})


class DatabaseCodes:
    def __init__(self, client, code_id: str):
        self.code_id = code_id
        self.client = client

    @property
    def info(self):
        x = col_codes.find_one({"_id": self.code_id})
        return x

    def insert(self, title, description, type, author_id, copyrights, code):
        json = {
            "_id": self.code_id,
            "title": title,
            "description": description,
            "type": type,
            "author_id": author_id,
            "copyrights": copyrights,
            "code": code,
            "data": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "link": self._create_link(title, type, code)
        }
        try:
            x = col_codes.insert_one(json)
            return x
        except Exception as error:
            return error

    @staticmethod
    def _create_link(title, type, code):
        json = {
            "api_dev_key": "blY19Lnbi1K4aI-0-IMMCtK4Fdn5lfzz",
            "api_paste_code": "%s\n# Copyright (c) 2021 OTTAWA server\n# Discord: https://discord.gg/sUZ2W8FDKr\n# Note: this auto paste," % code,
            "api_paste_private": "0",
            "api_paste_name": title,
            "api_paste_format": type,
            "api_user_key": "",
            "api_option": "paste"
        }
        x = requests.post("https://pastebin.com/api/api_post.php", data=json)
        return x.content.decode("utf-8")


class DatabaseVip:
    def __init__(self, client, _id: int = None):
        self.id = _id
        self.client = client

    def insert(self, ctx, time_str, time: int, end_at):
        json = {
            "_id": self.id,
            "name": str(self.client.get_user(self.id)),
            "add_by": ctx.author.id,
            "time_str": time_str,
            "time": time,
            "end_at": end_at
        }
        try:
            x = col_vip.insert_one(json)
        except:
            old_time = self.info.get("time")
            col_vip.update_one({"_id": self.id}, {"$set": {"time": old_time + time}})

    @property
    def info(self):
        x = col_vip.find_one({"_id": self.id})
        return x

    def update_time(self):
        old_time = self.info.get("time")
        col_vip.update_one({"_id": self.id}, {"$set": {"time": old_time - 2}})

    def delete_vip(self):
        col_vip.delete_one({"_id": self.id})

    @property
    def all(self):
        return col_vip.find()


