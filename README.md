# Fateful Quest Maker

This is a simple Python framework that allows you to create pixel art "Choose Your Own Adventure" quests that are playable from the browser over the web. The quests are written and illustrated by AI using models like ChatGPT, LLaMA and Stable Diffusion.

Example quest created using this framework - https://fateful.quest

You don't need programming experience, artistic abilities or writing talent to produce results similar to this. Just be creative with the prompt and be able to operate some common AI tools (all instructions given below).

## Motivation

> **Dr. Strange:** I went forward in time... to view alternate futures. To see all the possible outcomes of the coming conflict.<br>
**Quill:** How many did you see?<br>
**Dr. Strange:** 14,000,605.<br>
**Stark:** How many did we win?<br>
**Dr. Strange:** One.

This quote from 2018 Avengers: Infinity War is one of the inspirations for this adventure. A perilous quest with branching decisions where a single improbable path leads to victory. I'm 41, so for some extra nostalgia I had to add a bit of LucasArts and Sierra and a dab of "Choose Your Own Adventure" books from my childhood.

The longest "Choose Your Own Adventure" book I've ever seen had 300 decisions in it. Can we make one closer to Avengers numbers?

This absurd idea can be explored using AI. While GPT may lack the finesse of a human writer, it can scale and will never get bored out of writing. This entire adventure is written and illustrated by AI. Instead of suppressing the hallucinations of the models, we ride them straight down the rabbit hole.

The credits go to OpenAI's ChatGPT4, Meta's LLaMA, Jon Durbin's airoboros, Stability AI's Stable Diffusion XL, Brandon Neri's Pixel Art XL LoRA and Astropulse's PixelDetector.

Needless to say, this is a fun open source passion project, there are no ads and no monetization anywhere.

## Overview of the process

1. Install some dependencies on your machine (stable-diffusion-webui, text-generation-webui)
2. Think about an idea for your quest and create a prompt that will start off the story
3. Generate with the framework the main plot synopsis using ChatGPT4 (API key costs $)
4. Generate with the framework the text content for all scenes using LLaMA (free)
5. Generate with the framework the images using Stable Diffusion (free)
6. The framework will then combine all of this into HTML pages
7. Upload the HTML pages to Github Pages so you can host them for free
8. I will happily give you a free subdomain https://your-game-name.fateful.quest so you can share your quest with the world

The idea was to see if I can create really huge quests with millions of scenes. For this to be feasible, I reduced costs as much as possible. The only paid model in the process is ChatGPT4 and we use it just for the main plot. Using ChatGPT4 API costs about $0.08 for 100 scenes. So a quest with 10,000 scenes (more than what most humans will be able to read without losing their mind) will cost you about $8 to make.

## Requirements

The primary requirement is a machine that can run Stable Diffusion and LLaMA. I personally use my local Windows machine that carries a 4090 GPU, but you can tweak the instructions easily for a cloud machine or a weaker GPU (generation will just take longer).

Not using Windows? I apologize but you will have to tweak the scripts. The paths in the scripts are Windows compatible and will probably have some issues on Linux/Mac. 

### Stable Diffusion

We need Stable Diffusion for illustrating all the scenes (create a bunch of PNG files).

1. Install stable-diffusion-webui - https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Download model SDXL v1.0 - https://civitai.com/models/101055?modelVersionId=126601 
3. Download LoRA Pixel Art XL v1.1 - https://civitai.com/models/120096?modelVersionId=135931
4. Run with `--api` enabled - https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API

Can you use a different SD client? Sure, but you may have to tweak the scripts. Can you use another model or LoRA? Sure, but you may have to tweak the scripts.

### LLaMA

We need LLaMA for writing the detailed scenes since using ChatGPT for this would be too expensive.

1. Install text-generation-webui - https://github.com/oobabooga/text-generation-webui
2. Download model airoboros 33B GPT4 m2.0 - https://huggingface.co/TheBloke/airoboros-33B-GPT4-m2.0-GPTQ
3. Run with `--api` enabled - https://github.com/oobabooga/text-generation-webui#api

Can you use another model? Sure, but you may have to tweak the scripts.

### Python

You need Python installed, I use version 3.10.11. The scripts have a couple of simple dependencies, pip install them.

### Git

You need Git installed, I use version 2.4.

## Step 1: Installation

