import scrapetube
import csv
from datetime import datetime

CHANNEL_ID = "your_channel_id_here"

def get_videos():
    videos = scrapetube.get_channel(CHANNEL_ID)
    return list(videos)

def update_exercises(videos):
    exercises = []
    for video in videos:
        exercise = {
            'name': video['title']['runs'][0]['text'],
            'link': f"https://www.youtube.com/watch?v={video['videoId']}",
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        exercises.append(exercise)
    return exercises

def save_exercises_to_csv(exercises):
    with open('exercises.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'link', 'date_added'])
        writer.writeheader()
        writer.writerows(exercises)

if __name__ == "__main__":
    videos = get_videos()
    exercises = update_exercises(videos)
    save_exercises_to_csv(exercises)
    print("Exercises saved to exercises.csv")