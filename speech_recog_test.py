import speech_recognition as sr
import time
import json

wav_list = ["노인남여_노인대화77_F_김XX_62_제주_실내_84050",
            "노인남여_노인대화77_F_김XX_62_제주_실내_84051",
            "노인남여_노인대화77_F_김XX_62_제주_실내_84052",
            "노인남여_노인대화77_F_김XX_62_제주_실내_84053",
            "노인남여_노인대화77_F_김XX_62_제주_실내_84054"]


if __name__ == '__main__':
    r = sr.Recognizer()

    for wav in wav_list:
        label = None

        kr_audio = sr.AudioFile("datasets/OldPeople_Voice/"+wav+".WAV")
        label_data = "datasets/OldPeople_Voice/label/" + wav + ".json"
        with open(label_data, "r") as f:
            label = json.load(f)["발화정보"]["stt"]

        with kr_audio as source:
            audio = r.record(source)
        # sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시

        # s = time.time()
        # print(json.loads(r.recognize_vosk(audio, language='ko'))["text"])
        # print("vosk 수행시간 : ", time.time() - s,"\n")

        s = time.time()
        google_recog = r.recognize_google(audio, language='ko-KR')
        print("google 수행시간 : ", time.time() - s, "\n")

        s = time.time()
        whisper_recog = r.recognize_whisper(audio, language='ko')
        print("whisper 수행시간 : ", time.time() - s, "\n")

        print("  실제  : ", label)
        print("google : ", google_recog)
        print("whisper: ", whisper_recog)
