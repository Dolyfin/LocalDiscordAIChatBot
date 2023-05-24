import json

chat_histories = {}


async def add_message(channel_id, role, content):
    chat_history = chat_histories.setdefault(channel_id, [])
    chat_history.append({"role": role, "content": content})
    chat_histories[channel_id] = chat_history


async def remove_oldest_message(channel_id):
    chat_history = chat_histories.get(channel_id, [])
    if chat_history:
        chat_history.pop(0)
        chat_histories[channel_id] = chat_history


async def get_chat_history(channel_id):
    return chat_histories.get(channel_id, [])


async def export_chat_histories():
    with open('chat_history.json', 'w') as file:
        json.dump(chat_histories, file, indent=4)
