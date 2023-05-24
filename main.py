import discord
import dotenv
import os
import traceback
import asyncio
from os import getenv

import chat_handler
import config_handler

bot = discord.Bot(intents=discord.Intents.all())
dotenv.load_dotenv()

env_file_path = ".env"
env_variables_list = ["DISCORD_BOT_TOKEN", "IMAGE_GEN_IP", "TEXT_GEN_IP"]

cached_config_json = {}


def initialize():
    print("<!> Initializing bot...")

    if not os.path.isfile(env_file_path):
        print("<?> '.env' not found. Creating new '.env' file with necessary variables.")
        with open(env_file_path, "w") as env_file:
            for variable_string in env_variables_list:
                env_file.write(variable_string + "=\n")
        print("<!> Please save your discord bot token and other settings in the '.env' file and start again.")
        exit()
    else:
        with open(env_file_path, "r") as env_file:
            env_rows = env_file.readlines()

        with open(env_file_path, "w") as env_file:
            env_file_lines = []
            for var_row in env_rows:
                var_row_name = var_row.split("=")[0].strip()
                if var_row_name in env_variables_list:
                    env_file_lines.append(var_row)
                else:
                    print(f"<?> Removing '{var_row_name}' from '.env'. It is no longer needed.")

            for variable_string in env_variables_list:
                if variable_string not in [row.split("=")[0].strip() for row in env_rows]:
                    print(f"<?> Adding variable '{variable_string}' to '.env'")
                    env_file_lines.append(variable_string + "=\n")
            env_file.writelines(env_file_lines)

    config_handler.create_config()


async def change_env_var(env_var, new_value):
    change_completed = False
    with open(env_file_path, "r") as env_file:
        env_rows = env_file.readlines()

    with open(env_file_path, "w") as env_file:
        env_file_lines = []
        for var_row in env_rows:
            var_row_name = var_row.split("=")[0].strip()
            if var_row_name == env_var:
                env_file_lines = var_row_name + "=" + new_value
                change_completed = True
            else:
                env_file_lines = var_row
        env_file.writelines(env_file_lines)


async def set_config_update(server_id, config_name, new_config_value):
    cached_config_json.update(await config_handler.set_config(server_id, config_name, new_config_value))


@bot.event
async def on_ready():
    print(f"<?> Bot connected to discord as {bot.user}!")
    bot_guilds_list = [str(guild) for guild in bot.guilds]
    print(f"<?> In {len(bot_guilds_list)} Servers: {', '.join(bot_guilds_list)}")
    try:
        await config_handler.initialize_config(bot)
        cached_config_json.update(await config_handler.load_configs())
    except Exception as error:
        traceback.print_exc()
        print("<!> Error while trying to check and update config.json")
        print(error)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"[ ] [{message.guild}] #{message.channel} ({message.channel.id})")
    print(f"[+] {message.author}: {message.content}")

    for guild in cached_config_json:
        if message.channel.id == cached_config_json[guild]['chat_channel']:
            await chat_handler.add_message(message.channel.id, message.author.name, message.content)

    await chat_handler.export_chat_histories()


initialize()
try:
    bot.run(getenv("DISCORD_BOT_TOKEN"))
except Exception as boterror:
    traceback.print_exc()
    print("<X> Bot has failed to start.")
    print(boterror)
