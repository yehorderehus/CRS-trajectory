from scripts.data_extractor import DataExtractor
from scripts.logging_config import logger

from typing import Union
import pandas as pd
import json
import csv


class DataReader:
    def __init__(self):
        self.extractor = DataExtractor()
        self.init_readed()

    def init_readed(self) -> None:
        self.readed_data = None
        self.get_index = 0

    def update_source(self, file_path: Union[str, None], columns: Union[dict, None]):
        if not isinstance(file_path, (str, type(None))) or not isinstance(columns, (dict, type(None))):
            logger.error('DataReader: "file_path" must be a str or None and "columns" must be a dict or None.')
            return None

        self.file_path = file_path
        self.columns = columns

    async def get_data(self) -> Union[pd.DataFrame, None]:
        if not self.get_index < len(self.readed_data):
            return None

        self.get_index += 1
        return pd.DataFrame([self.readed_data.iloc[self.get_index - 1]])

    async def read_data(self) -> Union[pd.DataFrame, None]:
        if isinstance(self.readed_data, pd.DataFrame) and not self.readed_data.empty:
            return await self.get_data()

        if self.file_path is None or self.columns is None:
            return None

        try:
            with open(self.file_path, 'r') as file:
                if self.file_path.endswith('.json'):
                    readed_data = json.load(file)
                elif self.file_path.endswith('.csv'):
                    readed_data = [row for row in csv.DictReader(file)]
                else:
                    logger.error('DataReader: File format not supported.')
                    return None

            if not readed_data:
                raise ValueError('No data read from file.')

            self.readed_data = self.extractor.extract_data(data=readed_data, columns=self.columns)

        except FileNotFoundError:
            # No need for an error here
            return None
        except json.JSONDecodeError as je:
            logger.error(f'DataReader JSONDecodeError: {je}')
            return None
        except csv.Error as ce:
            logger.error(f'DataReader CSVError: {ce}')
            return None
        except ValueError as ve:
            logger.error(f'DataReader ValueError: {ve}')
            return None
