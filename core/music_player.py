import pygame
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import sys
from pathlib import Path

# Инициализация Pygame
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.is_playing = False
        self.current_file = None
        self.music_folder = Path(__file__).parent / "music_player"
        self.setup_ui()
        self.check_music_end()  # Запускаем проверку окончания трека

    def setup_ui(self):
        """Настройка интерфейса"""
        self.root.title("Музыкальный проигрыватель")
        self.root.geometry("600x500")
        
        # Вкладки
        self.tab_control = ttk.Notebook(self.root)
        self.main_tab = ttk.Frame(self.tab_control)
        self.library_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.main_tab, text="Управление")
        self.tab_control.add(self.library_tab, text="Библиотека")
        self.tab_control.pack(expand=1, fill="both")
        
        # Основная вкладка
        self.track_label = tk.Label(self.main_tab, text="Сейчас играет: ")
        self.track_label.pack(pady=10)
        
        self.play_button = tk.Button(self.main_tab, text="Играть", command=self.toggle_play)
        self.play_button.pack(pady=5)
        
        self.time_label = tk.Label(self.main_tab, text="Время: 00:00")
        self.time_label.pack(pady=5)
        
        tk.Label(self.main_tab, text="Громкость").pack()
        self.volume_slider = ttk.Scale(self.main_tab, from_=0, to=100, command=self.set_volume)
        self.volume_slider.set(70)
        self.volume_slider.pack(pady=10)
        
        # Вкладка библиотеки
        self.setup_library_tab()
    
    def setup_library_tab(self):
        """Настройка вкладки библиотеки"""
        # Поиск
        search_frame = tk.Frame(self.library_tab)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.update_music_list())
        
        tk.Button(search_frame, text="Найти", command=self.update_music_list).pack(side="left")
        tk.Button(self.library_tab, text="Обновить", command=self.update_music_list).pack(pady=5)
        
        # Список треков
        self.track_list = tk.Listbox(self.library_tab, width=70, height=20)
        scrollbar = ttk.Scrollbar(self.library_tab, orient="vertical", command=self.track_list.yview)
        self.track_list.configure(yscrollcommand=scrollbar.set)
        self.track_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.track_list.bind("<Double-Button-1>", self.play_selected_from_list)
        
        self.update_music_list()
    
    def check_music_end(self):
        """Проверка окончания воспроизведения"""
        if self.is_playing and not pygame.mixer.music.get_busy():
            # Музыка закончилась
            self.is_playing = False
            self.play_button.config(text="Играть")
            self.time_label.config(text="Время: 00:00")
        
        # Проверяем каждые 500 мс
        self.root.after(500, self.check_music_end)
    
    def play_selected_from_list(self, event):
        """Воспроизведение выбранного трека из библиотеки"""
        selection = self.track_list.curselection()
        if selection:
            filename = self.track_list.get(selection[0])
            filepath = self.music_folder / filename
            
            # Останавливаем текущее воспроизведение
            if self.is_playing:
                pygame.mixer.music.stop()
                self.is_playing = False
            
            # Загружаем новую музыку
            if self.load_music(str(filepath)):
                # Переключаем на вкладку управления
                self.tab_control.select(0)
                # Сбрасываем текст кнопки на "Играть"
                self.play_button.config(text="Играть")
                # Начинаем воспроизведение
                self.toggle_play()
    
    def load_music(self, file_path):
        """Загрузка музыки с обработкой ошибок"""
        try:
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.track_label.config(text=f"Сейчас играет: {Path(file_path).name}")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
            return False
    
    def toggle_play(self):
        """Переключение воспроизведения"""
        if not self.is_playing and self.current_file:
            pygame.mixer.music.play()
            self.play_button.config(text="Стоп")
            self.is_playing = True
            self.update_time()
        elif self.is_playing:
            pygame.mixer.music.stop()
            self.play_button.config(text="Играть")
            self.is_playing = False
            self.time_label.config(text="Время: 00:00")
    
    def update_time(self):
        """Обновление времени воспроизведения"""
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() // 1000
            mins, secs = divmod(current_time, 60)
            self.time_label.config(text=f"Время: {mins:02}:{secs:02}")
            self.root.after(1000, self.update_time)
    
    def set_volume(self, value):
        """Установка громкости"""
        pygame.mixer.music.set_volume(float(value) / 100)
    
    def update_music_list(self):
        """Обновление списка музыки"""
        self.track_list.delete(0, tk.END)
        
        # Создаем папку если не существует
        self.music_folder.mkdir(exist_ok=True)
        
        search_text = self.search_entry.get().lower()
        
        for f in sorted(self.music_folder.iterdir()):
            if f.suffix.lower() in ('.mp3', '.m4a', '.ogg', '.wav'):
                if not search_text or search_text in f.name.lower():
                    self.track_list.insert(tk.END, f.name)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()