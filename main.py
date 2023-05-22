import discord
import dotenv
import os

bot = discord.Bot()
dotenv.load_dotenv()

def initialize():
    print("<?> Initializing bot...")
    env_variables_list = ["DISCORD_BOT_TOKEN", "IMAGE_GEN_IP", "TEXT_GEN_IP"]
    env_file_path = ".env"

    if not os.path.isfile(env_file_path):
        print("<?> '.env' not found. Creating new '.env' file with necessary variables.")
        with open(env_file_path, "w") as env_file:
            for variable_string in env_variables_list:
                env_file.write(variable_string + "=\n")
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


@bot.event
async def on_ready():
    print(f"<?> Bot connected to discord as {bot.user}!")
    bot_guilds_list = [str(guild) for guild in bot.guilds]
    print(f"<?> In {len(bot_guilds_list)} Servers: {', '.join(bot_guilds_list)}")

initialize()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

