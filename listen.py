import speech_recognition as sr

def dinle(data_obj):
    while (data_obj.get_mode()):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source=source)
            audio = r.listen(source)
            try:
                voice = r.recognize_google(audio, language='tr-TR')
                print(voice)
                data_obj.set_voice(voice)
            except sr.UnknownValueError:
                pass
