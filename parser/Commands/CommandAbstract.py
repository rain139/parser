import abc


class Command(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self) -> None:
        """Action for parsing"""
        return
