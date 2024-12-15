import pandas as pd
from sklearn.preprocessing import StandardScaler

CATEGORICAL_COLUMNS = [
    'Sex',
    'FamilialvsSporadic',
    'COD NUMBER',
    'Binary diagnosis',
    'Detail',
    'Radiological Pattern',
    'Detail on NON UIP',
    'Pathology Pattern Binary',
    'Pathology pattern UIP, probable or CHP',
    'Pathology pattern',
    'Extras AP',
    'Treatment',
    'Type of telomeric extrapulmonary affectation',
    'Extra',
    'Type of neoplasia',
    'Hematological abnormality before diagnosis',
    'Hematologic Disease',
    'Liver abnormality before diagnosis',
    'Liver abnormality',
    'Type of liver abnormality',
    'Liver disease',
    'Transplantation date',
    'Death',
    'Cause of death',
    'Identified Infection',
    'Date of death',
    'Type of family history',
    'Mutation Type',
]


NUMERICAL_COLUMNS = [
    'Pedigree',
    'Age at diagnosis',
    'Final diagnosis',
    'TOBACCO',
    'Biopsy',
    'Diagnosis after Biopsy',
    'Neutropenia',
    'FVC (L) at diagnosis',
    'FVC (%) at diagnosis',
    'DLCO (%) at diagnosis',
    'FVC (L) 1 year after diagnosis',
    'FVC (%) 1 year after diagnosis',
    'DLCO (%) 1 year after diagnosis',
    'RadioWorsening2y',
    'Genetic mutation studied in patient',
    'Severity of telomere shortening',
    'Severity of telomere shortening - Transform 4',
]


BINARY_COLUMNS = [
    'Comorbidities',
    'Multidsciplinary committee',
    'Pirfenidone',
    'Nintedanib',
    'Antifibrotic Drug',
    'Prednisone',
    'Mycophenolate',
    'Extrapulmonary affectation',
    'Associated lung cancer',
    'Other cancer',
    'Blood count abnormality at diagnosis',
    'Anemia',
    'Thrombocytopenia',
    'Thrombocytosis',
    'Lymphocytosis',
    'Lymphopenia',
    'Neutrophilia',
    'Leukocytosis',
    'Leukopenia',
    'LDH',
    'ALT',
    'AST',
    'ALP',
    'GGT',
    'Transaminitis',
    'Cholestasis',
    'Necessity of transplantation',
    '1st degree relative',
    '2nd degree relative',
    'More than 1 relative',
    'Progressive disease',
    'ProgressiveDisease',
    'target',
]


def preprocess_data(data: pd.DataFrame) -> tuple[pd.DataFrame, StandardScaler]:
    # Replace missing values with a new category for categorical columns,
    # and with the mean for numerical columns
    columns = data.columns
    numerical_in_data = [c for c in columns if c in NUMERICAL_COLUMNS]
    categorical_in_data = [c for c in columns if c in CATEGORICAL_COLUMNS]

    for column in columns:
        if column in CATEGORICAL_COLUMNS:
            data[column] = data[column].fillna('Unknown')
        elif column in NUMERICAL_COLUMNS:
            data[column] = data[column].fillna(data[column].mean())
        elif column in BINARY_COLUMNS:
            data[column] = data[column].fillna(data[column].median())

    # Standardize numerical columns and one-hot encode categorical columns.
    scaler = StandardScaler()
    data = pd.get_dummies(data, columns=categorical_in_data)
    data[numerical_in_data] = scaler.fit_transform(data[numerical_in_data])

    return data[data.notnull().all(axis=1)], scaler


# Store in a json all the column names, and all the possible values that they can have (if they are categorical), or 0 if they are numerical
def get_columns_info(data: pd.DataFrame) -> dict:
    columns = data.columns
    columns_info = {}
    for column in columns:
        if column in CATEGORICAL_COLUMNS:
            columns_info[column] = list(data[column].unique())
        else:
            columns_info[column] = 0

    return columns_info
