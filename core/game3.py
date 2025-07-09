import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import pygame
import threading
import time
import sys

class ChestGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Выбери уровень сложности")
        self.root.geometry("300x200")
        
        # Инициализация pygame
        pygame.init()
        pygame.mixer.init()
        
        self.chest_image = None
        self.chest_win_image = None
        self.dead_image = None
        self.active_windows = []
        self.error_windows = []
        self.winning_chest = None
        self.current_level = None
        self.keep_spawning_errors = False
        
        # Интерфейс
        self.label = tk.Label(root, text="Выбери уровень:", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.btn_level1 = tk.Button(root, text="Level 1", command=lambda: self.start_level(4))
        self.btn_level1.pack(pady=5)
        
        self.btn_level2 = tk.Button(root, text="Level 2", command=lambda: self.start_level(6))
        self.btn_level2.pack(pady=5)
        
        self.btn_level3 = tk.Button(root, text="Level 3", command=lambda: self.start_level(8))
        self.btn_level3.pack(pady=5)
        
        self.load_images()
    
    def load_images(self):
        """Загружает изображения сундуков."""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
            chest_path = os.path.join(base_dir, "source", "image", "chest.png")
            pil_chest = Image.open(chest_path)
            self.chest_image = ImageTk.PhotoImage(pil_chest, master=self.root)
            
            chest_win_path = os.path.join(base_dir, "source", "image", "chest_win.png")
            pil_chest_win = Image.open(chest_win_path)
            self.chest_win_image = ImageTk.PhotoImage(pil_chest_win, master=self.root)
            
            dead_path = os.path.join(base_dir, "source", "image", "dead.png")
            pil_dead = Image.open(dead_path)
            self.dead_image = ImageTk.PhotoImage(pil_dead, master=self.root)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображения:\n{e}")
            self.root.destroy()
    
    def show_pygame_fullscreen(self):
        """Показывает полноэкранное изображение со скримером."""
        time.sleep(1)  # Задержка перед показом
        
        try:
            # Загрузка и воспроизведение звука скримера
            music_path = os.path.join(os.path.dirname(__file__), "source", "music", "scream.mp3")
            pygame.mixer.music.load(music_path)
            
            # Создание полноэкранного окна
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screen_w = screen.get_width()
            screen_h = screen.get_height()
            
            # Загрузка и масштабирование фонового изображения
            bg_path = os.path.join(os.path.dirname(__file__), "source", "image", "dead.png")
            bg = pygame.image.load(bg_path)
            bg_scaled = pygame.transform.scale(bg, (screen_w, screen_h))
            
            pygame.display.set_caption("YOU MUST DIE")
            pygame.mixer.music.play()
            screen.blit(bg_scaled, (0, 0))
            pygame.display.flip()
            
            # Ожидание 3 секунды
            start_time = time.time()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                
                if time.time() - start_time >= 3:
                    running = False
            
            pygame.quit()
            
            # Закрываем основное окно Tkinter
            self.root.after(0, self.root.destroy)
            
        except Exception as e:
            print(f"Ошибка в полноэкранном режиме: {e}")
            self.root.destroy()
    
    def start_level(self, count):
        """Начинает уровень."""
        if self.active_windows:
            messagebox.showwarning("Ошибка", "Сначала закройте все сундуки!")
            return
        
        self.current_level = count
        self.lock_buttons()
        self.winning_chest = random.randint(0, count - 1)
        self.open_windows(count)
    
    def lock_buttons(self):
        """Блокирует кнопки выбора уровня."""
        self.btn_level1.config(state=tk.DISABLED)
        self.btn_level2.config(state=tk.DISABLED)
        self.btn_level3.config(state=tk.DISABLED)
    
    def unlock_buttons(self):
        """Разблокирует кнопки выбора уровня."""
        self.btn_level1.config(state=tk.NORMAL)
        self.btn_level2.config(state=tk.NORMAL)
        self.btn_level3.config(state=tk.NORMAL)
    
    def open_windows(self, count):
        """Открывает окна с сундуками."""
        for i in range(count):
            window = tk.Toplevel(self.root)
            window.title(f"Сундук {i + 1}")
            window.geometry("200x200")
            
            btn = tk.Button(
                window,
                image=self.chest_image,
                command=lambda w=window, idx=i: self.on_chest_click(w, idx)
            )
            btn.pack(pady=20)
            
            self.active_windows.append(window)
    
    def play_scary_music(self):
        """Воспроизводит страшную музыку."""
        time.sleep(1)
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            music_path = os.path.join(base_dir, "source", "music", "scary.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Не удалось воспроизвести музыку: {e}")
    
    def start_error_spam(self):
        """Начинает спам ошибками."""
        self.keep_spawning_errors = True
        threading.Thread(target=self.spawn_errors, daemon=True).start()
    
    def spawn_errors(self):
        """Создает окна с ошибками."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        while self.keep_spawning_errors:
            error_window = tk.Toplevel(self.root)
            error_window.overrideredirect(True)
            
            x = random.randint(0, screen_width - 200)
            y = random.randint(0, screen_height - 100)
            error_window.geometry(f"200x100+{x}+{y}")
            
            error_window.configure(bg='red')
            label = tk.Label(error_window, 
                           text="YOU MUST DIE", 
                           font=("Arial", 16, "bold"), 
                           fg='white', 
                           bg='red')
            label.pack(expand=True)
            
            self.error_windows.append(error_window)
            time.sleep(random.uniform(0.05, 0.2))
    
    def stop_error_spam(self):
        """Останавливает спам ошибками."""
        self.keep_spawning_errors = False
        for window in self.error_windows:
            try:
                window.destroy()
            except:
                pass
        self.error_windows.clear()
    
    def delayed_close(self, delay=15):
        """Закрывает окна с задержкой."""
        time.sleep(delay)
        self.stop_error_spam()
        self.close_all_windows()
        
        # Для Level 3 показываем полноэкранное окно Pygame
        if self.current_level == 8:
            threading.Thread(target=self.show_pygame_fullscreen, daemon=True).start()
    
    def on_chest_click(self, window, chest_index):
        """Обрабатывает клик по сундуку."""
        if chest_index == self.winning_chest:
            win_image = self.dead_image if self.current_level == 8 else self.chest_win_image
            message_text = "HELP!" if self.current_level == 8 else "Ты нашёл сокровище! 🎉"
            
            for widget in window.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(image=win_image)
                    widget.config(state=tk.DISABLED)
            
            messagebox.showinfo("Результат", message_text)
            
            if self.current_level == 8:
                threading.Thread(target=self.play_scary_music, daemon=True).start()
                threading.Thread(target=self.start_error_spam, daemon=True).start()
                threading.Thread(target=self.delayed_close, daemon=True).start()
            else:
                self.close_all_windows()
        else:
            messagebox.showinfo("Мимо", "Этот сундук пуст. Попробуй другой!")
    
    def close_all_windows(self):
        """Закрывает все окна."""
        pygame.mixer.music.stop()
        self.stop_error_spam()
        self.root.after(0, self._close_windows)
    
    def _close_windows(self):
        """Фактическое закрытие окон."""
        for window in self.active_windows:
            try:
                window.destroy()
            except:
                pass
        self.active_windows.clear()
        self.unlock_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    game = ChestGame(root)
    root.mainloop()