from tempfile import NamedTemporaryFile
import whisper
import os
from typing import List
import json

def transcribe_audio(path: str):
    model = whisper.load_model("small")
    result = model.transcribe(path)
    return result

def format_transcription(transcription: str):
    formatted_segments: List = []
    for segment in transcription['segments']:
        formatted_segment = {'start': segment['start'], 'end': segment['end'], 'text': segment['text']}
        formatted_segments.append(formatted_segment)
    return formatted_segments

def save_transcription(transcription: List, filename: str, directory: str = "transcriptions"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/{filename}', 'w') as f:
        f.write(json.dumps(transcription))
    print("Transcription saved")

def save_updated_episodes(episodes: List, filename: str = "episodes.json"):
    with open(filename, 'w') as f:
        f.write(json.dumps(episodes))
    print("Updated episodes saved")

def main():
    print("Starting")
    directory = "transcriptions"
    with open('episodes.json', 'r') as f:
        episodes = json.load(f)
        if(len(episodes) == 0):
            print("No episodes to transcribe")
            return
        for episode in episodes:
            if episode['processed'] == True or episode['transcribed'] == True:
                print("Episode already transcribed or processed")
                continue
            audio_path = episode['audio']
            filename = episode['title'].replace(" ", "_") + ".json"
            transcription = transcribe_audio(audio_path)
            formatted_transcription = format_transcription(transcription)
            save_transcription(formatted_transcription, filename, directory)
            episode['transcription'] = f'{directory}/{filename}'
            episode['transcribed'] = True
            save_updated_episodes(episodes)

if __name__ == "__main__":
    main()