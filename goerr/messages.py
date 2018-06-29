from goerr.colors import colors


class Msgs():
    """
    Class to handle the messages
    """

    def fatal(self, i: int=None) -> str:
        """
        Returns a fatal error message
        """
        head = "[" + colors.red("\033[1mfatal error") + "]"
        if i is not None:
            head = "[" + colors.red("\033[1mfatal error " + str(i)) + "]"
        return head

    def error(self, i: int=None) -> str:
        """
        Returns an error message
        """
        head = "[" + colors.red("error") + "]"
        if i is not None:
            head = "[" + colors.red("error " + str(i)) + "]"
        return head

    def warning(self, i: int=None) -> str:
        """
        Returns a warning message
        """
        head = "[" + colors.purple("\033[1mwarning") + "]"
        if i is not None:
            head = "[" + colors.purple("\033[1mwarning " + str(i)) + "]"
        return head

    def info(self, i: int=None) -> str:
        """
        Returns an info message
        """
        head = "[" + colors.blue("info") + "]"
        if i is not None:
            head = "[" + colors.blue("info " + str(i)) + "]"
        return head

    def debug(self, i: int=None) -> str:
        """
        Returns a debug message
        """
        head = "[" + colors.yellow("debug") + "]"
        if i is not None:
            head = "[" + colors.yellow("debug " + str(i)) + "]"
        return head

