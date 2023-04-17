from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def requires_command_substitution(self):
        pass

    @abstractmethod
    def print(self):
        pass
