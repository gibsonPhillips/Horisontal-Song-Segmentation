from annotated_intake import *
import os

def getAnnotatedBeats():
    for song in os.scandir("ground_truth/Beats_Downbeats"):
        anno_beats = beat_intake(song)
        print(anno_beats)

