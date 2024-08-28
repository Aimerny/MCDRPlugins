from abc import ABC, abstractmethod
from mcdreforged.api.all import *


class Processor(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
