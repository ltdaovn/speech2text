import argparse
import speech_recognition as sr
from pydub import AudioSegment

ap=argparse.ArgumentParser(description='Speech to text')
ap.add_argument('-i', '--input', required=True, help='path to input audio file')
ap.add_argument('-o', '--output', required=True, help='path to output text')

args=vars(ap.parse_args())

# convert to .wav file
sound = AudioSegment.from_mp3(args['input'])
sound.export("./audio.wav", format='wav')
recognizer = sr.Recognizer()

with sr.AudioFile("./audio.wav") as source:
    recorded_audio = recognizer.listen(source)
    print("Done recording")

    ''' Recorgnizing the Audio '''
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="vi-VI"
            )
        print("Decoded Text : {}".format(text))

        # Save to file
        file = open(args['output'], 'w', encoding="utf-8")
        file.write(text)
        file.close()

    except Exception as ex:
        print(ex)