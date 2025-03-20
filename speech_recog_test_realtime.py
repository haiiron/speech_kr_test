import speech_recognition as sr
import keyboard
import time

if __name__ == '__main__':

    r = sr.Recognizer()

    print("음성 인식 시작... (종료하려면 'q'를 누르세요)")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # 주변 소음 보정

        while True:
            if keyboard.is_pressed('q'):  # 'q' = 종료
                print("\n음성 인식 종료.")
                break

            print("\n음성을 입력하세요...")
            start_time = time.time()

            try:
                audio = r.listen(source, timeout=5)  # 5초 대기
                text = r.recognize_google(audio, language="ko-KR")
                # text = r.recognize_whisper(audio, language='ko')
                print("인식된 텍스트:", text)
            except sr.UnknownValueError:
                print("음성을 인식할 수 없습니다.")
            except sr.RequestError:
                print("Google API 요청 실패.")

            print("수행시간:", time.time() - start_time)

