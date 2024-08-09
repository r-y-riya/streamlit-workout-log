import json
import scrapetube
import pandas as pd

BASE_URL = "https://www.youtube.com/@altapersonal/videos"

def get_videos(base_url):
    "Fetch video titles and URLs from the specified YouTube channel URL"
    try:
        videos = scrapetube.get_channel(base_url)
        print("Response content type:", type(videos))  # Debugging line to print response type
        video_list = []
        for video in videos:
            print("Raw video data:", video)  # Debug: print raw video data
            video_list.append({
                "title": video.get("title", {}).get("runs", [{}])[0].get("text", "No title"),
                "url": f"https://www.youtube.com/watch?v={video.get('videoId', '')}"
            })
        return video_list
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def update_exercises(videos):
    "Convert video data to exercises format"
    exercises = [{"exercise": video["title"], "url": video["url"]} for video in videos]
    return exercises

def save_exercises_to_csv(exercises):
    "Save exercises to a CSV file"
    df = pd.DataFrame(exercises)
    df.to_csv("exercises.csv", index=False)

if __name__ == "__main__":
    try:
        videos = get_videos(BASE_URL)
        if videos:
            exercises = update_exercises(videos)
            save_exercises_to_csv(exercises)
            print(f"Successfully saved {len(exercises)} exercises to CSV.")
        else:
            print("No videos were fetched. Check the error messages above.")
    except Exception as e:
        print(f"An error occurred in the main block: {e}")