import os
import sys
import json
import random
import openai

def load_json_from_file(filename):
    """Load and parse a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def get_background(scenes, index):
    prevscenes = []
    i = index
    while i > 1:
        i = i // 2
        prevscenes.insert(0, scenes[f"Scene {i}"])
    return scenes["Background"] + " " + " ".join(prevscenes)

def call_chatgpt_api(toshorten, outfilename):
    config = load_json_from_file("config.json")
    if not "OpenaiApiKey" in config:
        print("config.json does not contain 'OpenaiApiKey'")
        sys.exit(1)
    openai.api_key = config["OpenaiApiKey"]
    print("Calling ChatGPT API")
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "user",
        "content": f"Shorten this to three sentences:\n\n:{toshorten}"
        }
    ],
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print(f"Writing response to {outfilename}")
    with open(outfilename, 'w') as file:
        json.dump(response, file, indent=4)

def get_direction():
    return ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]
    outprefix = dirname
    nextoutprefix = f"s{int(outprefix[1:]) + 1}"

    if not os.path.exists(nextoutprefix):
        os.makedirs(nextoutprefix)

    scenes = {}
    try:
        filename = os.path.join(dirname, f'{outprefix}-scenes.out.json')
        scenes = load_json_from_file(filename)
        if not "Scene 1" in scenes:
            print(f"{filename} content does not contain 'Scene 1'")
            sys.exit(1)
        if not "Choice 1" in scenes:
            print(f"{filename} content does not contain 'Choice 1'")
            sys.exit(1)
        if not "PositiveScene" in scenes:
            print(f"{filename} content does not contain 'PositiveScene'")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not a valid JSON file.")

    positivescene = scenes["PositiveScene"]

    bgfilename = os.path.join(outprefix, f'{outprefix}-bgsummary.out.json')
    if not os.path.isfile(bgfilename):
        toshorten = get_background(scenes, positivescene)
        call_chatgpt_api(toshorten, bgfilename)
    bgdata = load_json_from_file(bgfilename)
    bgsummary = bgdata["choices"][0]["message"]["content"]

    nextinput = {}
    nextinput["Background"] = bgsummary.replace("\n", "")
    nextinput["Scene"] = scenes[f"Scene {positivescene}"]
    nextinput["Choice"] = scenes[f"Choice {positivescene}"]
    nextinput["PositiveScene"] = random.randrange(16, 32)
    nextinput["Direction"] = get_direction()
    path = os.path.join(nextoutprefix, f'{nextoutprefix}.in.json')
    with open(path, 'w') as nextinputfile:
        json.dump(nextinput, nextinputfile, indent=4)

if __name__ == "__main__":
    main()