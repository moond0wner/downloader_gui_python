from tkinter import *
from tkinter import ttk
import os
import requests
from pytube import YouTube
from moviepy.editor import VideoFileClip


class VideoInstaller(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        master.title('Установщик видео')

        self.create_widgets()

    def create_widgets(self):
        self.entry_url = Entry(root)
        self.entry_url.config(width=30)
        self.entry_url.pack()

        self.get_video_button = Button(root, text='Скачать видео', command=self.get_link)
        self.get_video_button.pack()

        self.clear_button = Button(root, text='Очистить', command=self.clear_entry)
        self.clear_button.pack()

        self.status_label = ttk.Label(root, text="")
        self.status_label.pack()

    def get_link(self):
        if not self.check_internet_connection():
            self.status_label.config(text="Отсутствует подключение к интернету")
            return
        self.url = self.entry_url.get()
        if self.url.startswith('https://www.youtube.com/watch?v=') or self.url.startswith('https://youtu.be/'):
            try:
                self.video = self.create_video(self.url)
            except Exception as ex:
                self.status_label.config(text=f"Произошла ошибка: {ex}")
        else:
            self.status_label.config(text="Недействительный URL-адрес YouTube")

    def clear_entry(self):
        self.entry_url.delete(0, END)
        self.status_label.config(text="")

    def check_internet_connection(self):
        try:
            requests.get("https://www.youtube.com/")
            return True
        except requests.ConnectionError:
            return False

    def create_video(self, url):
        try:
            self.video = self.url
            self.youtube = YouTube(self.video).streams.get_highest_resolution()
            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            self.path = self.youtube.download(downloads_dir)
            self.status_label.config(text='Ваше видео скачано!')
        except Exception as ex:
            self.label = Label(root, text=f'Ошибка: {ex}')
            self.label.pack()
            return None


class MusicInstaller(Frame):
    def __init__(self, master):
        self.master = master
        master.title("Установщик музыки")

        self.create_widgets()

    def create_widgets(self):
        self.entry_url = Entry(root)
        self.entry_url.config(width=30)
        self.entry_url.pack()

        self.get_video_button = Button(root, text='Скачать музыку', command=self.download_song)
        self.get_video_button.pack()

        self.clear_button = Button(root, text='Очистить', command=self.clear_entry)
        self.clear_button.pack()

        self.status_label = ttk.Label(root, text="")
        self.status_label.pack()

    def download_song(self):
        self.url = self.entry_url.get()

        if not self.check_internet_connection():
            self.status_label.config(text="Отсутствует подключение к интернету")
            return


        if self.url.startswith('https://www.youtube.com/watch?v=') or self.url.startswith('https://youtu.be/'):
            try:
                self.music = YouTube(self.url)
                self.result = self.music.streams.filter().first()
                downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                video_path = self.result.download(output_path=downloads_dir)

                video = VideoFileClip(video_path)
                audio_path = os.path.splitext(video_path)[0] + ".mp3"
                video.audio.write_audiofile(audio_path, fps=44100)

                video.close()
                os.remove(video_path)
                self.status_label.config(text='Ваша музыка скачана!')
            except Exception as ex:
                self.status_label.config(text=f"Произошла ошибка: {ex}")
        else:
            self.status_label.config(text="Недействительный URL-адрес YouTube")


    def check_internet_connection(self):
        try:
            requests.get("https://www.youtube.com/")
            return True
        except requests.ConnectionError:
            return False

    def clear_entry(self):
        self.entry_url.delete(0, END)
        self.status_label.config(text="")

class StartMenu:
    def __init__(self, master):
        self.master = master
        master.title("Установщик")

        # Создаем основную рамку
        self.main_frame = Frame(master)
        self.main_frame.pack(padx=20, pady=20)

        # Создаем заголовок
        self.title_label = Label(self.main_frame, text="Выберите, что вы хотите установить:", font=("Arial", 10))
        self.title_label.pack(pady=10)

        # Создаем кнопки для выбора установки видео или музыки
        self.video_button = Button(self.main_frame, text="Установить видео из ютуба", command=self.install_video)
        self.video_button.pack(pady=10)

        self.musicyt_button = Button(self.main_frame, text="Установить музыку из ютуба", command=self.install_music)
        self.musicyt_button.pack(pady=10)

    def install_video(self):
        # Закрываем стартовое меню
        self.main_frame.destroy()

        # Создаем и запускаем установщик видео
        video_installer = VideoInstaller(self.master)

    def install_music(self):
        # Закрываем стартовое меню
        self.main_frame.destroy()

        # Создаем и запускаем установщик музыки
        music_installerYT = MusicInstaller(self.master)

if __name__ == "__main__":
    root = Tk()
    # Запустить приложение посередине экрана
    # Получаем ширину и высоту экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    window_width = 300
    window_height = 300
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Устанавливаем размер и положение окна
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    start_menu = StartMenu(root)
    root.mainloop()