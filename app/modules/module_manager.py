import util
from modules import models


class ModuleManager:
    def __init__(self) -> None:

        self.model = models.SklearnModel(util.path.get_available_models()[0])

    def change_model(self, model_id: str) -> bool:

        if model_id not in util.path.get_available_models():
            return False

        if model_id == self.model.model_id:
            return False

        del self.model
        self.model = models.SklearnModel(model_id)
