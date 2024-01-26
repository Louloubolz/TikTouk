from tiktok_uploader.upload import upload_video
import random
import os
import pandas as pd
import shutil
from instagrapi import Client


def publish(): 

    files = os.listdir("output/")
    if len(files)!=0:
        path = random.choice(files)
        df = pd.read_csv('titres.csv')
        description = df.loc[df['vod_name'] == path, 'titre'].iloc[0]

    publish_tiktok("output/"+path, description)
    publish_insta("output/"+path, description)

    deplacer_fichier("output/"+path, "archive/"+path )
    return 0 

def publish_tiktok(path, description):

    print("uploading on TikTouk")

    upload_video(path, 
    description=description, 
    cookies='input/tiktok_cookies.txt')

    print("succesfully uploaded")

    return True

def publish_insta(chemin_video, description):
    # Remplacez ces informations par vos propres identifiants Instagram
    username = 'votre_nom_utilisateur'
    password = 'votre_mot_de_passe'

    # Créez une instance du client Instagrapi
    client = Client()

    # Connectez-vous à votre compte Instagram
    client.login(username, password)

    try:
        # Chargez la vidéo à partir du chemin spécifié
        media = client.clip_upload(chemin_video, description)
        print("Reel posté avec succès!")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    # Déconnectez-vous du compte Instagram
    client.logout()



def publish_youtube(path, description): 

    return 0 


def deplacer_fichier(source, destination):
    shutil.move(source, destination)
