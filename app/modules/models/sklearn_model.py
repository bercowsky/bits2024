import os
import random

import joblib
import numpy as np
import pandas as pd
import util

from .abstract_model import AbstractModel


class SklearnModel(AbstractModel):
    def __init__(self, model_name: str):
        super().__init__(model_name)

        self._model = joblib.load(os.path.join(util.path.get_models_dir(), f'{model_name}.pkl'))
        print(f'Loaded {model_name}!')
        self._preprocessing = joblib.load(
            os.path.join(os.path.join(util.path.get_preprocessing_dir(), f'{model_name}_pre.pkl'))
        )

        for feature in self._model.feature_names_in_:
            name, *modality = feature.split('_')

            if modality:
                self._features[name].append(modality[0])
            else:
                self._features[name] = 0.0

    def predict(self, df: pd.DataFrame) -> np.ndarray:

        # Transform only the specified numerical columns
        transformed_data = self._preprocessing.transform(df[self._preprocessing.feature_names_in_])

        # Create a copy of the original DataFrame
        df_transformed = df.copy()

        # Replace the original numerical columns with their transformed counterparts
        df_transformed[self._preprocessing.feature_names_in_] = transformed_data

        # df_transformed = df_transformed[self._model.feature_names_in_]

        # Use the updated DataFrame for prediction
        return self._model.predict_proba(df_transformed)
