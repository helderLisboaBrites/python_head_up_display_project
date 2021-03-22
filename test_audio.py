#import pyttsx3
#import time
#engine = pyttsx3.init()
#engine.setProperty('rate', 100)
#engine.setProperty('voice', 'fr')
#engine.say('Prendre la direction est sur Avenue du Bel air vers Place des Tilleuls')
#
#voices = engine.getProperty('voices')
#for voice in voices:
#    print("Voice: %s" % voice.name)
#    print(" - ID: %s" % voice.id)
#    print(" - Languages: %s" % voice.languages)
#    print(" - Gender: %s" % voice.gender)
#    print(" - Age: %s" % voice.age)
#    print("\n")
#
#engine.runAndWait()



from gtts import gTTS
from io import BytesIO
import os

tts = gTTS("Prendre la direction est sur Avenue du Bel air vers Place des Tilleuls", lang="fr")
tts.save("test.mp3")
os.system("mpg321 -q test.mp3")


#mp3_fp.seek(0)
#base64.b64encode(mp3_fp.read())