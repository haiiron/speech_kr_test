import speech_recognition as sr
import time


if __name__ == '__main__':
    s = time.time()
    r = sr.Recognizer()
    kr_audio = sr.AudioFile('audio/wtf_voice.wav')
    # ababo.m4a

    with kr_audio as source:
        audio = r.record(source)

    #sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시 사용
    print(r.recognize_google(audio, language='ko-KR')) #-- 한글 언어 사용
    print("수행시간 : ",time.time() - s)
