import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv


### Load API Key ###
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


### Store Music History ###
HISTORY_FILE = "music_history.json"

### Music History Functions ###
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("music_history.json is empty. Starting fresh.")
    return {}


def save_history(music_history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(music_history, f, indent=2)


def store_in_history(music_history, mood, recommendation):
    mood = mood.lower().strip()
    if mood not in music_history:
        music_history[mood] = []
    music_history[mood].append(recommendation)
    save_history(music_history)


def show_history(music_history):
    if not music_history:
        print("No music history yet.")
        return
    
    print("Music History:")
    for mood, recommendations in music_history.items():
        print(f"    - {mood}")
        for recom in recommendations:
            print(f"    - {recom}")
        print() # blank line


def show_history_by_mood(music_history):
    if not music_history:
        print("No music history yet.")
        return
    
    print("Moods in your history:")
    for mood in music_history:
        print(f"    - {mood}")

    chosen_mood = input("Type a mood to see its song suggestions: ").strip().lower()
    if chosen_mood in music_history:
        print(f"Recommendations for '{chosen_mood}'")
        for song in music_history[chosen_mood]:
            print(f"    - {song}")
        print()
    else:
        print("That mood hasn't been added yet.")


### Call to ChatGPT for Recommendations ###
def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" / "gpt-4o" if your account has access
        temperature= 0.9,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def get_music_recommendations(mood, day_feeling):
    prompts = [
        f"What song and artist would you recommend to someone feeling {mood} and that his/her day has been {day_feeling}? Pick 1 artist",
        f"Give me a lesser-known song and lesser known-artist for the mood: {mood} and that his/her day has been {day_feeling}?. Keep it short. Pick 1 artist",
        f"A person is feeling {mood} and that his/her day has been {day_feeling}?. What's a great song and artist to listen to? Avoid mainstream artists. Pick 1 artist",
        f"Suggest one short music recommendation (song and artist) for a {mood} vibe and that his/her day has been {day_feeling}?. Pick 1 Metal song from the 2000s",
        f"If someone feels {mood} and that his/her day has been {day_feeling}?, what music would you suggest? (Keep it to 1 line). Pick 1 Alternative artist and song from the 90s"
    ]
    prompt = random.choice(prompts)
    response = call_gpt(prompt)
    return response


### User Input ###
# Ask user for his mood (1 word)
def get_user_mood(music_history):
    while True:
        mood = input("\nHow are you feeling today? (sad, happy, angry, relaxed, etc.): ").strip().lower()
        #print(len(mood))
        if len(mood) == 0:
            return None
        elif mood == "history":
            show_history_by_mood(music_history)
        elif len(mood) < 3:
            print("Enter a valid mood")
        else:
            return mood


# Ask how the user is feeling to get a better recommendation.
def get_day_feeling():
    while True:
        day_feeling = input("How was your day? (e.g., stressful, calm, chaotic, peaceful): ").strip().lower()
        if len(day_feeling) == 0:
            print("Please describe your day in a few words.")
        elif len(day_feeling) < 5:
            print("Too short! Describe your day a little more.")
        else:
            return day_feeling
        

### MAIN FUNCTION ###
def main():
    music_history = load_history()

# Introduction to the program
    print("\nWelcome to the Humör, your music recommendation program by mood")
    print("\nIf you want to exit the program just press 'ENTER'")
    print("\nYou can also enter 'history' to get a history of your moods")
    print("and then review the list of recommendations by selecting one of them")


    while True:
        mood = get_user_mood(music_history)
        if mood is None:
            print("Empty mood. Exiting the program.")
            break

        day = get_day_feeling()
        recommendation = get_music_recommendations(mood, day)

        print(f"\nHere's some music for your current mood:")
        print(recommendation)

        store_in_history(music_history, mood, recommendation)

        again = input("\nWould you like another recommendation? (y/n): ").strip().lower()
        if again != 'y':
            print("\nTake care!")
            break

    print("\nYour music recommendations have been saved. Remeber you can use 'history' to access it")


if __name__ == '__main__':
    main()