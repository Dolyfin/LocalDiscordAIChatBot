import traceback
import json
import os

configs_file_path = "configs.json"
configs_defaults = {
    "owner_id": -1,
    "chat_channel": -1,
    "chat_enabled": True,
    "message_delay": 0,
    "message_reply": False,
    "mention_reply": True,
    "persona": "example",
    "enable_image_gen": True
}

env_file_path = ".env"
env_variables_list = ["DISCORD_BOT_TOKEN", "TEXT_GEN_IP", "TEXT_GEN_PORT", "IMAGE_GEN_IP", "IMAGE_GEN_PORT"]


def initialize_env():
    if not os.path.isfile(env_file_path):
        print("<?> '.env' not found. Creating new '.env' file with necessary variables.")
        with open(env_file_path, "w") as env_file:
            for variable_string in env_variables_list:
                env_file.write(variable_string + "=\n")
        print("<!> Please save your discord bot token and API address settings in the '.env' file and start again.")
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


def initialize_config():
    if not os.path.exists(configs_file_path):
        print(f"<?> 'configs.json' not found. Creating new configs file.")
        with open(configs_file_path, "w") as configs_file:
            json.dump({}, configs_file)


async def create_config(bot):
    with open(configs_file_path, "r") as configs_file:
        existing_configs = json.load(configs_file)

    for guild in bot.guilds:
        if str(guild.id) not in existing_configs:
            print(f"<?> Created defaults in configs.json for guild: {guild} ({guild.id})")
            existing_configs[str(guild.id)] = configs_defaults

    with open(configs_file_path, "w") as configs_file:
        json.dump(existing_configs, configs_file, indent=4)


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
            return await load_configs()
    except Exception as error:
        traceback.print_exc()
        print("<!> Error while trying to set config")
        print(error)
        return False


async def load_configs():
    with open(configs_file_path, "r") as configs_file:
        return json.load(configs_file)


initialize_env()
initialize_config()
