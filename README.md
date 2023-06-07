# Welcome to BuellerBot V1 👋

🤖 Meet BuellerBot: Your AI-powered clone that joins online meetings, listens for your name, and then responds with *your* voice - all so you don’t have to. 

## Realtime Demo of BuellerBot in Action!

https://github.com/EdwardIPAguilar/BuellerBot/assets/59296703/7bc4bfa1-8104-4ffb-964f-87159ac144a5

## Table of Contents

1. [Installation](#installation)
2. [Contributing](#contributing)
3. [Questions](#questions)

## ⚙️ Installation

### Prerequisites
Python >=3.8.0
An OpenAI API key that can access OpenAI API (set up a paid account OpenAI account)
An ElevenLabs API key that can access the EL API (set up a paid account EL account)
Mac OS (Not yet tested on others!)

### Setting Up Blackhole For Source Audio Intake
One of the cool things about BuellerBot is that it can take in source audio, that way you don't need to worry about audio feedback during meetings. It can do this by using the blackhole download, which you can get here for free: https://existential.audio/blackhole/

  - Once you've downloaded blackhole (make sure it's the 2ch version), you'll need to setup a MIDI multi-output device. This is super easy on MacOS.

  - All you've got to do is open the 'Audio MIDI setup' app, click on the plus button on the bottom right-hand corner, click multi-output-device, and then be sure to select blackhole + any other devices you want your audio output to route to. Viola, audio device created!

  - Now, to make sure that audio is actually getting passed through to blackhole as well as your other output devices, be sure to right click on the newly created output device on the menu on the left-side and select 'use this device for sound output'

  - Sometimes, you might not see anything showing up when transcribing, the most likely cause is that you haven't selected 'use this device for sound output'. This resets every now and again if you're frequently connecting and disconnecting the output devices it relies on. 

P.S. Input is typically handled within the platform you're using. 

### Connecting BuellerBot To Your ElevenLabs + OpenAI Account
All you've got to do here is create your .env file, and set EL_API_KEY and OPEN_AI_KEY to = your api keys :)

## Contributing

This project is open for suggestions and contributions! In case it's your first time (as is mine), here's how you can do so:

Fork the repository: Click on the 'Fork' button at the top right corner of this page. This will create a copy of this repository in your account.

Clone the repository to your local machine: Click on the 'Code' button (usually green and located at the right of the repo's name), copy the URL, then open a terminal on your machine, navigate to the directory you want, and run

```
git clone URL
Replace URL with the url you just copied.
```

Create a branch where you can make your changes. From the terminal inside your project directory, run

```
git checkout -b branch-name
Replace branch-name with a name related to the feature you want to work on or the bug you want to fix.
```

Make your changes in this new branch.
Then, commit and push your changes. From your terminal, run

```
git add .
git commit -m "Your commit message"
git push origin branch-name
```

Replace branch-name with the name of the branch you created earlier and "Your commit message" with a description of the changes you've made.

Once you've pushed your changes to GitHub, you can create a pull request. Go to the repository page in your account, and you will see a 'Compare & pull request' button. Click on it, add further details if needed, and then click on 'Create pull request'.

If you have any suggestions, questions, or bugs to report, please open an issue in this repository! I will do my best to work on them :)

## ✍️ Questions

If you have any questions or ideas, feel free to reach out at aguilare@lakeforest.edu!

## ⚠️ Disclaimer
Buellerbot was built for *educational* purposes only. As in, you should use any free-time gained with BB to educate yourself in what matters. 

*"Life moves pretty fast. If you don't stop and look around once in a while, you could miss it."* - Ferris Bueller's Day Off, 1986

## 🏆 Acknowledgements

S/O to Michael, thank you Michael
