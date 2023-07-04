class Parser:
    def check_value(self, value):
        if value:
            return value.text
        else:
            return None