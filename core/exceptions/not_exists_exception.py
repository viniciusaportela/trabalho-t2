class NotExistsException(Exception):
    def __init__(self, entity_readable):
        self.entity = entity_readable
        super().__init__('Esse ' + entity_readable + 'não existe')
