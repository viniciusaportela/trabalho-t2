class AlreadyExistsException(Exception):
    def __init__(self, entity_readable):
        super.__init__('Esse ' + entity_readable + 'ja existe')
