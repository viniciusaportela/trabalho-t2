class Event:
    def __init__(self, title, max_participants, participants, local, datetime, organizers):
        self.__title = title
        self.__max_participants = max_participants
        self.__participants = participants
        self.__local = local
        self.__datetime = datetime
        self.__organizers = organizers

    def to_raw(self):
        raw_participants = []

        for participant in self.participants:
            raw_participants.append(participant.to_raw())

        organizers_str = ''
        for index, organizer in enumerate(self.organizers):
            organizers_str += organizer.name + '(' + organizer.cpf + ')'

            if (index != len(self.organizers) - 1):
                organizers_str += ', '

        return {
            "title": self.title,
            "max_participants": self.max_participants,
            "datetime": self.datetime.strftime('%d/%m/%Y %H:%M'),
            "participants": raw_participants,
            "local": self.local.to_raw(),
            "organizers": organizers_str,
        }

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def max_participants(self):
        return self.__max_participants

    @max_participants.setter
    def max_participants(self, max_participants: str):
        self.__max_participants = max_participants

    @property
    def participants(self):
        return self.__participants

    @participants.setter
    def participants(self, participants: str):
        self.__participants = participants

    @property
    def local(self):
        return self.__local

    @local.setter
    def local(self, local: str):
        self.__local = local

    @property
    def datetime(self):
        return self.__datetime

    @datetime.setter
    def datetime(self, datetime: str):
        self.__datetime = datetime

    @property
    def organizers(self):
        return self.__organizers

    @organizers.setter
    def organizers(self, organizers):
        self.__organizers = organizers
