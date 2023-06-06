class ResponseModel:
    """Format json response message."""

    def __init__(self, message, status):
        self.message = message
        self.status = status

    def to_dict(self):
        return {
            'status': self.status,
            'message': [self.message]
        }