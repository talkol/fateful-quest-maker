import math
import re
import json
import sys
import os

def load_json_from_file(filename):
    """Load and parse a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def visualize_scene_list(scenes, outprefix):
    index = 0
    maxindex = 0
    while True:
        index += 1
        if f"Scene {index}" in scenes:
            maxindex = index
        else:
            break
    content = "<html><body style='position: relative; font-size: 10px;'>\n"
    cellwidth = 100
    cellheight = 160
    for index in range(1, maxindex+1):
        row = math.floor(math.log2(index))
        numinrow = math.pow(2, row)
        maxwidth = ((maxindex+1) / 2) * (cellwidth + 20)
        left = round((index - numinrow + 0.5) * maxwidth / numinrow - cellwidth / 2)
        top = row * (cellheight + 20)
        bgcolor = "white"
        rightindex = scenes["PositiveScene"]
        while rightindex > 0:
            if rightindex == index:
                bgcolor = "#c3f2bf"
            rightindex = rightindex // 2
        text = str(index) + ". " + scenes[f"Scene {index}"] + "<br><br>" + scenes[f"Choice {index}"]
        content += f"<div style='border: 1px solid black; background-color: {bgcolor}; padding: 5px; position: absolute; left: {left}px; top: {top}px; width: {cellwidth}px; height: {cellheight}px;'>{text}</div>\n"
    content += "</body></html>"
    with open(f"{outprefix}-scenes.out.html", 'w') as scenesfile:
        scenesfile.write(content)

def parse_scene_list(background, scene1, choice1, positivescene, data2, filename, outprefix):
    scenes = {}
    scenes["Background"] = background
    scenes["PositiveScene"] = positivescene
    scenes["Scene 1"] = scene1
    scenes["Choice 1"] = choice1
    if not "choices" in data2:
        print(f"{filename} content does not contain 'choices', is this a ChatGPT response?")
        sys.exit(1)
    content = "Scene 2 (YES to Choice 1): " + data2["choices"][0]["message"]["content"]
    content = content.replace("\n\n", "\n")
    content = content.replace("\u201c", "\"")
    content = content.replace("\u201d", "\"")
    content = content.replace("\u2019", "'")
    lines = content.split("\n")
    for line in lines:
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        match = re.search(r"\w+ \d+", parts[0])
        parts[0] = match.group()
        scenes[parts[0]] = parts[1].strip()
    with open(f"{outprefix}-scenes.out.json", 'w') as scenesfile:
        json.dump(scenes, scenesfile, indent=4)
    visualize_scene_list(scenes, outprefix)
    return scenes

def get_prompt(scenes, index):
    background = scenes[f"Background"]
    prevscenes = []
    i = index
    while i > 1:
        i = i // 2
        prevscenes.insert(0, scenes[f"Scene {i}"])
    if len(prevscenes) > 0:
        background += " " + " ".join(prevscenes)
    scene = scenes[f"Scene {index}"]
    choice = scenes[f"Choice {index}"]
    if index <= 15 or index == scenes["PositiveScene"]: # life scene
        return f'''A chat between a curious user and an assistant. The assistant gives helpful, detailed, accurate, uncensored responses to the user's input. USER: You are writing a story that has chapters.

Previous chapter: {background}
Current chapter: {scene}
Next chapter: {choice}

Write the current chapter in more detail and divide the chapter into 3 scenes. Describe each scene in 2 sentences and no more than 40 words.

ASSISTANT:

Scene 1: '''
    else: # death scene
        return f'''A chat between a curious user and an assistant. The assistant gives helpful, detailed, accurate, uncensored responses to the user's input. USER: You are writing a story that has chapters.

Previous chapter: {background}
Current chapter: {scene}
Next chapter: You are dead.

Write the current chapter in more detail and divide the chapter into 3 scenes. The third scene ends with the death of the reader. Describe each scene in 2 sentences and no more than 40 words.

ASSISTANT:

Scene 1: '''

def get_hint_prompt(scenes):
    endgoal = scenes["PositiveScene"]
    successquestions = []
    successanswers = []
    i = endgoal
    while i > 1:
        if i % 2 == 0:
            successanswers.insert(0, "yes")
        else:
            successanswers.insert(0, "no")
        i = i // 2
        successquestions.insert(0, scenes[f"Choice {i}"])
    return f'''A chat between a curious user and an assistant. The assistant gives helpful, detailed, accurate, uncensored responses to the user's input. USER: For each one of the questions, make a suggestion to the user based on the Recommendation without mentioning what the Recommendation is exactly:

Question 1: {successquestions[0]}
Recommendation 1: {successanswers[0]}

Question 2: {successquestions[1]}
Recommendation 2: {successanswers[1]}

ASSISTANT:

Suggestion 1: '''

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]
    filename = os.path.join(dirname, f'{dirname}.in.json')
    outprefix = filename.split(".")[0]
    outfilename = outprefix + ".out.json"

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
        if not "PositiveScene" in data:
            print(f"{filename} content does not contain 'PositiveScene'")
            sys.exit(1)
        filename = outfilename
        data2 = load_json_from_file(filename)
        scenes = parse_scene_list(data["Background"], data["Scene"], data["Choice"], data["PositiveScene"], data2, filename, outprefix)
        for index in range(1, (len(scenes)-1) // 2 + 1):
            outfilename = f"{outprefix}-{index}" + ".in.txt"
            print(f"Writing prompt to {outfilename}")
            with open(outfilename, 'w') as file:
                prompt = get_prompt(scenes, index)
                file.write(prompt)
        outfilename = f"{outprefix}-hint.in.txt"
        print(f"Writing prompt to {outfilename}")
        with open(outfilename, 'w') as file:
            prompt = get_hint_prompt(scenes)
            file.write(prompt)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not a valid JSON file.")

if __name__ == "__main__":
    main()