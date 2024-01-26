import init
import video
import story
import voice
import montage
import save
import post

from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
import os
import datetime
import subprocess
import random
from tqdm import tqdm



ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


default_video_link = 'https://www.youtube.com/watch?v=ZkHKGWKq9mY'
default_prompt = "Raconte une histoire improbable, de tromperie, qui donne envie au lecteur de rester jusqu'a la fin. Construit l'anecdote pour que le lecteur soit passioné. l'histoire doit etre courte et la premiere phrase doit etre extremement accrochante, donnant envie au lecteur de découvrir l'histoire. Par exemple commence par 'cette anecdote réelle va vous retourner le cerveau' ou 'vous n'êtes pas prets pour l'histoire que je vais vous raconter'"
#"Raconte une andecdote réelle qui est arrivée dans l'histoire. raconte de facon extremement simple, il faut que le lecteur comprenne tout sans contexte et qu'il soit très intrigué par la première phrase de l'histoire. L'histoire doit avoir du sens et respecter les 5 étapes d'un récit : la situation initiale très rapidemnt, l'élément déclencheur (très intriguant, qui suscite l'impatience du lecteur'), les péripéties innatendues, la situation finale."


def create_videos(background_link, music_link, number, prompt, type = 'story', continue_session = False, path_background = '', path_music = '', path_audio = '', name_session = '', name_srt ='', name_srt_words = ''):
    
    if type == 'story': 

        if not continue_session : 

            name_session = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            print("------- 0 : Downloading Video & Music ")
            video.get_yt_video(background_link,name_session+'_background.mp4' )
            video.get_music(music_link, name_session+'_background.mp3')

            for i in range(number):
                pbar = tqdm(total=100)
                name_project = 'video' + str(i) + name_session
                
            
                pbar.set_description("------- 1 : Generating Story")
                text, titre =story.GetStory(prompt)
                pbar.update(20)
                

                pbar.set_description("------- 2 : Generating Voice")
                voice.generate_speech(text, name_project)
                pbar.update(20)

                pbar.set_description("-------- 3 : Generating Video")
                montage.combine_video_audio(name_project, name_session)
                pbar.update(50)

                pbar.set_description("-------- 4 : Saving Video")
                save.save_infos(name_project, titre)
                pbar.update(10)
        else : 
            if path_background == '':
                video.get_yt_video(background_link,name_session+'_background.mp4' )
            if path_music == '':
                video.get_music(music_link, name_session+'_background.mp3')

            name_project = 'video' + str(0) + name_session

            if path_audio == '':    
                print("------- 1 : Generating Story")
                text, titre =story.GetStory(prompt)

                print("------- 2 : Generating Voice")
                voice.generate_speech(text, name_project)

            print("-------- 3 : Generating Video")
            
            montage.combine_video_audio(name_project, name_session, name_srt , name_srt_words)

            print("-------- 4 : Saving Video")
            save.save_infos(name_project, "test")
             
    elif type == 'tedx': 
        return True



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.path_mp3 = ''
        self.path_mp4 = ''

        self.title("TikTouk.py")
        self.geometry(f"{711}x{500}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook.Tab", background="black", foreground="black", padding=[5, 2])
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=2, rowspan=3, sticky="nesw")


        self.tab1 = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.tab1, text="Histoire")
        self.entry_url_yt = ctk.CTkEntry(self.tab1, placeholder_text="Background YouTube", width=300)
        self.entry_url_yt.pack(pady=(50, 5))
        self.entry_nb_video = ctk.CTkEntry(self.tab1, placeholder_text="Number", width=100)
        self.entry_nb_video.pack(pady=5)
        self.name = ctk.CTkEntry(self.tab1, placeholder_text="Enter name for video series", width=200)
        self.name.pack(pady= 5)
        button = ctk.CTkButton(self.tab1, text="Generate Video(s)", command = lambda : self.call_create_video())
        button.pack(pady=5)
        button = ctk.CTkButton(self.tab1, text="Upload last video", command = lambda : post.publish())
        button.pack(pady=5)
        nb_video_prete = ctk.CTkLabel(self.tab1, text= "Videos ready : " + str(number_available))
        nb_video_prete.pack(pady = 5)
        self.prompt_story = ctk.CTkTextbox(self.tab1, width=500)
        self.prompt_story.pack(pady = 5)
        self.prompt_story.insert("1.0", default_prompt)

        self.b_dossier_car = ctk.CTkButton(self.tab1, text = 'Fichier Video', command=lambda : self.select_file(type = 'mp4'))
        self.b_dossier_car.pack(pady = 5)


        self.tab2 = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.tab2, text="Ted X")
        entry_url_yt_tedX = ctk.CTkEntry(self.tab2, placeholder_text="Coller un url YT")
        entry_url_yt_tedX.pack(pady=(50, 10))
        self.entry_nb_video_tedX = ctk.CTkEntry(self.tab2, placeholder_text="nombre de video")
        self.entry_nb_video_tedX.pack(pady=10)
        button = ctk.CTkButton(self.tab2, text="Export Vidéo", command = lambda : video.get_yt_video(link = self.entry_url_yt.get()))
        button.pack(pady=10)
        button = ctk.CTkButton(self.tab2, text="Poster last video", command = lambda : post.publish())
        button.pack(pady=10)
        nb_video_prete = ctk.CTkLabel(self.tab2, text= "Nb vidéo pretes : 0")
        nb_video_prete.pack(pady = 10)
        self.prompt_tedX = ctk.CTkTextbox(self.tab2)
        self.prompt_tedX.pack(pady = 10)

    def select_file(self, type):
        if type == 'mp4': 
            self.path_mp4 = filedialog.askopenfilename(title="Sélectionner un fichier mp4", filetypes=[("Fichiers mp4", "*.mp4")])

        if type == 'mp3': 
            self.path_mp3 = filedialog.askopenfilename(title="Sélectionner un fichier mp3", filetypes=[("Fichiers mp3", "*.mp3")])

    def call_create_video(self): 
        if self.path_mp4 == '': 
                    self.path_mp4 = self.entry_url_yt.get()
        # if self.path_mp3 == '': 
        #     self.path_mp3 = filedialog.askopenfilename(title="Sélectionner un fichier mp3", filetypes=[("Fichiers mp3", "*.mp3")])

        create_videos(self.path_mp4, self.path_mp3, int(self.entry_nb_video.get()), self.prompt_story.get("1.0", "end-1c"))

    def load_session(self): 
        return 0
    
    def save_session(self): 
        return 0

if __name__ == "__main__":

    # subprocess.run(["python", "init.py"])
    files = os.listdir("output/")
    number_available = len(files)
    app = App()
    app.mainloop()

    #create_videos("input/2024-01-25_14-39-11_background.mp4", "input\solas.mp3", 1, default_prompt, type = 'story',  continue_session = True, path_background = 'input\2024-01-25_14-48-31_background.mp4', path_music = 'input\2024-01-25_14-48-31_background.mp3', path_audio = 'temporaire\video02024-01-25_14-48-31_audio.mp3', name_session = '2024-01-25_14-48-31', name_srt ='temporaire\video02024-01-25_14-48-31_audio.srt', name_srt_words = 'temporaire\video02024-01-25_14-48-31_audio_words.srt')