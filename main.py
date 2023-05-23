import discord
import dotenv
import os
import json
import traceback
from os import getenv

bot = discord.Bot(intents=discord.Intents.all())
dotenv.load_dotenv()

configs_file_path = "configs.json"
configs_defaults = {
    "owner_id": -1,
    "chat_channel": -1,
    "chat_enabled": True,
    "message_delay": 0,
    "mention_reply": True,
    ""
}
env_file_path = ".env"
env_variables_list = ["DISCORD_BOT_TOKEN", "IMAGE_GEN_IP", "TEXT_GEN_IP"]


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

        if not os.path.exists(configs_file_path):
            print(f"<?> 'configs.json' not found. Creating new configs file.")
            with open(configs_file_path, "w") as configs_file:
                json.dump({}, configs_file)


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
    return change_completed


async def get_config(server_id, config_name):
    try:
        with open(configs_file_path, "r") as configs_file:
            configs_json = json.load(configs_file)
            server_configs = configs_json.get(str(server_id), {})
            return server_configs.get(config_name)
    except Exception as error:
        traceback.print_exc()
        print("<!> Error while trying to get config")
        print(error)


async def set_config(server_id, config_name, new_config_value):
    try:
        with open(configs_file_path, "r+") as configs_file:
            configs_json = json.load(configs_file)
            server_configs = configs_json.setdefault(str(server_id), {})
            server_configs[config_name] = new_config_value
            configs_file.seek(0)
            json.dump(configs_json, configs_file, indent=4)
            configs_file.truncate()
            return True
    except Exception as error:
        traceback.print_exc()
        print("<!> Error while trying to set config")
        print(error)
        return False


@bot.event
async def on_ready():
    print(f"<?> Bot connected to discord as {bot.user}!")
    bot_guilds_list = [str(guild) for guild in bot.guilds]
    print(f"<?> In {len(bot_guilds_list)} Servers: {', '.join(bot_guilds_list)}")
    try:
        with open(configs_file_path, "r") as configs_file:
            existing_configs = json.load(configs_file)

        for guild in bot.guilds:
            if str(guild.id) not in existing_configs:
                print(f"<?> Creating defaults in configs.json for guild: {guild}({guild.id})")
                existing_configs[str(guild.id)] = configs_defaults

        with open(configs_file_path, "w") as configs_file:
            json.dump(existing_configs, configs_file, indent=4)
    except Exception as error:
        traceback.print_exc()
        print("<!> Error while trying to check and update config.json")
        print(error)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message.content)


initialize()
try:
    bot.run(getenv("DISCORD_BOT_TOKEN"))
except Exception as boterror:
    traceback.print_exc()
    print("<X> Bot has failed to start.")
    print(boterror)
