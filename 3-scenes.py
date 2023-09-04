import os
import requests
import json
import sys

def load_json_from_file(filename):
    """Load and parse a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def call_llama_api(prompt, sceneprefix):
    HOST = "localhost:5000"
    URI = f"http://{HOST}/api/v1/generate"
    request = {
        'prompt': prompt,
        'max_new_tokens': 500,
        'auto_max_new_tokens': False,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',
        'seed': 1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }
    print("Calling Llama API")
    response = requests.post(URI, json=request)
    outfilename = sceneprefix + ".out.txt"
    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        result = result.replace("’", "'")
        result = result.replace("–", "-")
        result = result.replace(" (Death):", ":")
        #print(result)
        print(f"Writing response to {outfilename}")
        with open(outfilename, 'w') as file:
            file.write("Scene 1: " + result)

def call_llama_api_for_hint(prompt, outprefix):
    HOST = "localhost:5000"
    URI = f"http://{HOST}/api/v1/generate"
    request = {
        'prompt': prompt,
        'max_new_tokens': 500,
        'auto_max_new_tokens': False,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',
        'seed': 1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }
    print("Calling Llama API")
    response = requests.post(URI, json=request)
    outfilename = outprefix + "-hint.out.html"
    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        result = result.strip()
        result = result.replace("\n", "")
        result = result.replace("’", "'")
        result = result.replace("–", "-")
        result = result.replace("Suggestion 2: ", "</p><p>")
        #print(result)
        print(f"Writing response to {outfilename}")
        with open(outfilename, 'w') as file:
            file.write(result)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]
    filename = os.path.join(dirname, f'{dirname}.in.json')
    outprefix = filename.split(".")[0]

    try:
        filename = f"{outprefix}-scenes.out.json"
        scenes = load_json_from_file(filename)
        if not "Background" in scenes:
            print(f"{filename} content does not contain 'Background'")
            sys.exit(1)
        if not "Scene 1" in scenes:
            print(f"{filename} content does not contain 'Scene 1'")
            sys.exit(1)
        if not "Choice 1" in scenes:
            print(f"{filename} content does not contain 'Choice 1'")
            sys.exit(1)
        file = open(f"{outprefix}-hint.in.txt", 'r')
        prompt = file.read()
        call_llama_api_for_hint(prompt, outprefix)
        for index in range(1, (len(scenes)-1) // 2 + 1):
            #if index != 24:
            #    continue
            sceneprefix = f"{outprefix}-{index}"
            file = open(sceneprefix + ".in.txt", 'r')
            prompt = file.read()
            call_llama_api(prompt, sceneprefix)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not a valid JSON file.")

if __name__ == "__main__":
    main()