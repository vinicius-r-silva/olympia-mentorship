from abc import ABC, abstractmethod

class CommandHandler(ABC):
    @abstractmethod
    def run(self, args):
        pass