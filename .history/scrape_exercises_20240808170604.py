import scrapetube
import pandas as pd

BASE_URL = "https://www.youtube.com/@altapersonal/videos"

def get_videos(base_url):
    "Fetch video titles and URLs from the specified YouTube channel URL"
    videos = scrapetube.get_channel(base_url)
    print("Response content:", videos)  # Debugging line to print response content
    if not videos:
        raise ValueError("The response from the YouTube channel URL is empty or invalid JSON.")
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
    videos = get_videos(BASE_URL)
    exercises = update_exercises(videos)
    save_exercises_to_csv(exercises)
