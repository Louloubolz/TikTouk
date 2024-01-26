import os

dossiers =  ["output/", "temporaire/", "input/" ]

for dossier in dossiers : 
    if not os.path.exists(dossier):
        os.mkdir(dossier)
