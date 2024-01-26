from moviepy.editor import CompositeVideoClip, TextClip
import random
import whisper
from whisper.utils import get_writer
import re
import string


model_name = "large"
model = whisper.load_model(model_name, download_root="models")

def get_srt(name_project):
    audio_path = "temporaire/"+name_project+"_audio.mp3"
    audio = whisper.load_audio(audio_path)
    result = whisper.transcribe(model, audio, word_timestamps=True, language='fr')

    srt_writer = get_writer("srt", "temporaire/")
    srt_writer(result, audio_path, {"max_line_width": 16, "max_line_count": 1})
    srt_writer(result, "temporaire/"+name_project+"_audio_words.mp3", {"max_words_per_line": 1})

def load_srt(chemin_fichier):
    sous_titres = []
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            bloc = []
            for ligne in fichier:
                if ligne.strip() == '':
                    if bloc:
                        sous_titres.append(bloc)
                        bloc = []
                elif '-->' in ligne:
                    temps = ligne.split('-->')
                    temps_debut = temps[0].strip()
                    temps_fin = temps[1].strip()
                    bloc.append(temps_debut)
                    bloc.append(temps_fin)
                elif bloc:
                    bloc.append(ligne.strip())
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

    return sous_titres

def convertir_timestamp_en_secondes(timestamp):
    heures, minutes, rest = timestamp.split(':')
    secondes, millisecondes = rest.split(',')
    temps_total = int(heures) * 3600 + int(minutes) * 60 + int(secondes) + int(millisecondes) / 1000
    return temps_total

def choisir_aleatoirement():
    green = '#33FF36'
    yellow = '#FFEC33'
    red = '#FF5733'
    return random.choice([green, yellow, red])

def are_equal_without_punctuation(str1, str2):
    # Supprimer la ponctuation et comparer les chaînes
    def remove_punctuation(input_str):
        # Supprimer les signes de ponctuation de la chaîne
        translator = str.maketrans("", "", string.punctuation)
        return input_str.translate(translator)
    cleaned_str1 = remove_punctuation(str1)
    cleaned_str2 = remove_punctuation(str2)
    return cleaned_str1 == cleaned_str2

def make_srt(name_project, video, name_srt  = '', name_srt_words = ''):
    audio_name = name_project + "_audio"
    path_font = 'input/Montserrat-Black.ttf'

    if name_srt  =='' and  name_srt_words == '' :
        get_srt(name_project)
    subtitles = load_srt("temporaire/"+audio_name+".srt")
    subtitles_precis = load_srt("temporaire/"+audio_name+"_words.srt")

    shift = 100
    shift_2= -66

    size_border_1 = 84
    size_txt_1 = 63
    size_border_2 = 75
    size_txt_2 = 57

    couleur = 'white'  
    contour = 'black'
    clips = []
    i = 0
    for j in range(0, len(subtitles), 2): 
        sub1 = subtitles[j]
        if j + 1 < len(subtitles): 
            sub2 = subtitles[j+1]
        #print('-', sub1[2])
        for mot in re.split(r"[ ' -]", sub1[2]):
            if i<len(subtitles_precis) and are_equal_without_punctuation(mot, subtitles_precis[i][2] ):
                mot_highlight = '<span foreground="' + choisir_aleatoirement()+'" >'
                mot_highlight += mot.upper()
                mot_highlight += '</span>'
                texte = sub1[2].upper().replace(mot.upper(), mot_highlight)
                if i == 0 : 
                    start = convertir_timestamp_en_secondes(subtitles_precis[i][0])
                else : start = end
                end = convertir_timestamp_en_secondes(subtitles_precis[i][1])
                #print(start, end, subtitles_precis[i][2])
                video_height = video.h 
                vertical_position = (video_height / 2) -54

                txt_ = sub1[2].upper()
                border = TextClip(txt_, font=path_font, fontsize=size_border_1, color=couleur, stroke_color=contour, stroke_width=15).set_position(('center', vertical_position)).set_start(start).set_end(end)
                txt = TextClip(texte,font="Montserrat Black",  fontsize=size_txt_1, color=couleur, stroke_color=contour, stroke_width=0, method="pango").set_position('center').set_start(start).set_end(end)
                    

                vertical_position = (video_height / 2) -54 + shift
                vertical_position_ = (video_height / 2) +shift_2 + shift
                border_2 = TextClip(sub2[2].upper(), font=path_font, fontsize=size_border_2, color=couleur, stroke_color=contour, stroke_width=15).set_position(('center', vertical_position)).set_start(start).set_end(end)
                txt_2 = TextClip(sub2[2].upper(),font="Montserrat Black",  fontsize=size_txt_2, color=couleur, stroke_color=contour, stroke_width=0, method="pango").set_position(('center', vertical_position_)).set_start(start).set_end(end)

                clips.append(border)
                clips.append(txt)
                clips.append(border_2)
                clips.append(txt_2)

                i += 1
        #print('--', sub2[2])
        for mot in re.split(r"[ ' -]", sub2[2]):
            if i<len(subtitles_precis) and are_equal_without_punctuation(mot, subtitles_precis[i][2] ):
                mot_highlight = '<span foreground="' + choisir_aleatoirement()+'" >'
                mot_highlight += mot.upper()
                mot_highlight += '</span>'
                texte = sub2[2].upper().replace(mot.upper(), mot_highlight)
                start = end
                end = convertir_timestamp_en_secondes(subtitles_precis[i][1])
                #print(start, end, subtitles_precis[i][2])
                video_height = video.h 
                vertical_position = (video_height / 2) -54

                txt_ = sub2[2].upper()
                border = TextClip(sub1[2].upper(), font=path_font, fontsize=size_border_2, color=couleur, stroke_color=contour, stroke_width=15).set_position(('center', vertical_position)).set_start(start).set_end(end)
                txt = TextClip(sub1[2].upper(),font="Montserrat Black",  fontsize=size_txt_2, color=couleur, stroke_color=contour, stroke_width=0, method="pango").set_position('center').set_start(start).set_end(end)
                    
            
                vertical_position = (video_height / 2) -54 + shift
                vertical_position_ = (video_height / 2) +shift_2 + shift
                border_2 = TextClip(txt_ , font=path_font, fontsize=size_border_1, color=couleur, stroke_color=contour, stroke_width=15).set_position(('center', vertical_position)).set_start(start).set_end(end)
                txt_2 = TextClip(texte ,font="Montserrat Black",  fontsize=size_txt_1, color=couleur, stroke_color=contour, stroke_width=0, method="pango").set_position(('center', vertical_position_)).set_start(start).set_end(end)

                clips.append(border)
                clips.append(txt)
                clips.append(border_2)
                clips.append(txt_2)

                i += 1

    
    return CompositeVideoClip([video, *clips ])