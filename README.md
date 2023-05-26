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
1. ```git clone https://github.com/Dolyfin/DiscordAIChatBot```
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

# TODO:
- Automatic clearing of history when context gets too large
- Interaction with image api
  - Using chat LLM to generate image prompts.
- TTS Voice generation
- More stuff I didnt write down
