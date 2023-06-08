import discord
import dotenv
import traceback
import asyncio
import re
import os
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
    config_handler.initialize_env()
    if not os.path.exists("filter.txt"):
        print(f"<?> 'filter.txt' not found. Creating new filter file.")
        with open("filter.txt", "w") as filter_file:
            filter_file.write("naked\nnsfw\ngore\n")


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


async def image_gen_trigger(message):
    first_word_patterns = r'(send|draw|show|display|generate|give)'
    second_word_patterns = r'(image|picture|photo|drawing|art|artwork)'
    first_word_match = re.search(first_word_patterns, message, re.IGNORECASE)

    if first_word_match:
        first_word_index = first_word_match.end()
        next_words = message[first_word_index:].split()[:5]
        next_words_str = ' '.join(next_words)
        second_word_match = re.search(second_word_patterns, next_words_str, re.IGNORECASE)

        if second_word_match:
            return True
    return False


async def filter_word_detector(input_string):
    with open('filter.txt', 'r') as filter_file:
        nsfw_phrases = [line.strip() for line in filter_file]
    input_lower = input_string.lower()
    for phrase in nsfw_phrases:
        if phrase in input_lower:
            return phrase
    return False


async def change_nickname(guild, name):
    if not guild.me.guild_permissions.change_nickname:
        print(f"<?> No permission to change nickname in {guild.name} ({guild.id})")
    else:
        await guild.me.edit(nick=name)


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
    for guild in bot.guilds:
        persona_data = await config_handler.load_persona(cached_config_json[str(guild.id)]['persona'])
        await change_nickname(guild, persona_data['name'])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for guild in cached_config_json:
        if message.channel.id != cached_config_json[guild]['chat_channel'] or not cached_config_json[guild]['chat_enabled']:
            continue
        await message.channel.trigger_typing()
        print(f"[+] #{message.channel} ({message.channel.id}) {message.author}: {message.content}")
        response = await api_hander.request_text_gen(message.channel.id, message.author.name, message.content, cached_config_json[guild]['persona'])
        await asyncio.sleep(int(cached_config_json[guild]['message_delay']))
        if cached_config_json[guild]['message_reply']:
            await message.reply(response, mention_author=cached_config_json[guild]['message_reply_mention'])
        else:
            await message.channel.send(response)
        print(f"[=] #{message.channel} ({message.channel.id}) {message.guild.me.name}: {response}")

        if not await image_gen_trigger(message.content) or not cached_config_json[guild]['image_enabled']:
            continue
        print(f"[?] Image generating...")
        await message.channel.trigger_typing()
        prompt_output = await api_hander.request_sd_prompt(message.author, message.content, cached_config_json[guild]['persona'], response)
        result = await filter_word_detector(prompt_output)
        if result and cached_config_json[guild]['filter_enabled']:
            print(f"<?> Filter detected word ({result}) in prompt.")
            await message.channel.send(f"```Image Filtered```")
        else:
            print(f"[=] #{message.channel} ({message.channel.id}) Image Gen: +({prompt_output}) -()")
            file_name = await api_hander.request_image_gen(message.channel.id, prompt_output, "")

            if file_name:
                with open(f"temp/{file_name}", 'rb') as file_path:
                    await message.channel.send(file=discord.File(file_path, 'image.jpg'))


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

        persona_data = await config_handler.load_persona(cached_config_json[str(ctx.guild.id)]['persona'])
        await change_nickname(ctx.guild, persona_data['name'])


@bot.command(description="Clears all chat history for current channel")
async def clearhistory(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You are not an administrator of the server.")
        return
    await chat_handler.clear_all_history(ctx.channel.id)
    await ctx.respond('Cleared.')


@bot.command(description="A test command")
async def testcmd(ctx, var):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You are not an administrator of the server.")
        return
    await ctx.defer()
    await ctx.respond(await filter_word_detector(var))


@bot.command(description="A test command")
async def shutdownbot(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You are not an administrator of the server.")
        return
    await chat_handler.remove_oldest_message(ctx.channel_id)
    await ctx.respond(f"Bot shutting down...")
    exit()


initialize()
try:
    bot.run(getenv("DISCORD_BOT_TOKEN"))
except Exception as bot_error:
    traceback.print_exc()
    print("<X> Bot has failed to start.")
    print(bot_error)
