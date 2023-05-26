import discord
import dotenv
import traceback
from os import getenv

import chat_handler
import config_handler
import api_hander

bot = discord.Bot(intents=discord.Intents.all())
dotenv.load_dotenv()


cached_config_json = {}


def initialize():
    print("<!> Initializing bot...")
    config_handler.initialize_config()


async def change_env_var(env_var, new_value):
    env_file_path = ".env"
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


async def set_config_update(server_id, config_name, new_config_value):
    cached_config_json.update(await config_handler.set_config(server_id, config_name, new_config_value))


@bot.event
async def on_ready():
    print(f"<?> Bot connected to discord as {bot.user}!")
    bot_guilds_list = [str(guild) for guild in bot.guilds]
    print(f"<?> In {len(bot_guilds_list)} Servers: {', '.join(bot_guilds_list)}")
    try:
        await config_handler.create_config(bot)
        cached_config_json.update(await config_handler.load_configs())
    except Exception as error:
        traceback.print_exc()
        print("<!> Error while trying to check and update config.json")
        print(error)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for guild in cached_config_json:
        if message.channel.id == int(cached_config_json[guild]['chat_channel']):
            print(f"[+] #{message.channel} ({message.channel.id}) {message.author}: {message.content}")
            response = await api_hander.request_text_gen(message.channel.id, message.author.name, message.content, cached_config_json[guild]['persona'])
            await message.channel.send(response)
            print(f"[-] #{message.channel} ({message.channel.id}) {message.guild.me.name}: {response}")


@bot.command(description="Change server settings.")
async def editconfig(ctx, setting, value):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You are not an administrator of the server.")
        return
    if not await config_handler.set_config(ctx.guild.id, setting, value):
        await ctx.respond(f"Failed to set '{setting}' to '{value}'.")
        print(f"<!> [{ctx.guild.name}] Failed to set '{setting}' to '{value}'.")
    else:
        await ctx.respond(f"Successfully set '{setting}' to '{value}'.")
        print(f"<!> [{ctx.guild.name}] Successfully set '{setting}' to '{value}'.")
        global cached_config_json
        cached_config_json = await config_handler.load_configs()

        await ctx.guild.me.edit(nick=f"{ctx.guild.me.name} ({cached_config_json[str(ctx.guild.id)]['persona']})")


@bot.command(description="Clears all chat history for current channel")
async def clearhistory(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You are not an administrator of the server.")
        return
    await chat_handler.clear_all_history(ctx.channel.id)
    await ctx.respond('Cleared.')


initialize()
try:
    bot.run(getenv("DISCORD_BOT_TOKEN"))
except Exception as bot_error:
    traceback.print_exc()
    print("<X> Bot has failed to start.")
    print(bot_error)
