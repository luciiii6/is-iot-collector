
class AirTemperatureError:
    def __init__(self):
        self.counter = 0
        self.__message = 'Air temperature sensor does not send values anymore \n'
        self.error_sent = False

    def build_message(self, message):
        if not self.error_sent:
            message += self.__message

        return message

    def reset_counter(self):
        self.counter = 0

    def reset_flag(self):
        self.error_sent = False