from youtubesearchpython import *
from typing import List
import yt_dlp
import re
import json

BASE_YOUTUBE_PLAYLIST_URL = "https://www.youtube.com/playlist?list="


def getNewEpisodes(playlist_id: str, last_episode_number: int) -> List:
    playlist = Playlist(f'{BASE_YOUTUBE_PLAYLIST_URL}{playlist_id}')
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    
    print("Total number of videos: ", len(playlist.videos))

    # filter out videos that have already been processed
    new_videos = [video for video in playlist.videos if int(re.search(r'\d+', video.get('title')).group().replace(" ", "")) > int(last_episode_number)]

    return new_videos
    

def get_audio(videos: List):
    new_episodes = []
    for video in videos:
        try:
            ep_number = re.search(r'\d+', video.get('title')).group().replace(" ", "")
            result = save_audio(video.get('link'), ep_number)
            if(result != 0):
                print("Error downloading audio for episode number:", ep_number)
                continue
            video_location = "audio/%s.m4a"%str(ep_number)
            video_title = video.get('title')
            video_url = video.get('link')
            video_thumbnail = video.get('thumbnails')[0].get('url')
            new_episode = {"episodeNumber": ep_number, "title": video_title, "url": video_url, 
                        "thumbnail": video_thumbnail, "audio": video_location, "transcription": "NA", 
                        "transcribed": False, "processed": False}
            new_episodes.append(new_episode)
        except Exception as e:
            print("Error downloading audio for episode number:", video.get('title'), e)
    return new_episodes

def save_audio(ep_link: str, ep_number: int):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'audio/%s.m4a'%str(ep_number),
        'noplaylist': True,
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download(ep_link)
    return result


def save_new_episodes(new_episodes: List, existing_episodes: List):
    with open('episodes.json', 'w') as f:
        f.write(json.dumps(existing_episodes + new_episodes))


def main():
    print("Starting")
    playlist_id = "PLrYeaDpClt33OD3orEdZ2GUBqG03z5a2U"
    existing_episodes = []
    try:
        with open('episodes.json', 'r') as f:
            existing_episodes = json.load(f)
            last_episode = existing_episodes[-1]
            last_episode_number = int(last_episode.get("episodeNumber"))
    except Exception as e:
        print("Exception when opening file", e)
        last_episode_number = 0
    episodes: List = getNewEpisodes(playlist_id, last_episode_number)
    episodes.reverse()
    new_episodes = get_audio(episodes)
    save_new_episodes(new_episodes, existing_episodes)

if __name__ == "__main__":
    main()