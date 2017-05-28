class BadEngine(Exception):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error


class BadAction(Exception):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error


class BadRequest(Exception):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error


class ProcessRequest(Exception):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error


class RequestError(Exception):
    def __init__(self, error, data=None):
        self.error = error
        self.data = data

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error


class ServerError(Exception):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error
