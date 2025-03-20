import speech_recognition as sr
import time
import json


if __name__ == '__main__':
    r = sr.Recognizer()
    kr_audio = sr.AudioFile('datasets/KsponSpeech_eval/eval_other/test2.wav')

    with kr_audio as source:
        audio = r.record(source)
    # sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시

    s = time.time()
    print(json.loads(r.recognize_vosk(audio, language='ko'))["text"])
    print("vosk 수행시간 : ", time.time() - s,"\n")

    s = time.time()
    print(r.recognize_google(audio, language='ko-KR'))
    print("google 수행시간 : ", time.time() - s, "\n")

    s = time.time()
    print(r.recognize_whisper(audio, language='ko'))
    print("whisper 수행시간 : ", time.time() - s, "\n")

