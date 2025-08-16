# Gamora - Game Design & Generation Tool
# This tool helps users design and generate simple games based on their ideas.

import streamlit as st
from pathlib import Path
import json
import pygame
import os
import zipfile
import random
import io
import requests
from datetime import datetime

# Utilities
def slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")[:60] or "game"

def download_file(url: str):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            return r.content
    except:
        return b''

# Templates & Sprites
TEMPLATES = {
    "platformer": {"base_enemies":5,"base_collectibles":3,"mechanics":["move","jump"]},
    "shooter": {"base_enemies":10,"base_collectibles":2,"mechanics":["move","shoot"]},
    "puzzle": {"puzzles_per_level":3,"mechanics":["switch","timer"]},
    "minigame": {"mechanics":[]}
}

SPRITES = {
    "pixel":{"player":"https://opengameart.org/sites/default/files/player.png",
             "enemy":"https://opengameart.org/sites/default/files/enemy.png",
             "collectible":"https://opengameart.org/sites/default/files/collectible.png"},
    "cartoon":{"player":"https://opengameart.org/sites/default/files/cartoon_player.png",
               "enemy":"https://opengameart.org/sites/default/files/cartoon_enemy.png",
               "collectible":"https://opengameart.org/sites/default/files/cartoon_collectible.png"},
    "minimalist":{"player":"https://opengameart.org/sites/default/files/minimal_player.png",
                  "enemy":"https://opengameart.org/sites/default/files/minimal_enemy.png",
                  "collectible":"https://opengameart.org/sites/default/files/minimal_collectible.png"}
}

# AI Design Suggestions
GENRE_KEYWORDS = {
    "platformer": ["jump","run","platform","mario","metroidvania"],
    "shooter": ["shoot","gun","bullet","shooter","top-down"],
    "puzzle": ["puzzle","logic","riddle"],
    "adventure": ["explore","story","quest"],
    "survival": ["survive","horde","waves"],
    "minigame": ["tic","connect","memory","board","game"]
}

MECHANIC_KEYWORDS = {
    "jump": ["jump","double jump","wall jump","dash"],
    "shoot": ["shoot","reload","aim","grenade"],
    "collect": ["collect","pickup","coin","gem"],
    "stealth": ["stealth","hide","sneak"],
    "craft": ["craft","build","upgrade"]
}

ENEMY_KEYWORDS = {
    "zombies":["zombie","undead"],
    "robots":["robot","drone"],
    "guards":["guard","soldier","security"],
    "dragons":["dragon","wyvern"],
}

def ai_suggest_mechanics(idea):
    idea_l = idea.lower()
    mechanics = []
    for mech, kws in MECHANIC_KEYWORDS.items():
        for kw in kws:
            if kw in idea_l:
                mechanics.append(mech)
    if not mechanics:
        mechanics=["move","jump"]
    return list(set(mechanics))

def ai_suggest_enemies(idea):
    idea_l = idea.lower()
    enemies=[]
    for enemy, kws in ENEMY_KEYWORDS.items():
        for kw in kws:
            if kw in idea_l:
                enemies.append(enemy)
    if not enemies:
        enemies=["default_enemy"]
    return list(set(enemies))

def ai_suggest_genre(idea):
    idea_l = idea.lower()
    for genre,kws in GENRE_KEYWORDS.items():
        for kw in kws:
            if kw in idea_l:
                return genre
    return "platformer"

# Procedural Level Generation
def generate_levels(data):
    levels=[]
    for i in range(data["levels"]):
        level={}
        if data["genre"]=="platformer":
            platforms=[{"x":random.randint(50,550),"y":random.randint(50,400),
                        "width":random.randint(50,150)} for j in range(5+i)]
            
            enemies=[]
            for e_type in data["enemies"]:
                count=random.randint(1,3+i)
                for _ in range(count):
                    behavior=random.choice(["patrol","follow_pattern","chase"])
                    enemies.append({"type":e_type,"x":random.randint(50,600),
                                    "y":random.randint(50,400),"behavior":behavior})
            
            collectibles=[{"x":random.randint(50,600),"y":random.randint(50,400)} 
                          for j in range(data.get("base_collectibles",3)+i)]
            
            level={"level_number":i+1,"platforms":platforms,"enemies":enemies,
                   "collectibles":collectibles,"difficulty":i+1}

        elif data["genre"]=="shooter":
            enemies=[]
            for e_type in data["enemies"]:
                count=random.randint(2,5+i)
                for _ in range(count):
                    behavior=random.choice(["patrol","chase","shoot"])
                    speed=random.randint(2,5)+i
                    enemies.append({"type":e_type,"x":random.randint(50,600),
                                    "y":random.randint(50,400),
                                    "behavior":behavior,"speed":speed})
            
            collectibles=[{"x":random.randint(50,600),"y":random.randint(50,400)} 
                          for j in range(data.get("base_collectibles",2)+i)]
            
            level={"level_number":i+1,"enemies":enemies,"collectibles":collectibles,
                   "difficulty":i+1}

        elif data["genre"]=="puzzle":
            puzzles=[{"type":random.choice(["switch","timer","lever"]),
                      "position":(random.randint(50,600),random.randint(50,400))} 
                     for j in range(TEMPLATES["puzzle"]["puzzles_per_level"])]
            level={"level_number":i+1,"puzzles":puzzles,"difficulty":i+1}

        else:  # minigame / board game
            level={"level_number":i+1,"type":data.get("game_type","Tic-Tac-Toe")}
        levels.append(level)
    return levels

