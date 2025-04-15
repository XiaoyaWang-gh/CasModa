from abc import ABC,abstractmethod
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

class Prompt(ABC):
    @abstractmethod
    def construct_prompt(self):
        pass