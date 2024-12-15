import random
import typing as tp
from collections import defaultdict

import numpy as np
import util


class AbstractModel:
    def __init__(self, model_id: str):
        self._model_id = model_id
        self._features = defaultdict(list)

    @util.gen.virtual
    def predict(self, data: np.ndarray) -> float:
        pass

    def get_features(self) -> dict[str, tp.Sequence[str] | float]:
        return self._features

    @property
    def model_id(self) -> str:
        return self._model_id
