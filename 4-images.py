import os
import sys
import glob
import webuiapi
import subprocess

def call_stablediffusion_api(prompt, sceneprefix, subscene):
    succeeded = False
    while not succeeded:
        try:
            api = webuiapi.WebUIApi(sampler="Euler a", steps=20)
            options = {}
            options["sd_model_checkpoint"] = "sd_xl_base_1.0.safetensors [31e35c80fc]"
            api.set_options(options)
            for seed in [1]:
                print(f"Calling StableDiffusion API (seed {seed})")
                result = api.txt2img(prompt=f"{prompt} <lora:pixelbuildings128-v2:1>",
                                    negative_prompt="",
                                    seed=seed,
                                    width=1024,
                                    height=1024,
                                    cfg_scale=7,
                                    )
                outfilename = f"{sceneprefix}-{subscene}-pixel-{seed}.png"
                print(f"Writing response to {outfilename}")
                result.image.save(outfilename)
                subprocess.run(["python", "pixeldetector.py", "-i" , outfilename, "-o", outfilename, "-d", "128"])
                succeeded = True
        except:
            print("Failed generating image, trying again..")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <dirname>")
        sys.exit(1)

    dirname = sys.argv[1]
    filename = os.path.join(dirname, f'{dirname}.in.json')
    outprefix = filename.split(".")[0]
    canstart = True

    files = glob.glob(f"{outprefix}-*.out.txt")
    for filename in files:
        sceneprefix = filename.split(".")[0]
        #if sceneprefix == "s1\\s1-14":
        #    canstart = True
        if not canstart:
            continue
        file = open(filename, 'r')
        while (file):
            line = file.readline()
            if line == "":
                break
            if line.startswith("Scene 1:"):
                call_stablediffusion_api(file.readline(), sceneprefix, 1)
            if line.startswith("Scene 2:"):
                call_stablediffusion_api(file.readline(), sceneprefix, 2)
            if line.startswith("Scene 3:"):
                call_stablediffusion_api(file.readline(), sceneprefix, 3)

if __name__ == "__main__":
    main()