import random

import numpy as np

from .abstract_model import AbstractModel


class RandomModel(AbstractModel):
    def __init__(self):
        super().__init__('random')

    def predict(self, data: np) -> float:

        return random.random()
