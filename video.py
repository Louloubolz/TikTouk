from pytube import YouTube
import os 
import random

def choisir_fichiers_aleatoires(dossier = 'input/'):

    fichiers_mp4 = [f for f in os.listdir(dossier) if f.endswith('.mp4')]
    fichiers_mp3 = [f for f in os.listdir(dossier) if f.endswith('.mp3')]
    fichier_mp4_aleatoire = random.choice(fichiers_mp4) if fichiers_mp4 else None
    fichier_mp3_aleatoire = random.choice(fichiers_mp3) if fichiers_mp3 else None
    return dossier + fichier_mp4_aleatoire, dossier + fichier_mp3_aleatoire


def get_yt_video(link, name_project):
    if "youtube.com" in link or "youtu.be" in link:
        path = 'input/'
        video = YouTube(link)
        stream = video.streams.get_highest_resolution()
        stream.download(path, name_project)
    if link == '': 
        os.rename(choisir_fichiers_aleatoires()[0], 'input/' + name_project)
    elif os.path.isfile(link): os.rename(link, 'input/' + name_project)


def get_music(link, name_project):
    if "youtube.com" in link or "youtu.be" in link:
        video = YouTube(link)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(output_path="input/", filename = name_project)
    elif link == '': 
        os.rename(choisir_fichiers_aleatoires()[1], 'input/' + name_project)
    elif os.path.isfile(link): os.rename(link, 'input/' + name_project)