# Assets & main.py
def prepare_assets(data):
    if data["genre"]=="minigame":
        return {}
    art_style=data.get("art_style","pixel")
    assets={}
    urls=SPRITES.get(art_style,SPRITES["pixel"])
    for key,url in urls.items():
        assets[key]=download_file(url)
    return assets

def generate_main_py(data):
    if data["genre"]=="minigame":
        return f"""import pygame
pygame.init()
screen=pygame.display.set_mode((400,400))
pygame.display.set_caption("{data['idea']}")
font=pygame.font.SysFont(None,40)
board=[["","",""],["","",""],["","",""]]
player="X"
def draw_board():
    screen.fill((255,255,255))
    for i in range(1,3):
        pygame.draw.line(screen,(0,0,0),(0,i*133),(400,i*133),3)
        pygame.draw.line(screen,(0,0,0),(i*133,0),(i*133,400),3)
    for r in range(3):
        for c in range(3):
            if board[r][c]!="":
                txt=font.render(board[r][c],True,(0,0,0))
                screen.blit(txt,(c*133+50,r*133+50))
running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        elif e.type==pygame.MOUSEBUTTONDOWN:
            x,y=e.pos
            r=int(y//133)
            c=int(x//133)
            if board[r][c]=="":
                board[r][c]=player
                player="O" if player=="X" else "X"
    draw_board()
    pygame.display.flip()
pygame.quit()
"""
    else:
        return f"""import pygame
pygame.init()
screen=pygame.display.set_mode((640,480))
pygame.display.set_caption("{data['idea']}")
running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
    screen.fill((100,150,200))
    pygame.display.flip()
pygame.quit()
"""

#README Generator
def generate_readme(data):
    readme = f"# {data['idea']}\n\n"
    readme += f"**Genre:** {data['genre'].capitalize()}\n\n"
    
    if data["genre"] in ["platformer", "shooter", "puzzle"]:
        readme += f"- **Mechanics:** {', '.join(data.get('mechanics', []))}\n"
        readme += f"- **Enemies:** {', '.join(data.get('enemies', []))}\n"
        readme += f"- **Levels:** {data.get('levels', 1)}\n"
        readme += f"- **Art Style:** {data.get('art_style', 'pixel').capitalize()}\n"
    else:
        readme += f"- **Game Type:** {data.get('game_type', 'Minigame')}\n"
    
    readme += "\n## How to Play\n"
    readme += "1. Install [Python](https://www.python.org/downloads/)\n"
    readme += "2. Install Pygame with `pip install pygame`\n"
    readme += "3. Run the game with `python main.py`\n\n"
    readme += "Enjoy your game!\n"
    return readme

#Project Generator
def generate_project(data):
    slug=slugify(data["idea"])
    zip_buffer=io.BytesIO()
    assets=prepare_assets(data)
    in_memory_files={}

    design={"meta":{"title":data["idea"],"created_at":datetime.utcnow().isoformat()+"Z"},
            "concept":data,
            "progression":{"levels":generate_levels(data)}}
    in_memory_files["design.json"]=json.dumps(design,indent=4).encode("utf-8")
    in_memory_files["main.py"]=generate_main_py(data).encode("utf-8")
    in_memory_files["README.md"]=generate_readme(data).encode("utf-8")

    for name, content in assets.items():
        in_memory_files[f"assets/sprites/{name}.png"]=content

    with zipfile.ZipFile(zip_buffer,'w',zipfile.ZIP_DEFLATED) as zipf:
        for path,content in in_memory_files.items():
            zipf.writestr(path,content)
    zip_buffer.seek(0)
    return slug, zip_buffer

# Streamlit UI
st.title("🎮 Gamora- Game Design & Generation Tool")

idea=st.text_input("Enter your game idea","A cyberpunk robot shooter")
genre_ai=ai_suggest_genre(idea)
st.write(f"**Suggested genre:** {genre_ai}")
data={"idea":idea,"genre":genre_ai}

if genre_ai in ["platformer","shooter","puzzle"]:
    suggested_mechanics=ai_suggest_mechanics(idea)
    data["mechanics"]=st.multiselect("Select mechanics", suggested_mechanics, default=suggested_mechanics)
    suggested_enemies=ai_suggest_enemies(idea)
    data["enemies"]=st.multiselect("Select enemies", suggested_enemies, default=suggested_enemies)
    data["levels"]=st.number_input("Number of levels",1,10,3)
    if genre_ai in ["platformer","shooter"]:
        data["base_collectibles"]=st.number_input("Base collectibles per level",0,20,3)
    data["art_style"]=st.selectbox("Art style",["pixel","cartoon","minimalist"],index=0)
else:  
    minigames=["Tic Tac Toe","Connect Four","Memory"]
    data["game_type"]=st.selectbox("Minigame type",minigames)
    data["levels"]=1

if st.button("Generate & Download Game"):
    slug, zip_buffer=generate_project(data)
    st.download_button("Download Ready to Play Game",
                       zip_buffer,
                       file_name=f"{slug}.zip",
                       mime="application/zip")
    st.success(f"Game '{data['idea']}' generated successfully! 🎉")
