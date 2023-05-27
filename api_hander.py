import requests
import json
import dotenv
from os import getenv

import chat_handler

dotenv.load_dotenv()
API_ADDRESS = getenv('TEXT_GEN_IP') + ":" + getenv('TEXT_GEN_PORT')


async def load_persona(file_path):
    with open(file_path, 'r') as file:
        persona_data = json.load(file)
    return persona_data


async def auto_truncate_chat_history(channel_id, message_content, word_limit):
    while True:
        word_count = len(message_content.split())
        for chat_message in await chat_handler.get_chat_history(channel_id):
            word_count += len(chat_message['role'].split())
            word_count += len(chat_message['content'].split())

        if word_count >= word_limit:
            chat_handler.remove_oldest_message(channel_id)
            print(f"[-] ({channel_id}) Message history too long ({word_count}), removing oldest message.")
        else:
            break


async def request_text_gen(channel_id, user_name, message_content, persona):
    await auto_truncate_chat_history(channel_id, message_content, 1024)

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
        'temperature': 1.3,
        'top_p': 1,
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

    response = requests.post(f"http://{API_ADDRESS}/api/v1/generate", json=request)

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
