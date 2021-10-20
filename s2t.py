import argparse
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
ap=argparse.ArgumentParser(description='Speech to text')
ap.add_argument('-i', '--input', required=True, help='path to input audio file')
ap.add_argument('-o', '--output', required=True, help='path to output text')

args=vars(ap.parse_args())

# convert to .wav file
sound = AudioSegment.from_mp3(args['input'])
sound.export("./audio.wav", format='wav')
r = sr.Recognizer()

# with sr.AudioFile("./audio.wav") as source:
#     recorded_audio = recognizer.listen(source)
#     print("Done recording")

#     ''' Recorgnizing the Audio '''
#     try:
#         print("Recognizing the text")
#         text = recognizer.recognize_google(
#                 recorded_audio, 
#                 language="vi-VI"
#             )
#         print("Decoded Text : {}".format(text))

#         # Save to file
#         file = open(args['output'], 'w', encoding="utf-8")
#         file.write(text)
#         file.close()

#     except Exception as ex:
#         print(ex)
def get_large_audio_transcription(path):
    """
    Chia file âm thanh thành nhiều phần và áp dụng nhận dạng giọng nói
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # must be silent for at least 0.5 seconds
        # or 500 ms. adjust this value based on user
        # requirement. if the speaker stays silent for 
        # longer, increase this value. else, decrease it.        min_silence_len = 500,
        # consider it silent if quieter than -14 dBFS adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `audio-chunks` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="vi-VN")
            except sr.UnknownValueError as e:
                print("Error:" + str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    print(whole_text)

    # Save to file
    file = open(args['output'], 'w', encoding="utf-8")
    file.write(whole_text)
    file.close()
get_large_audio_transcription('./audio.wav')