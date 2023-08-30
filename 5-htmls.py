import os
import sys
import glob
import json
import re

def load_json_from_file(filename):
    """Load and parse a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def add_line_break(description):
    description = description.replace("\n", "")
    parts = re.split(r"([\.\?\!]\s+)", description)
    if len(parts) < 3:
        return description
    else:
        firstline = ""
        i = 0
        while (i+1 < len(parts) and len(firstline) < len(description)/3):
            firstline += parts[i] + parts[i+1]
            i += 2
        return firstline + '</p><p>' + "".join(parts[i:])

def generate_html(description, subscenetag, subscenetagyes, subscenetagno, type):
    templatefile = open("template.html", 'r')
    template = templatefile.read()
    template = template.replace("{{description}}", add_line_break(description))
    template = template.replace("{{subscenetag}}", subscenetag)
    template = template.replace("{{subscenetag-yes}}", subscenetagyes)
    template = template.replace("{{subscenetag-no}}", subscenetagno)
    template = template.replace("{{display-choice}}", "block" if type == "choice" else "none")
    template = template.replace("{{display-scene}}", "block" if type == "scene" else "none")
    template = template.replace("{{display-death}}", "block" if type == "death" else "none")
    template = template.replace("{{display-hint}}", "block" if type == "hint" else "none")
    titletag = subscenetag
    titletag = titletag.replace("s", "")
    titletag = titletag.replace("-", ".")
    template = template.replace("{{title}}", titletag)
    with open(f"out\\{subscenetag}.html", 'w') as outfile:
        outfile.write(template)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]
    outprefix = dirname
    nextoutprefix = f"s{int(outprefix[1:]) + 1}"

    scenes = {}
    try:
        filename = f"{dirname}\\{outprefix}-scenes.out.json"
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

    file = open(f"{dirname}\\{outprefix}-hint.out.html", 'r')
    hint = file.read()
    generate_html(hint, f"{outprefix}-hint", f"{outprefix}-1-1", f"{outprefix}-1-1", "hint")

    files = glob.glob(f"{dirname}\\{outprefix}-*.out.txt")
    for filename in files:
        sceneprefix = (filename.split("\\")[1]).split(".")[0]
        index = int(sceneprefix.split("-")[1])
        if index == scenes["PositiveScene"]:
            continue
        file = open(filename, 'r')
        finalscene = 0
        while (file):
            line = file.readline()
            if line == "":
                if finalscene != 0:
                    if index*2 == scenes["PositiveScene"]:
                        generate_html(scenes[f"Choice {index}"], f"{sceneprefix}-{finalscene}", f"{nextoutprefix}-1-1", f"{outprefix}-{index*2+1}-1", "choice")
                    elif index*2+1 == scenes["PositiveScene"]:
                        generate_html(scenes[f"Choice {index}"], f"{sceneprefix}-{finalscene}", f"{outprefix}-{index*2}-1", f"{nextoutprefix}-1-1", "choice")
                    else:
                        generate_html(scenes[f"Choice {index}"], f"{sceneprefix}-{finalscene}", f"{outprefix}-{index*2}-1", f"{outprefix}-{index*2+1}-1", "choice")
                break
            if line.startswith("Scene 1:"):
                generate_html(file.readline(), f"{sceneprefix}-1", f"{sceneprefix}-2", f"{sceneprefix}-2", "scene")
                finalscene = 2
            if line.startswith("Scene 2:"):
                generate_html(file.readline(), f"{sceneprefix}-2", f"{sceneprefix}-3", f"{sceneprefix}-3", "scene")
                finalscene = 3
            if line.startswith("Scene 3:"):
                if (index >= 16 or (outprefix == "s0" and index >= 3)) and index != scenes["PositiveScene"]:
                    generate_html(file.readline(), f"{sceneprefix}-3", f"{outprefix}-1-1", f"{outprefix}-hint", "death")
                    finalscene = 0
                else:
                    generate_html(file.readline(), f"{sceneprefix}-3", f"{sceneprefix}-4", f"{sceneprefix}-4", "scene")
                    finalscene = 4
            if line.startswith("Scene 4:"):
                generate_html(file.readline(), f"{sceneprefix}-4", f"{sceneprefix}-5", f"{sceneprefix}-5", "scene")
                finalscene = 5
            if line.startswith("Scene 5:"):
                generate_html(file.readline(), f"{sceneprefix}-5", f"{sceneprefix}-6", f"{sceneprefix}-6", "scene")
                finalscene = 6
                
if __name__ == "__main__":
    main()