from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import random
import subtitles
from moviepy.editor import VideoFileClip, clips_array
import random


def crop_video(video): 
    video = video.resize((2332, 1313))

    # Calculate the center of the video
    center_x = video.size[0] // 2
    center_y = video.size[1] // 2

    # Define the dimensions for cropping (1080x1920)
    crop_width = 1080
    crop_height = 1313

    # Calculate the cropping region
    x1 = center_x - crop_width // 2
    y1 = center_y - crop_height // 2
    x2 = center_x + crop_width // 2
    y2 = center_y + crop_height // 2

    # Crop the video clip
    video = video.crop(x1=x1, y1=y1, x2=x2, y2=y2)
    return video 


def create_vertical_split_video(name_session, name_project, name_srt  = '', name_srt_words = ''):

    video_top = "input/" + name_project + "_top.mp4"
    video_background_path = "input/" + name_session+'_background.mp4'
    output_path = "output/" + name_project +  ".mp4"

    # Charger les vidéos d'entrée
    print("-------- 3.1 : Importing Vidéo")
    video_t = VideoFileClip(video_top)
    video_b = VideoFileClip(video_background_path)
     # Générer un point de départ aléatoire
    
    total_duration = video_t.duration
    start_time = random.randint(120, int(total_duration) - 180) 
    video_t = video_t.subclip(start_time )
    video_t = video_t.set_duration(random.randint(2, 3))
    video_t_duration = round(video_t.duration); 
    video_b_duration = round(video_b.duration); 
    diff = - video_t_duration + video_b_duration -1

    if diff < 0 :
        raise Exception("**** ERROR la video donnée est plus courte que l'audio généré *****")

    start = random.randint(0, diff)

    video_b = video_b.subclip(start)
    video_b = video_b.set_duration(video_t.duration)

    print(video_b.duration)
    print(video_t.duration)

    # Ajuster la taille de la vidéo 2 pour qu'elle ait la même hauteur que la vidéo 1
    video_t = video_t.resize(( 1080, 608))
    video_b = crop_video(video_b)

    # Créer une composition verticale des deux vidéos
    final_video = clips_array([[video_t], [video_b]])

    print("-------- 3.2 : Generating SRT")

    video_final = subtitles.make_srt(name_project, final_video, name_srt , name_srt_words)

    print("-------- 3.3 : Rendering Video")

    # Écrire la vidéo résultante dans le fichier de sortie
    final_video.write_videofile(output_path, codec="libx264", bitrate="8000k", temp_audiofile="temp-audio.m4a", remove_temp=True, audio_codec="aac")


def combine_video_audio(name_project, name_session, name_srt  = '', name_srt_words = ''):

    video_background_path = "input/" + name_session+'_background.mp4'
    music_name ="input/" + name_session+'_background.mp3'
    audio_path = "temporaire/" + name_project +  "_audio.mp3"
    output_path = "output/" + name_project +  ".mp4"

    print("-------- 3.1 : Importing Vidéo")

    video_clip = VideoFileClip(video_background_path)
    video_clip = video_clip.resize((3413, 1920))

    # Calculate the center of the video
    center_x = video_clip.size[0] // 2
    center_y = video_clip.size[1] // 2

    # Define the dimensions for cropping (1080x1920)
    crop_width = 1080
    crop_height = 1920

    # Calculate the cropping region
    x1 = center_x - crop_width // 2
    y1 = center_y - crop_height // 2
    x2 = center_x + crop_width // 2
    y2 = center_y + crop_height // 2

    # Crop the video clip
    video_clip = video_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

    # Resize the cropped clip to 1080x1920 if needed
    #video_clip = video_clip.resize((1080, 1920))

    # Load audio clip
    audio_clip = AudioFileClip(audio_path)

    #Here, we will cut the video randomly so that it matches the audio duration
    video_duration = round(video_clip.duration)
    audio_duration = round(audio_clip.duration)
    diff = video_duration - audio_duration-1

    if diff < 0 :
        raise Exception("**** ERROR la video donnée est plus courte que l'audio généré *****")

    start = random.randint(0, diff)

    # Trim video based on start and end times
    video_clip = video_clip.subclip(start)
    video_clip = video_clip.set_duration(audio_clip.duration)

    print("-------- 3.2 : Generating SRT")

    video_final = subtitles.make_srt(name_project, video_clip, name_srt , name_srt_words)

    # Add music
    music = AudioFileClip(music_name)
    music = music.subclip(6).volumex(0.5)
    music = music.set_duration(video_final.duration)

    new_audioclip = CompositeAudioClip([music, audio_clip])
    video_final.audio = new_audioclip
    
    print("-------- 3.3 : Rendering Video")

    video_final.write_videofile(output_path, codec="libx264", bitrate="8000k", temp_audiofile="temp-audio.m4a", remove_temp=True, audio_codec="aac")

    video_clip.close()
    video_final.close()