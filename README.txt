# 🎮 Gamora – The AI Game Builder  

> *“Tell me your idea, I’ll build your game.”*  

Gamora is an **AI-powered 2D game generator** that creates complete, ready-to-play games based on simple user input.  
Whether it’s a **platformer**, **shooter**, **puzzle**, or **board game**, Gamora instantly builds the full game project folder with code, assets, and a README inside.  

No coding required — just describe your game idea, answer a few quick questions, and download a **ready-to-run game**.  

---

## ✨ Features  

- 🧠 **AI-Assisted Suggestions**  
  - Suggests game names and genres based on your input.  
  - Guides you through simple design choices (player count, difficulty, etc.).  

- 🎮 **Multiple Genres Supported**  
  - **Board Games** (Tic Tac Toe, Connect 4, etc.)  
  - **Platformers**  
  - **Shooters**  
  - **Puzzle & Mini Games**  

- 🖼️ **Automatic Assets**  
  - Pre-assigned placeholder sprites for player, enemies, and backgrounds.  
  - Simplified art to keep it lightweight and fast.  

- 📂 **Complete Game Folder**  
  - A full project with `main.py`, assets, and a README.  
  - Organized and ready-to-run instantly.  

- 🖱️ **Interactive UI with Streamlit**  
  - User interacts via **mouse clicks** in the web app.  
  - Generated games run in a **separate Pygame window**.  

- 📦 **Downloadable Game Projects**  
  - Games are zipped and downloadable directly from the web app.  
  - Folder name = the game’s chosen title.  

---

## 📂 Project Structure  

Gamora-GameBuilder/
│── gamora.py # (main entry point) # Handles game generation logic
│── requirements.txt # Python dependencies
│── commands.txt # Quick setup and usage commands
│── README.md # Project documentation
│── .gitignore # Ignore cache/venv files

## 📂Each generated game folder looks like:  

MyAwesomeGame/
│── main.py # The main game loop
│── assets/ # Placeholder art & sprites
│── README.md # Instructions for this game


## ⚡ Getting Started

1️⃣ Clone the Repository

2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

3️⃣ Install Requirements
pip install -r requirements.txt

4️⃣ Run Gamora with Streamlit
streamlit run app.py