After making sure the requirements are met, just clone this repo to download the scripts:

```
git clone https://github.com/talkol/fateful-quest-maker
```

Alternatively you can just download the ZIP with all the source files from github and extract it somewhere.

The scripts and resources after intallation are set to create my [example quest](https://fateful.quest), you will edit them in order to create your own quest with your own story.

## Step 2: General directory structure

`\` **(root of the project)**<br>This contains the Python scripts to generate the content. It also contains some static files you may want to edit like the favicon, images for home, hints and the choice screen.

`out\` **(out directory)**<br>The HTML output of your entire process will be generated here. You will publish the contents of this directory so other people can enjoy your quest. I normally make this diretory a git repo since I push it directly to Github Pages.

`s0\` **(s0 directory)**<br>Content for section 0 of the quest. This is the prologue of the quest, you will probably edit this manually to match your story.

`s1\` **(s1 directory)**<br>Content for section 1 of the quest. This is the first section generated by AI. You will just need to edit the prompt here.

`s2\` **(s2 directory)**<br>Content for section 2 of the quest. Generated fully by AI. Additional sections will be under similar directories if you add them.

You can add as many sections as you want to the quest. Every section is approximately 100 scenes with 16 possible endings, where the player only survives in one ending and continues to the next section.

We will generate using the Python scripts every section separately.

You can publish a couple of sections now and in the future add more sections and publish them as well. This is pretty flexible.

### Create the out directory

I left this directory out of the git repo on purpose. Create it yourself in the project root:

```
mkdir out
```

## Step 3: Think of a story for your quest

The protagonist is always the reader, so the quest is always mentioning "you". Is the reader an adventurer hunting for treasures? Maybe a DnD character fighting through a dungeon? Maybe a futuristic setting like Space Quest? Maybe a horror story? This is really up to you.

Once you have the setting chosen, you will need to introduce the reader to the story. This happens in the prologue in section 0 (directory `s0\`). In my [example quest](https://fateful.quest), the prologue is starts from the first scene (the golden skull) and ends with the first choice whether to take the skull or not (in the temple).

## Step 4: Edit the shared resources

The root directory contains some shared resources used in the quest. It's a good idea to update them for your story. Right now, they're updated to match my [example quest](https://fateful.quest). They include:

* `about.html` - This is the about page shown on the home screen, edit its content. I'll be grateful if you mention how you created your quest and give the link to https://github.com/talkol/fateful-quest-maker so other people can create quests too. You can open this page in your web browser to see what it looks like.

* `choice.png` - This is the PNG image shown in all the fateful choice screens. You can keep my image of the grim reaper or replace it with whatever you like. I generated mine manually with Stable Diffusion (SDXL v1.0 with Pixel Art XL v1.1 LoRA from the requirements as a 1024x1024 image that I later resized to 128x128).

* `comingsoon.html` - Let's say you decide to publish 2 sections. This page will be shown once the player finishes these 2 and reaches section 3. Once you publish section 3, this page will be shown when the player reaches section 4. You can open this page in your web browser to see what it looks like.

* `comingsoon.png` - This is the PNG image shown in `comingsoon.html`. I created it manually using the same method as `choice.png`.

* `dogicapixel.ttf`, `dogicapixelbold.ttf` - These are the pixel fonts used in the quest. If you decide to change them, either keep the same filename for simplicity or you will have to edit the font name in all HTML files.

* `favicon.ico` - The favicon for the quest that will be shown as the tab icon in the player's web browser. I created mine by uploading `favicon.png` to https://www.favicon.cc.

* `favicon.png` - The design for the favicon. I created mine by copy pasting a 16x16 area from one of the prologue images into a separate PNG file.

* `hint.png` - This is the PNG image shown in the hint screen (after the player dies and asks for a hint). I created it manually using the same method as `choice.png`.

* `home.png` - This is the PNG image shown in the background of the home screen `index.html`. I created it manually using the same method as `choice.png` but I set tiling to true in Stable Diffusion so it will seamlessly tile in the background.

* `index.html` - This is the home page of the quest. You will probably want to put your own quest's name inside and change the background. You can open this page in your web browser to see what it looks like.

* `template.html` - This is the template used for each of the scenes in your quest. Every scene has its own HTML page. You probably don't need to edit this file unless you want to change the font or button colors.

## Step 5: Prepare shared resources for publish

There's a simple batch file that copies the required files to the out directory, so they can be published later. Run:

```
0-copy-statics.bat
```

## Step 6: Edit the prologue

The prologue is found in direcoty `s0\`. It's a special section because this is the only section you will do manually. The rest of the sections will be generated by AI. I decided to do the prologue manually in order to introduce players to the story in a more stable and controlled way.

The current contents of `s0\` contain the prologue of my [example quest](https://fateful.quest). It's a good idea to play the prologue first in my example to better understand the contents of this directory. The prologue ends in the first fateful choice (where the reader chooses whether to take the skull or not). Choosing "no" in this choice is also part of the prologue. Choosing "yes" will lead to section 1 (we will create it later in directory `s1\`).

You have to edit the prologue to tell your own story, please don't use mine.

The files in the directory are pretty self explanatory. Focus on the PNG images. I created all of them with manual prompts given to Stable Diffusion with the same method as `choice.png` from the shared resources.

The texts of the prologue are found in the two TXT files in this directory. Either write them yourself, or use ChatGPT to write something and edit it. I'll leave the prompts for this small part in your hands. Probably write a shitty version yourself and tell ChatGPT to rewrite it.

The HTML file contains the hint for the first choice, shown in case the user chooses "no" and dies.

You can ignore the JSON files in this directory.

## Step 7: Prepare the prologue for publish

First copy all the PNG images to out. Run:

```
cp s0\*.png out\
```

Then generate the HTML files for the prologue. Run:

```
python 5-htmls.py s0
```

They will be generated in the out directory automatically based on `template.html` from the shared resources.

## Step 8: Create config.json

Another important file needed for the scripts is `config.json` which contains some secrets used by the scripts like your ChatGPT API key. I didn't include mine in the repo for obvious reasons. Place this file in the root directory. This is its format:

```json
{
    "OpenaiApiKey": "sk-xqFArxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxzj",
    "EncodeSecretSalt": "somepassphrase"
}
```

You will need the API key so we can use ChatGPT4 to generate the main plot synopsis. You can apply for one on https://openai.com. The API key should have ChatGPT4 allowed. Place it under the key `OpenaiApiKey`.

The second key here is `EncodeSecretSalt`. We will explain it later, for now, just think of a secret password and write it here. This will prevent your players from cheating.

Keep this config file secret and don't upload it to git. I put it in the `.gitignore` so it won't be uploaded to git by mistake.

## Step 9: Generate a section

Every section is approximately 100 scenes with 16 possible endings, where the player only survives in one ending and continues to the next section. You can create as many sections as you want to make your quest as long as you want.

Sections are generated using AI, so generating many of them doesn't take a lot of human effort. I recommend that you start with 2 sections and add more later.

These instructions will generate one section. The example given here is for section 1 (`s1` which is created in the directory `s1\`). You can easily change the instructions to secton 2 by changing `s1` to `s2`.

### 9.1 Prompt

For all sections except section 1, the prompt for generating the section is generated automatically by the previous section. For section 1 only, you will need to create the prompt manually. Run:

```
mdir s1
```

This will create the directory for section 1. Inside, create the file `s1.in.json` (so its path is `s1\s1.in.json`) with this content:

```json
{
    "Background": "After a long journey by ship, you finally reach the coordinates where the uncharted island is supposed to be. Upon arrival, you find the hidden temple and inside find the legendary cursed golden skull. As you touch the skull, you realize that something feels wrong and there may be truth to the curse of legend.",
    "Scene": "While exploring the temple, you encounter a strange insect unlike anything you've ever seen - it appears to glow and hum whenever you get closer.",
    "Choice": "Will you attempt to catch the insect?",
    "PositiveScene": 20,
    "Direction": ""
}
```

The content above is the one used for section 1 in my [example quest](https://fateful.quest). Change it to match your story. `Background` is a short background for the story up until the first scene in the section. `Scene` is the first scene of the section. `Choice` is the first choice given to the player in the section. `PositiveScene` please ignore for now, just leave it on 20.

Regarding `Direction`, you can also leave this field empty for now. In later sections, if you don't like the direction of the story and want to point it somewhere, you can add some general themes here, for example "time travel" or "horror".

Play my [example quest](https://fateful.quest) to understand where this scene shows up. It shows up right after the prologue (that ends with the first choice of the game - whether to take the skull or not). This means the choice in the prompt for section 1 is the second choice in the game.

Be very careful with the prompt since this will set the tone for your entire adventure! If you're unhappy with the results of section 1, you can always tweak the prompt and generate again.

### 9.2 ChatGPT for the synopsis

When the section prompt is ready, it's time to generate the synopsis for the section with ChatGPT4. This is a hard task, so we use the best model around. Run:

```
python 1-synopsis.py s1
```

I numbered the Python script as `1-synopsis` because it's the first Python script we run when generating a section.

This script will use your API key and ask ChatGPT4 to generate the synopsis for the section (16 possible endings). This can take about a minute.

Next, we will prepare the prompts automatically for writing all the scenes in this section. Run:

```
python 2-scene-prompts.py s1
```

### 9.3 Make sure you like the synopsis

ChatGPT doesn't always do a good job. Go over the results by opening `s1\s1-scenes.out.html` in your browser. It should look something like this:

<img src="https://i.imgur.com/HVuz8JD.png" width=600>

This HTML file helps you visualize the various scenes that this section will contain. This is shown as a tree. Every choice creates two branches. Left branch is when the player chooses "yes" and right branch is when the player chooses "no".

Overall, in a section there are exactly 15 choices that lead to 16 possible endings. Only one out of these 16 is the good ending where the player survives and moves to the next section. In all other endings the player dies. The quest involves the player guessing the correct path that leads to the good ending.

You can see the good path colored in green. All the scenes are numbered, the endings are scenes 16-31. Remember the key `PositiveScene` in the prompt file `s1.in.json`? This is the scene number of the scene that leads to victory.

If you don't like the synopsis, try generating again by running `python 1-synopsis.py s1` since ChatGPT has a random element in its responses. You can also try changing your prompt `s1.in.json` first. In the prompt, you should mainly tweak the `Background` field to give a slightly different background to the story. If you want to take the generated plot in a specific direction, add some themes to the `Direction` field, like "time travel" or "horror".

Once you like the synopsis, go over the 16 possible endings and choose the most interesting one. This should be your successful ending that leads to the next section. To change the successful ending, edit the file `s1\s1.in.json` and change `PositiveScene` to the number of the scene you want (the number must be between 16-31). Then run `python 2-scene-prompts.py s1` again and take a look at `s1\s1-scenes.out.html` in your browser again. The new scene should now be in green.

Move to the next part only after you like the synopsis and have chosen the best ending to be the green one.

### 9.4 LLaMA for writing the scenes

Start text-generation-webui to run LLaMA. 

Open http://127.0.0.1:7860/ and Load model (I use `airoboros-33B-GPT4-m2.0-GPTQ`).

Write the text for the scenes by running:

```
python 3-scenes.py s1
```

Every scene from before is expanded into 3 written scenes using LLaMA by this script.

You can go over the written scenes, they will be in the TXT files under `s1\*.out.txt`. You can edit any of them manually if you wish to change anything.

### 9.5 Stable Diffusion for illustrating the scenes

Start stable-diffusion-webui to run Stable Diffusion.

Illustrate the scenes by running:

```
python 4-images.py s1
```

You can go over the scene illustrations, they will be in the PNG files under `s1\*.png`. You can edit any of them manually if you wish to change anything.

### 9.6 Prepare the section for publish

First copy all the PNG images to out. Run:

```
cp s1\*.png out\
```

Then generate the HTML files for the section. Run:

```
python 5-htmls.py s1
```

They will be generated in the out directory automatically based on `template.html` from the shared resources.

Finally, if you're not planning to generate the next section (`s2` in this example), let's place a coming soon message there for any player that reaches this section by completing the quest. Run:

```
cp comingsoon.html out\s2-1-1.html
```

Note: If you just generated `s6` instead of `s1`, then change `s2` above to `s7`.

### 9.7 Prompt next section

Only section 1 required a manual prompt. For all other sections, the previous section generates the prompt for the next one automatically. To create the prompt for the next section, run:

```
python 6-next-section.py s1
```

This script will create the directory `s2\` and inside the prompt file `s2\s2.in.json`. Now, if you want to repeat step 9 to generate section 2, step 9.1 for section 2 is already done and you can continue from 9.2.

## Step 10: Keep generating sections

To generate section 2, repeat step 9 above to by changing `s1` in all the commands to `s2`.

In the same manner, you can add as many sections as you want, to make your quest as long as you want. This is the magical point with this experiment. A human writer will have a very hard time writing a quest with 10,000 scenes, but an AI writer can do this easily without losing its mind.

## Step 11: Encoding filenames to prevent cheating (optional)

The quest you're about to publish is split into many HTML files, one for each scene. The filenames are very indicative of when this scene is, for example `s1-3-1.html` is section 1, scene 3, part 1. This allows players to "cheat" by changing the numbers in the URL address of the website and jumping between scenes directly.

There's an optional script to prevent this type of cheating which will encode all filenames as a bunch of letters and numbers that are impossible to guess. The only way to reach the later scenes would be to actually play the game. If you want to encode the filenames, run:

```
python 7-encode.py
```

After running this script, all the filenames in out directory are going to change.

The encoding process relies on a secret passphrase that only you should know. You provided this passphrase in `config.json` under the key `EncodeSecretSalt` (see step 8).

## Step 12: Publish your quest to Github Pages

Your quest is ready for publish and found in the out directory. If you want to test it locally, use your browser to open `out\index.html`.

The easiest way to publish your quest to the world for free is by using Github Pages. This is a free service by Github that lets you publish a website directly from a git repo.

Make sure you have an account on https://github.com and use the web UI to [create a new public repo](https://docs.github.com/en/get-started/quickstart/create-a-repo). You will need to choose a name, this should probably your quest's title. For this example let's say your new quest is titled "Alien Attack", so the repo name should probably be `alien-attack`.

You should then push to git the contents of the out directory (`out\*.*`). If you know how to use git, you can create a new git repo inside the out directory and set your new Github repo as the remote. Then simply git commit and git push.

If you don't know how to use git, you can do this part manually on https://github.com using the web UI. Open your repo in the website, it should have a URL like https://github.com/talkol/alien-attack - notice that your Github username should appear instead of mine (talkol). Then, from the web UI, press [Add file - upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) and upload all the files inside the out directory. If you have more than 100 files, you may have to do this in a few batches.

Once your files are properly pushed, the repo should look something like this https://github.com/talkol/fateful-quest - this is my [example quest](https://fateful.quest).

Now, you will need to enable Github Pages on this repo, which can also be done in the web UI. Go to [Settings - Pages - Branch - main - Save](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and enable publishing the content in your main branch in the root of the repo.

This will take a few moments, but eventually your quest should be published to https://talkol.github.io/alien-attack - notice that your Github username should appear instead of mine (talkol).

You can share your quest with players by giving them the above URL. They will be able to play by visiting this address using their web browser.

## Step 13: Ask me for a free custom domain

The default Github Pages domain name is a bit ugly - https://talkol.github.io/alien-attack. You can host your quest on your own domain if you'd like to purchase one.

If you don't want to spend money, I'll be happy to give you the domain https://alien-attack.fateful.quest for free.

I will give these out on a first come first serve basis, assuming you did a decent job and this is real quest and not some low effort spam.

To ask, just [open an issue](https://github.com/talkol/fateful-quest-maker/issues) on this repo, or contact me on Telegram messenger [@talkol](https://t.me/talkol). I'm not a fan of Discord, sorry. You will need to tell me the Github URL of your published quest - like https://talkol.github.io/alien-attack.

The instructions on how to connect a custom domain to Github Pages are found [here](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

Once this is set up, the new shiny home for your quest will be:

https://alien-attack.fateful.quest

## Step 14: Adding more sections after publish

You can add more sections or make changes after you publish. Just repeat the relevant steps (step 9 for example) to add content to your out directory.

If you decided to encode filenames to prevent cheating, also repeat step 11.

When you're done, test your quest locally using your browser by opening `out\index.html`. If everything is ok, just push the new changes to git (the repo in the out directory) and your published website will be updated by Github Pages in a minute.

## Need any help?

If you need help, just [open an issue](https://github.com/talkol/fateful-quest-maker/issues) on this repo.

If you want to chat with me, contact me on Telegram messenger [@talkol](https://t.me/talkol). I'm not a fan of Discord, sorry.

## License

MIT, this is a non-profit passion project