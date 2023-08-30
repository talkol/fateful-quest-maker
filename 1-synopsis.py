import os
import openai
import json
import sys

def call_chatgpt_api(background, scene, choice, direction, outfilename):
    config = load_json_from_file("config.json")
    if not "OpenaiApiKey" in config:
        print("config.json does not contain 'OpenaiApiKey'")
        sys.exit(1)
    openai.api_key = config["OpenaiApiKey"]
    print("Calling ChatGPT API")
    if direction != "":
        background += "\n" + "Themes: " + direction
    messages = [
        {
        "role": "system",
        "content": "You are writing the synopsis for an adventure story where the main character is the reader acting as an explorer. The story is divided into scenes, each scene has a numeric index.\n\nAt the end of every scene, the reader gets a pivotal yes no choice that will take the story to two very different and equally exciting directions.\n\nFor every scene index n provide the following:\n- Description of the scene in a sentence that describes what happens to the reader.\n- The yes no choice presented to the reader at the end of this scene, presented as a yes no question.\n\nAnswering yes to choice index n takes the reader from scene index n to scene index n*2. Answering no to choice index n takes the reader from scene index n to scene index n*2+1. Each of these next scenes is logically connected to the previous one, but takes the story in a new surprising twist.\n\nContinue adding scenes until scene index 31. Every scene has its own choice, do not combine scenes."
        },
        {
        "role": "user",
        "content": f"Background: {background}\n\nScene 1: {scene}\nChoice 1: {choice}"
        },
        {
        "role": "assistant",
        "content": "Scene 2 (YES to Choice 1): "
        }
    ]
    print(messages)
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print(f"Writing response to {outfilename}")
    with open(outfilename, 'w') as file:
        json.dump(response, file, indent=4)

def load_json_from_file(filename):
    """Load and parse a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]
    filename = dirname + "\\" + dirname + ".in.json"
    outfilename = filename.split(".")[0] + ".out.json"

    try:
        data = load_json_from_file(filename)
        if not "Background" in data:
            print(f"{filename} content does not contain 'Background'")
            sys.exit(1)
        if not "Scene" in data:
            print(f"{filename} content does not contain 'Scene'")
            sys.exit(1)
        if not "Choice" in data:
            print(f"{filename} content does not contain 'Choice'")
            sys.exit(1)
        # Call API
        direction = ""
        if "Direction" in data:
            direction = data["Direction"]
        call_chatgpt_api(data["Background"], data["Scene"], data["Choice"], direction, outfilename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not a valid JSON file.")

if __name__ == "__main__":
    main()