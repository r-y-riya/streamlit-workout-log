import scrapetube
import pandas as pd

CHANNEL_ID = "UCuAXFkgsw1L7xaCfnd5JJOw"

def get_videos(channel_id):
    "Fetch video titles and URLs from the specified YouTube channel"
    videos = scrapetube.get_channel(channel_id)
    video_list = [{"title": video["title"], "url": f"https://www.youtube.com/watch?v={video['videoId']}"} for video in videos]
    return video_list

def update_exercises(videos):
    "Convert video data to exercises format"
    exercises = [{"exercise": video["title"], "url": video["url"]} for video in videos]
    return exercises

def save_exercises_to_csv(exercises):
    "Save exercises to a CSV file"
    df = pd.DataFrame(exercises)
    df.to_csv("exercises.csv", index=False)

if __name__ == "__main__":
    videos = get_videos(CHANNEL_ID)
    exercises = update_exercises(videos)
    save_exercises_to_csv(exercises)
