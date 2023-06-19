import azure.cognitiveservices.speech as speechsdk
import dotenv
import os
from os import getenv

dotenv.load_dotenv()

azure_speech_enabled = True
if getenv('SPEECH_KEY') == "" or getenv('SERVICE_REGION') == "":
    print("<!> 'SPEECH_KEY' or 'SERVICE_REGION' is missing in .env file.")
    azure_speech_enabled = False
if not os.path.isfile("ffmpeg.exe"):
    print(
        "<!> ffmpeg.exe is not found in the root folder. Please download manually and place .exe in root folder for voice.")
    azure_speech_enabled = False


def initialize():
    if not azure_speech_enabled:
        print(f"<!> Azure Speech not available.")
        return
    directory_path = "temp/"
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(directory_path, file_name)
            os.remove(file_path)


async def is_azure_speech_enabled():
    return azure_speech_enabled


voice_counter = 0


async def azure_gen_speech(channel_id, text_message, persona_data):
    global voice_counter
    voice_counter += 1

    speech_config = speechsdk.SpeechConfig(subscription=getenv('SPEECH_KEY'), region=getenv('SERVICE_REGION'))
    ssml_text = f'''
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="{persona_data["voice"][:5]}">
    <voice name="{persona_data["voice"]}">
    <prosody pitch="{persona_data["voice_pitch"]}">
    {text_message}
    </prosody>
    </voice>
    </speak>
    '''

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(f"temp/{channel_id}-{voice_counter}.mp3")

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"[=] Speech synthesized for text: [{text_message}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"[!] Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"<!> Speech Error: {cancellation_details.error_details}")

    return f"{channel_id}-{voice_counter}"


initialize()