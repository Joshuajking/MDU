from typing import Dict


# Custom Response class mimicking an HTTP-like response
class Response:
    def __init__(self, status_code: int, response_data: Dict):
        self.status_code = status_code
        self.data = response_data

    def json(self):
        return self.data
