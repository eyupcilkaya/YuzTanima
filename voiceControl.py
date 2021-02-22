from cv2 import cv2

Tr2Eng = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
def calistir(data_obj):
    i=0
    info=["",""]
    print("voiceControl")
    while (data_obj.get_mode()):
        voice = data_obj.get_voice()
        if i==0:
            if voice == "yeni":
                info[0]="Lutfen isminizi soyleyin"
                data_obj.set_data(info)
                data_obj.set_voice("")
                i=1
            elif voice=="başlat":
                i=3
            else:
                continue

        elif i==1:
            if voice!="":
                i=2
                voice=voice.translate(Tr2Eng)
                info[1]=f"Isminiz {voice} ise 'evet' diyin"
                data_obj.set_data(info)
                name=voice

        elif i==2:
            if voice=="Evet":
                data_obj.set_name(name)
                info=["",""]
                data_obj.set_data(info)
                data_obj.set_screen(False)
                i=0
                continue
        else:
            data_obj.set_mode(False)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break