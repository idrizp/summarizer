from dotenv import load_dotenv
import os

load_dotenv()

import replicate
import openai
import pytube
import json

# Skip this part if we have a transcript already
total_text = ""
if not os.path.exists("transcript.txt"):

    path = input("Enter the URL of the video:")
    yt = pytube.YouTube(path)


    # 16kbps is the maximum bitrate for the openai whisper model
    print("Downloading audio...")
    audio = yt.streams.filter(only_audio=True).first()

    # download it into a temporary file
    audio.download(output_path=".", filename="audio.mp3")

    print("Preparing transcript...")
    output = replicate.run(
        "carnifexer/whisperx:1e0315854645f245d04ff09f5442778e97b8588243c7fe40c644806bde297e04",
        input={"audio": open("audio.mp3", "rb")}
    )

    # Convert the output to a json dict 
    array = json.loads(output)

    for segment in array:
        total_text += segment["text"] + " "

    with open("transcript.txt", "w") as f:
        f.write(total_text)
else:
    with open("transcript.txt", "r") as f:
        total_text = f.read()

openai.api_key = os.getenv("OPENAI_API_KEY")

context = input("Enter the context of the video: ")

def summarizer(batch, size = True):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You will summarize any text provided to you in bullet points" + "in 3 sentences or less." if size else "." + "The context is: " + context},
            {"role": "user", "content": batch}
        ]
    )
    return completion.choices[0].message.content

# Actual summarization now
window_size = 500
text_windows = [total_text[i:i+window_size] for i in range(0, len(total_text), window_size)]

window_summaries = [summarizer(window_text) for window_text in text_windows]
print(window_summaries)

combined_summary = " ".join(window_summaries)

final_summary = summarizer(combined_summary, size=False)

with open("summary.txt", "w") as f:
    f.write(final_summary)