import discord
from pytz import timezone as tz
from dotenv import load_dotenv
import os
import json

load_dotenv()  # take environment variables from .env file

json_config = {}
with open('config.json', 'r', encoding='utf-8') as f:
    json_config = json.load(f)


def save_config():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(json_config, f, indent=2, ensure_ascii=False)

### Core config
bot_name = os.getenv("BOT_NAME", "hitori")
prefix = os.getenv("PREFIX", "b!")
bot_version = os.getenv("BOT_VERSION", "3.6")

TOKEN = os.getenv("DISCORD_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

S3_CONFIG = {
    'endpoint_url': os.getenv("S3_ENDPOINT_URL"),
    'aws_access_key_id': os.getenv("S3_ACCESS_KEY_ID"),                 
    'aws_secret_access_key': os.getenv("S3_SECRET_ACCESS_KEY"),             
    'region_name': os.getenv("S3_REGION_NAME", "us-east-1") 
}
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")  # Bucket must be set to Public (Read Only or Public)

image_endpoint : str = os.getenv("IMAGE_ENDPOINT", "https://church-of-nijika.pages.dev/")
file_list_name : str = os.getenv("IMAGE_LIST_FILE_NAME", "file_list.txt")

language = json_config["settings"]["language"]

timezone = tz(json_config["settings"]["timezone"])

dev_ids = json_config["dev_ids"]

banned_users = json_config["banned_users"]

specific_prefix = {int(k): v for k, v in json_config["specific_prefix"].items()}


### autoreact configs
autoreact_emojis = json_config["autoreact_emojis"]

### word react configs
word_react_messages = json_config["word_react_messages"]

### welcome configs
welcome_channel_id = json_config["welcome_channel_id"]
