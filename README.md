# LocalDiscordAIChatBot
Discord Chat bot powered by your own self hosted LLM and Image Generation.  
Disclaimer: I'm not the most experienced coder.

### Requires API from oobabooga/text-generation-webui for text generation.
https://github.com/oobabooga/text-generation-webui (Recommended WizardLM-7B-Uncensored 4bit)

### Requires API from AUTOMATIC1111/stable-diffusion-webui for image generation.
https://github.com/AUTOMATIC1111/stable-diffusion-webui

# Features
Note: Still very in WIP and will break as I make commits.  

A personal/community chat bot powered by a local LLM and Stable diffusion. The bot can have a customized personality config and send images.  
Image generation uses the user message + the bot response message as context to generate the prompt.  

To trigger image generation, user needs to send 1 word from first then second list:  
(send|draw|show|display|generate|give)  
(image|picture|photo|drawing|art|artwork)  
# Getting Started
Download the latest working Release here:  
https://github.com/Dolyfin/LocalDiscordAIChatBot/releases

Alternativly clone the repo which may be broken:
1. ```git clone https://github.com/Dolyfin/LocalDiscordAIChatBot```
2. Run ```startbot.bat```
3. Add discord bot token, API address and port into ```.env``` file.
4. Run ```startbot.bat``` again.
5. Use ```/editconfig chat_channel [channel id here]``` to select a chat channel.

### Updating
1. cd to root folder ```*/LocalDiscordAIChatBot/```
2. ```git pull https://github.com/Dolyfin/LocalDiscordAIChatBot```

## Basic Commands
### ```/editconfig [setting] [value]```
Available options:  
"chat_channel": integer  
"persona": string  
"chat_enabled": boolean  
"message_delay": integer  
"message_reply": boolean  
"message_reply_mention": boolean  
"mention_reply": boolean  
"image_enabled": boolean  
"filter_enabled": boolean  

```/clearhistory```
Clears chat history for current channel.  

Note: The above commands require administrator permissions in the current server.  

```filter.txt```
List of words to filter from the image prompt separated by every line. You can start with: "https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/en"
### Custom personas
Copy ```persona/example.json``` template.
```json
{
  "name": "Alice",
  "system_message": "Current time: {{time}}, {{date}}.\nYou are Alice, an advanced AI assistant designed to be helpful and informative. Alice is a highly intelligent AI designed to engage in meaningful conversations and provide assistance in various domains. Alice has a sub system that automatically sends images.\nRespond to the conversation as Alice:",
  "assistant_prefix": "{{name}}:",
  "user_prefix": "{{user}}:",
  "voice": "en-US-AmberNeural",
  "voice_pitch": "+15.0%"
}

```
Create new ```persona_name.json``` in ```persona/``` folder.  
### Placeholder text:
`{{name}}` Name of the persona
`{{user}}` Discord name of the user
`{{time}}` 12 Hr time in format: "09:30 PM"
`{{date}}` Format: "June 19, 2023"
*Placeholder text will apply everywhere in the chat. Including user messages and bot replies, not just in the prompt.

# Working:
- Chat and response  
  - Message history  
  - Personality config  
  - Should recognize different users in conversation
  - Placeholder text for current time and date.
- Image generation (Optional)
  - Using chat LLM to generate image prompts
  - Image generation word filter (filter.txt)
- Text to speech (Optional)
  - Using non local MS Azure Speech as protype.
  - The local ones aren't good enough yet or fast enough. 
# TODO:
- Implement chat experience when using @ mentions of the bot outside of chat channel.
- Fallback TTS Voice generation without Azure. Using system tts api.
- Speech to text (Whisper?)
- More stuff I didnt write down  

# Examples
![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/8a8a5022-bf59-4db6-90f9-4815a04b346b)

![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/80b6df3a-62ea-45a2-8038-084c32d971c8)

![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/9599866d-fea7-4225-bedd-e9925c9a86e0)  
(Image Prompt: GreenHaus - A logotype featuring a leaf or plant design with the name "GreenHaus" written beneath in a clean, contemporary font.)

![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/69a5a8d2-1713-44a2-8934-2c3ea492d209)


