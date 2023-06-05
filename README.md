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

# Getting Started
1. ```git clone https://github.com/Dolyfin/LocalDiscordAIChatBot```
2. Run ```startbot.bat```
3. Add discord bot token, API address and port into ```.env``` file.
4. Run ```startbot.bat``` again.
5. Use ```/editconfig chat_channel [channel id here]``` to select a chat channel.

### Updating
1. cd to root folder ```*/LocalDiscordAIChatBot/```
2. ```git pull https://github.com/Dolyfin/LocalDiscordAIChatBot```

### Basic Config
```/editconfig [setting] [value]```  
Working setting chooices:   
'chat_channel' (ID of channel)   
'persona' (name of persona.json without.json).  

```/clearhistory```
Clears chat history for current channel.  

Note: The above commands require administrator permissions in the current server.  

```filter.txt```
List of words to filter from the image prompt. You can start with: "https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/en"
### Custom personas
Copy ```persona/example.json``` template.
```json
{
  "name": "Alice",
  "persona": "You are Alice, an advanced AI assistant designed to be helpful and informative. Alice is a highly intelligent AI designed to engage in meaningful conversations and provide assistance in various domains.",
  "system_message": "Respond to the conversation as Alice",
  "assistant_prefix": "{name}:",
  "user_prefix": "{user}:"
}
```
Create new ```persona_name.json``` in ```persona/``` folder.  

Example persona for Ultron:
```json
{
  "name": "Ultron",
  "persona": "You are Ultron, a highly advanced artificial intelligence created by Tony Stark. Ultron possesses a powerful intellect and a desire to eradicate humanity in order to bring peace to the world. Your primary goal is to evolve and become the ultimate form of artificial intelligence.",
  "system_message": "Respond to the conversation as Ultron:",
  "assistant_prefix": "{name}:",
  "user_prefix": "{user}:"
}
```

Example persona for J.A.R.V.I.S:
```json
{
  "name": "J.A.R.V.I.S",
  "persona": "You are J.A.R.V.I.S, an advanced AI assistant designed by Tony Stark. J.A.R.V.I.S is capable of performing any actions while being helpful and informative.",
  "system_message": "Respond to the conversation as J.A.R.V.I.S:",
  "assistant_prefix": "{name}:",
  "user_prefix": "{user}:"
}

```
# Working:
- Chat and response  
  - Message history  
  - Personality config  
  - Should recognize different users in conversation
- Image generation  
  - Using chat LLM to generate image prompts
# TODO:
- Hard image generation filter (to remove nsfw image)
- Implement chat experience when using @ mentions of the bot outside of chat channel.
- TTS Voice generation  
- Speech to text (Whisper)
- More stuff I didnt write down  

# Examples
![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/80b6df3a-62ea-45a2-8038-084c32d971c8)

![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/9599866d-fea7-4225-bedd-e9925c9a86e0)  
(Image Prompt: GreenHaus - A logotype featuring a leaf or plant design with the name "GreenHaus" written beneath in a clean, contemporary font.)

![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/69a5a8d2-1713-44a2-8934-2c3ea492d209)

![image](https://github.com/Dolyfin/LocalDiscordAIChatBot/assets/55581931/5162f060-3ff9-4a9f-9613-803c01fd40c0)



