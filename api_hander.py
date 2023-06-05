import requests
import json
import dotenv
import base64
import io
import os
from PIL import Image
from os import getenv

import chat_handler

dotenv.load_dotenv()
TEXT_API_ADDRESS = getenv('TEXT_GEN_IP') + ":" + getenv('TEXT_GEN_PORT')
IMAGE_API_ADDRESS = getenv('IMAGE_GEN_IP') + ":" + getenv('IMAGE_GEN_PORT')


async def load_persona(file_path):
    with open(file_path, 'r') as file:
        persona_data = json.load(file)
    return persona_data


async def auto_truncate_chat_history(channel_id, message_content, word_limit):
    removed_counter = 0
    while True:
        word_count = len(message_content.split())
        for chat_message in await chat_handler.get_chat_history(channel_id):
            word_count += len(chat_message['role'].split())
            word_count += len(chat_message['content'].split())

        if word_count >= word_limit:
            await chat_handler.remove_oldest_message(channel_id)
            removed_counter += 1
        else:
            if removed_counter > 0:
                print(f"[-] ({channel_id}) Message history too long (max {word_limit}), removing oldest message. (x{removed_counter})")
            break


async def request_text_gen(channel_id, user_name, message_content, persona):
    await auto_truncate_chat_history(channel_id, message_content, 800)

    persona_data = await load_persona(f"persona/{persona}.json")

    prompt = persona_data["persona"] + "\n"
    prompt = prompt + persona_data["system_message"] + "\n"

    for chat_message in await chat_handler.get_chat_history(channel_id):
        prompt = prompt + chat_message['role'] + ":" + chat_message['content'] + "\n"

    prompt = prompt + persona_data['user_prefix'].replace('{user}', user_name) + message_content + "\n"
    prompt = prompt + persona_data['assistant_prefix'].replace('{name}', persona_data['name'])

    request = {
        'prompt': prompt,
        'max_new_tokens': 512,
        'do_sample': True,
        'temperature': 1.5,
        'top_p': 0.5,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': [f"\n{user_name}:"]
    }

    response = requests.post(f"http://{TEXT_API_ADDRESS}/api/v1/generate", json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        result = result.replace(f"\n{user_name}:", "")
        await chat_handler.add_message(channel_id, user_name, message_content)
        await chat_handler.add_message(channel_id, persona_data['name'], result)
        return result
    elif response.status_code == 404:
        return "Not Found 404"
    else:
        return str(response.status_code)


async def request_image_gen(channel_id, prompt, negative_prompt):
    pos_prompt = f"{prompt}"
    neg_prompt = f"{negative_prompt}"
    payload = {
        "enable_hr": False,
        "prompt": pos_prompt,
        "seed": -1,
        "sampler_name": "DPM++ 2M",
        "batch_size": 1,
        "steps": 20,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "restore_faces": False,
        "tiling": False,
        "negative_prompt": neg_prompt
    }
    response = requests.post(url=f'http://{IMAGE_API_ADDRESS}/sdapi/v1/txt2img', json=payload)
    if response.status_code == 200:
        response_json = response.json()
        for i in response_json['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            file_name = f"{channel_id}.jpg"
            file_path = f"temp/{file_name}"
            if not os.path.exists("temp"):
                os.makedirs("temp")
            image.save(file_path, "JPEG", quality=75, optimize=True, progressive=True)
            return file_name
    else:
        print(str(response.status_code))
        return False


async def request_sd_prompt(user_name, user_message, persona, bot_message):
    # TODO: Take input message and get LLM to generate sd prompt
    persona_data = await load_persona(f"persona/{persona}.json")
    bot_name = persona_data['name']
    prompt = f'''
    You are a Image description generator. Based on the following message, respond with a description of the users desired image in short key words. The description must mostly contain short and concise keywords. Add detail to the description for setting, theme and style. Do not use NSFW words. Separate descriptions with commas.

    "{user_name}: {user_message}"
    "{bot_name}: {bot_message}"
    ### Response:Image description: 
    '''

    request = {
        'prompt': prompt,
        'max_new_tokens': 512,
        'do_sample': True,
        'temperature': 1.5,
        'top_p': 0.5,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(f"http://{TEXT_API_ADDRESS}/api/v1/generate", json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        result = result.replace("\n", "")
        result = result.strip()
        return result
    elif response.status_code == 404:
        return "Not Found 404"
    else:
        return str(response.status_code)
