from tiktok_uploader.upload import upload_video
import random
import os
import pandas as pd
import shutil



def publish(): 

    files = os.listdir("output/")
    if len(files)!=0:
        path = random.choice(files)
        df = pd.read_csv('titres.csv')
        description = df.loc[df['vod_name'] == path, 'titre'].iloc[0]

    publish_tiktok("output/"+path, description)

    deplacer_fichier("output/"+path, "archive/"+path )
    return 0 

def publish_tiktok(path, description):

    print("uploading on TikTouk")

    upload_video(path, 
    description=description, 
    cookies='input/tiktok_cookies.txt')

    print("succesfully uploaded")

    return True

def publish_insta(path, description):

    return 0

def publish_youtube(path, description): 

    return 0 


def deplacer_fichier(source, destination):
    shutil.move(source, destination)
