import pygame
import sys
import os
import ctypes
import random
import time
import subprocess
import tkinter as tk
from pathlib import Path

# Скрытие консоли
if sys.platform == "win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def run_community():
    # Путь к виртуальному окружению (относительно main.py)
    VENV_DIR = Path(__file__).parent.parent / "lib"
    
    # Путь к community.py (предполагаем, что он в той же папке)
    COMMUNITY_SCRIPT = Path(__file__).parent / "community.py"
    
    # Выбираем python.exe в зависимости от ОС
    if os.name == "nt":  # Windows
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:  # Linux/MacOS
        python_path = VENV_DIR / "bin" / "python"
    
    # Проверяем, что пути существуют
    if not python_path.exists():
        print(f"Ошибка: {python_path} не найден!")
        return
    
    if not COMMUNITY_SCRIPT.exists():
        print(f"Ошибка: {COMMUNITY_SCRIPT} не найден!")
        return
    
    # Запускаем community.py через интерпретатор из venv
    subprocess.Popen([str(python_path), str(COMMUNITY_SCRIPT)])

def run_game1():
    VENV_DIR = Path(__file__).parent.parent / "lib"
    COMMUNITY_SCRIPT = Path(__file__).parent / "game1.py"

    if os.name == "nt":
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_path = VENV_DIR / "bin" / "python"

    if not python_path.exists():
        print(f"Ошибка: {python_path} не найден!")
        return
    
    if not COMMUNITY_SCRIPT.exists():
        print(f"Ошибка: {COMMUNITY_SCRIPT} не найден!")
        return

    subprocess.Popen([str(python_path), str(COMMUNITY_SCRIPT)])

def run_game2():
    VENV_DIR = Path(__file__).parent.parent / "lib"
    COMMUNITY_SCRIPT = Path(__file__).parent / "game2.py"

    if os.name == "nt":
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_path = VENV_DIR / "bin" / "python"

    if not python_path.exists():
        print(f"Ошибка: {python_path} не найден!")
        return
    
    if not COMMUNITY_SCRIPT.exists():
        print(f"Ошибка: {COMMUNITY_SCRIPT} не найден!")
        return

    subprocess.Popen([str(python_path), str(COMMUNITY_SCRIPT)])    

def run_game3():
    VENV_DIR = Path(__file__).parent.parent / "lib"
    COMMUNITY_SCRIPT = Path(__file__).parent / "game3.py"

    if os.name == "nt":
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_path = VENV_DIR / "bin" / "python"

    if not python_path.exists():
        print(f"Ошибка: {python_path} не найден!")
        return
    
    if not COMMUNITY_SCRIPT.exists():
        print(f"Ошибка: {COMMUNITY_SCRIPT} не найден!")
        return

    subprocess.Popen([str(python_path), str(COMMUNITY_SCRIPT)])   

def music():
    VENV_DIR = Path(__file__).parent.parent / "lib"
    COMMUNITY_SCRIPT = Path(__file__).parent / "music_player.py"

    if os.name == "nt":
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_path = VENV_DIR / "bin" / "python"

    if not python_path.exists():
        print(f"Ошибка: {python_path} не найден!")
        return
    
    if not COMMUNITY_SCRIPT.exists():
        print(f"Ошибка: {COMMUNITY_SCRIPT} не найден!")
        return

    subprocess.Popen([str(python_path), str(COMMUNITY_SCRIPT)]) 

def game_hub():
    root = tk.Tk()
    root.title("game hub")
    root.geometry("300x300")

    button = tk.Button(
        root,
        text="shooter",
        command=run_game1
    )
    button2 = tk.Button(
        root,
        text="math",
        command=run_game2
    )
    button3 = tk.Button(
        root,
        text="chest",
        command=run_game3
    )
    button.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)
    root.mainloop()

def settings():
    root = tk.Tk()
    root.title("settings")
    root.geometry("300x300")

def create_menu():
    # Создаем новое окно меню
    root = tk.Tk()
    root.title("Menu")
    root.geometry("400x400")

    button = tk.Button(
        root,
        text="Community",
        command=run_community
    )
    button2 = tk.Button(
        root,
        text="game",
        command=game_hub
    )
    button4 = tk.Button(
        root,
        text="settings",
        command=settings
    )
    button3 = tk.Button(
        root,
        text="music",
        command=music
    )
    button2.pack(pady=10)
    button3.pack(pady=10)
    button4.pack(pady=10)
    button.pack(pady=10)
    
    root.mainloop()

pygame.init()
bg_path = os.path.join(os.path.dirname(__file__), "source", "image", "bg.png")
icon_path = os.path.join(os.path.dirname(__file__), "source", "image", "icon.ico")

try:
    bg = pygame.image.load(bg_path)
    icon = pygame.image.load(icon_path)
except:
    bg = pygame.Surface((250, 250))
    bg.fill((50, 100, 200))
    icon = None

screen = pygame.display.set_mode((250, 250))
pygame.display.set_caption("ёрик")
if icon:
    pygame.display.set_icon(icon)
clock = pygame.time.Clock()
bg_scaled = pygame.transform.scale(bg, (250, 250))

# Главный цикл
run = True
while run:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # ПКМ
                create_menu()  # Создаем новое меню при каждом нажатии ПКМ
    
    # Отрисовка
    screen.blit(bg_scaled, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()