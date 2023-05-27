# DiscordAIChatBot
Discord Chat bot powered by your own self hosted LLM and Image Generation.
Disclaimer: I'm not the most experienced coder.

### Requires API from oobabooga/text-generation-webui for text generation.
https://github.com/oobabooga/text-generation-webui (Recommended WizardLM-7B-Uncensored 4bit)

### Requires API from AUTOMATIC1111/stable-diffusion-webui for image generation.
https://github.com/AUTOMATIC1111/stable-diffusion-webui

# Minimal Viable Product
The bot currently works as expected for chat generation. Still very heavily WIP and will break as I make commits.

# Getting Started
1. ```git clone https://github.com/Dolyfin/LocalDiscordAIChatBot```
2. Run ```startbot.bat```
3. Add discord bot token, API address and port into ```.env``` file.
4. Run ```startbot.bat``` again.

### Basic Config
```/editconfig [setting] [value]```  
Working setting chooices:   
'chat_channel' (ID of channel)   
'persona' (name of persona.json without.json).  

```/clearhistory```
Clears chat history for current channel.  

Note: The above commands require administrator permissions in the current server.

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
# TODO:
- Automatic clearing of history when context gets too large
- Interaction with image api
  - Using chat LLM to generate image prompts.
- TTS Voice generation
- More stuff I didnt write down

#
