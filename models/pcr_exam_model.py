class PCRExam:
    def __init__(self, has_covid, date):
        self.__has_covid = has_covid
        self.__date = date

    @property
    def has_covid(self):
        return self.__has_covid

    @has_covid.setter
    def has_covid(self, has_covid: str):
        self.__has_covid = has_covid

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date: str):
        self.__date = date