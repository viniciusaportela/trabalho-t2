class NotExistsException(Exception):
    def __init__(self, entity_readable):
        self.entity = entity_readable
        super().__init__('This ' + entity_readable + 'not exists')
