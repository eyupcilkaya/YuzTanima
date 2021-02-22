class data_update():

    def __init__(self):
        self.__info=["",""]
        self.__voice=""
        self.__state=True
        self.__name=""
        self.__mode=True

    def set_data(self,data):
        self.__info=data

    def get_data(self):
        return self.__info

    def set_voice(self,voice):
        self.__voice=voice

    def get_voice(self):
        return self.__voice

    def set_screen(self,state):
        self.__state=state

    def get_screen(self):
        return self.__state

    def set_name(self,name):
        self.__name=name

    def get_name(self):
        return self.__name

    def set_mode(self,mode):
        self.__mode=mode

    def get_mode(self):
        return self.__mode

