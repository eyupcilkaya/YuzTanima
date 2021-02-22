import threading
import mainScreen
import listen
from data import data_update
import voiceControl

data_obj=data_update()

voiceControlThread=threading.Thread(target=voiceControl.calistir,args=(data_obj,))
screenThread=threading.Thread(target=mainScreen.screen,args=(data_obj,))
listenThread=threading.Thread(target=listen.dinle,args=(data_obj,))

listenThread.start()
screenThread.start()
voiceControlThread.start()