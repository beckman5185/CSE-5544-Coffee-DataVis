import pandas as pd
from pathlib import Path
from functools import reduce

app_dir = Path(__file__).parent

dropping_columns = [
    'submission_id',
    'coffee_a_bitterness',
    'coffee_a_acidity',
    'coffee_a_personal_preference',
    'coffee_a_notes',
    'coffee_b_bitterness',
    'coffee_b_acidity',
    'coffee_b_personal_preference',
    'coffee_b_notes',
    'coffee_c_bitterness',
    'coffee_c_acidity',
    'coffee_c_personal_preference',
    'coffee_c_notes',
    'coffee_d_bitterness',
    'coffee_d_acidity',
    'coffee_d_personal_preference',
    'coffee_d_notes',
    'prefer_abc',
    'prefer_ad',
    'prefer_overall',
    'ethnicity_race_specify',
    'gender_specify',
    'why_drink_other',
    'additions_other',
    'favorite_specify',
    'purchase_other',
    'purchase',
    'brew_other'
]

multiselect_columns = [
    'where_drink',
    'brew',
    'additions',
    'dairy',
    'sweetener'
]


coffee_survey_raw = pd.read_csv("CSE-5544-Coffee-DataVis/coffee_survey.csv").iloc[:, 1:]
dropped_coffee_survey = (coffee_survey_raw.drop(columns=dropping_columns)
                         .replace(r'\(e.g.,', '(e.g.', regex=True)
                         .replace(r'\ years old', '', regex=True)
                         .assign(additions=lambda df:
                                    df['additions'].str.replace(
                                        r'Milk, dairy alternative, or coffee creamer',
                                        'dairy or alternative',
                                        regex=True
                                    )
                                 )
                         .dropna(subset=['age']))

coffee_survey = reduce(
    lambda df, col: pd.concat([df, df[col].str.get_dummies(sep=', ').add_prefix(f"{col}_")], axis=1),
    multiselect_columns,
    dropped_coffee_survey.copy()
)