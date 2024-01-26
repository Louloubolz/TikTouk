from openai import OpenAI
import json




def GetStory(prompt = "Raconte une andecdote réelle qui est arrivée dans l'histoire. raconte de facon extremement simple, il faut que le lecteur comprenne tout sans contexte et qu'il soit très intrigué par la première phrase de l'histoire. L'histoire doit avoir du sens, être longue, respecter les 5 étapes d'un récit : la situation initiale, l'élément modificateur, les péripéties, l'élément rééquilibrant, la situation finale."):

    client = OpenAI(
    api_key="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",
    )

    less2500 = False
    text = ""

    while not less2500 :

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt + "\nTu devras également donner un titre aguicheur, qui invite le lecteur à découvrir la fin de la vidéo.\nA la suite de ce titre, tu donneras une série de hashtags très connus sur la plateforme TikTok, les hashtags doivent être en rapport avec l'histoire, tu dois en mettre au moins 10.\nLa réponse doit être sous format JSON en séparant 'hisoire' et 'titre', les hastags seront dans le string 'titre'. Le format sera donc {'histoire': 'histoire longue au format string, sans le titre, ni les hastags','titre': 'le titre suivi des hashtags (les hashatags sont séparés par des espaces)'}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        try :
            result = json.loads(chat_completion.choices[0].message.content)
            text = result["histoire"] + " Abonne toi pour la suite !"
            if len(text) <= 2500 :
                less2500 = True
            else :
                print("Story is too long, a new one is being generated !")
        except :
            print("Impossible to parse, a new story is being generated !")



    return text, result["titre"]