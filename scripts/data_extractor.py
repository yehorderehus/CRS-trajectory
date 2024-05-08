from typing import Union
import pandas as pd


class DataExtractor:
    def __init__(self) -> None:
        pass

    def extract_data(self, data: Union[dict, list], columns: dict) -> Union[pd.DataFrame, None]:
        if not isinstance(data, (dict, list)) or not isinstance(columns, dict):
            raise TypeError("DataExtractor TypeError: data must be a dict or a list and columns must be a dict.")
        try:
            if isinstance(data, dict):
                df = pd.DataFrame([{key: data.get(col) for key, col in columns.items()}])
            elif isinstance(data, list):
                df = pd.DataFrame([{key: row.get(col) for key, col in columns.items()} for row in data])
            # for index, row in df.iterrows():
            #     missing_columns = [col for col, value in row.items() if pd.isna(value)]
            #     if missing_columns:
            #         print(f"DataExtractor warning: Row {index}: Columns with missing values - {missing_columns}")
            return df
        except KeyError as ke:
            print(f"DataExtractor KeyError: {ke}")
            return None

# Output PdDataFrame column names are "columns" keys
