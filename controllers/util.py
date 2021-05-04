

class Checkinput:

    @classmethod
    def check_input_by_regex(cls, message, regex):
        """
            check input by type and by regex
            if ok return data input else ask again
        """
        while True:
            try:
                input_str = str(input(message)).capitalize()
            except ValueError:
                # input incorrect retry
                continue
            if not re.fullmatch(regex, input_str):
                # Value input incorrect
                continue
            else:
                return input_str