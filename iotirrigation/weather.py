import os

class Weather:
    def __init__(self) -> None:
        self.read_data = None
        self.api_key = os.getenv('ACCU_API_KEY')

    def get_1h_data(self):
        print(self.api_key)
