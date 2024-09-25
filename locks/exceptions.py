
class LockCannotBeAcquiredException(Exception):
    '''
    Raised if lock cannot be set on a given object
    Attributes:
        lock -- tuple made of the user_id which currently has locked that object
                and expiration date of their lock in seconds
    '''
    def __init__(self, lock, message=None):
        self.lock = lock
        self.message = message
        super().__init__(self.message)