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
            head = str(i) + " " + head
        return head

    def error(self, i: int=None) -> str:
        """
        Returns an error message
        """
        head = "[" + colors.red("error") + "]"
        if i is not None:
            head = str(i) + " " + head
        return head

    def warning(self, i: int=None) -> str:
        """
        Returns a warning message
        """
        head = "[" + colors.purple("\033[1mwarning") + "]"
        if i is not None:
            head = str(i) + " " + head
        return head

    def info(self, i: int=None) -> str:
        """
        Returns an info message
        """
        head = "[" + colors.blue("info") + "]"
        if i is not None:
            head = str(i) + " " + head
        return head

    def via(self, i: int=None) -> str:
        """
        Returns an via message
        """
        head = "[" + colors.green("via") + "]"
        if i is not None:
            head = str(i) + " " + head
        return head

    def debug(self, i: int=None) -> str:
        """
        Returns a debug message
        """
        head = "[" + colors.yellow("debug") + "]"
        if i is not None:
            head = str(i) + " " + head
        return head
