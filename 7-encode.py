import os
import sys
import glob
from hashlib import sha256
import re
import json

def load_json_from_file(filename):
    """Load and parse a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def encode(filename, secretsalt):
    print(f"filename is  '{filename}'")
    print(f"Encoding with secret salt '{secretsalt}'")
    ext = filename.split(".")[-1]
    data = secretsalt + ":" + filename
    hash = sha256(data.encode('utf-8')).hexdigest()
    return hash[0:4] + "_" + hash[4:40] + "." + ext

def main():
    config = load_json_from_file("config.json")
    if not "EncodeSecretSalt" in config:
        print("config.json does not contain 'EncodeSecretSalt'")
        sys.exit(1)
    secretsalt = config["EncodeSecretSalt"]

    htmls = glob.glob(os.path.join("out", "*.html"))  
    for filename in htmls:
        with open(filename, 'r') as file:
            content = file.read()
            pnglinks = set(re.findall(r"s\d+-\d+-\d+-pixel-1\.png", content))
            htmllinks = set(re.findall(r"s\d+-\d+-\d+\.html", content))
            htmllinks.update(set(re.findall(r"s\d+-hint.html", content)))
            for pnglink in pnglinks:
                content = content.replace(pnglink, encode(pnglink, secretsalt))
            for htmllink in htmllinks:
                content = content.replace(htmllink, encode(htmllink, secretsalt))
        with open(filename, 'w') as outfile:
            outfile.write(content)
    htmls = glob.glob(os.path.join("out", "s*.html"))  
    for filename in htmls:
        newfilename = os.path.join("out", encode(os.path.basename(filename), secretsalt))  
        if os.path.isfile(newfilename):
            os.remove(newfilename)
        os.renames(filename, newfilename)
    pngs = glob.glob(os.path.join("out", "s*.png"))  
    for filename in pngs:
        newfilename = os.path.join("out", encode(os.path.basename(filename), secretsalt))  
        if os.path.isfile(newfilename):
            os.remove(newfilename)
        os.renames(filename, newfilename)

if __name__ == "__main__":
    main()
