from scripts.logging_config import logger

from typing import Union
import pandas as pd
from functools import reduce
from operator import getitem


class DataExtractor:
    def __init__(self) -> None:
        pass

    def extract_data(self, data: Union[dict, list], columns: dict) -> Union[pd.DataFrame, None]:
        if not isinstance(data, (dict, list)) or not isinstance(columns, dict):
            logger.error('DataExtractor: "data" must be a dict or list and "columns" must be a dict.')
            return None

        try:
            def get_value(data: dict, key: str) -> Union[dict, None]:
                value = None
                if '.' in key:
                    keys = key.split('.')
                    try:
                        value = reduce(getitem, keys, data)
                    except (KeyError, TypeError):
                        value = None
                else:
                    value = data.get(key)
                    value = pd.to_numeric(value, errors='coerce', downcast='float')

                return value

            if isinstance(data, dict):
                df = pd.DataFrame([{key: get_value(data, key=value) for key, value in columns.items()}])
            elif isinstance(data, list):
                df = pd.DataFrame([{key: get_value(data=row, key=value) for key, value in columns.items()} for row in data])

            return df

        except KeyError as ke:
            logger.error(f'DataExtractor KeyError: {ke}')
            return None
        except TypeError as te:
            logger.error(f'DataExtractor TypeError: {te}')
            return None
