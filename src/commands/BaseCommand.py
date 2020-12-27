from abc import abstractmethod


class BaseCommand:

    @abstractmethod
    def execute(self):
        pass
