# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
audio_file = open("public/spanish.m4a", "rb")
transcript = openai.Audio.translate(
    model="whisper-1",
    file=audio_file,
    # prompt="Translate into english"
)

print(transcript.text)