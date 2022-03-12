class NotExists(Exception):
    def __init__(self, entity):
        self.entity = entity
        super().__init__('This ' + entity + 'not exists')