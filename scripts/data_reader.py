from scripts.data_extractor import DataExtractor

from typing import Union
import pandas as pd
import json
import csv


class DataReader:
    def __init__(self):
        self.extractor = DataExtractor()
        self.readed_data = None
        self.get_index = 0

    def update_source(self, file_path: Union[str, None], columns: Union[dict, None]):
        if not isinstance(file_path, (str, type(None))) or not isinstance(columns, (dict, type(None))):
            raise TypeError("DataReader TypeError: file_path must be a str or None and columns must be a dict or None.")
        self.file_path = file_path
        self.columns = columns

    def reset_data(self) -> None:
        self.readed_data = None
        self.get_index = 0

    async def get_data(self) -> Union[pd.DataFrame, None]:
        if self.get_index < len(self.readed_data):
            self.get_index += 1
            return pd.DataFrame([self.readed_data.iloc[self.get_index - 1]]) if self.readed_data is not None else None

    async def read_data(self) -> Union[pd.DataFrame, None]:
        if self.file_path is None or self.columns is None:
            return None
        if self.readed_data is not None and not self.readed_data.empty:
            return await self.get_data()
        try:
            with open(self.file_path, 'r') as file:
                if self.file_path.endswith('.json'):
                    readed_data = json.load(file)
                elif self.file_path.endswith('.csv'):
                    reader = csv.DictReader(file)
                    readed_data = [row for row in reader]
                else:
                    raise ValueError(f"DataReader ValueError: file extension {self.file_path.split('.')[-1]} not supported.")
            if readed_data:
                self.readed_data = self.extractor.extract_data(data=readed_data, columns=self.columns)
            else:
                raise ValueError("DataReader ValueError: no data read from file.")
        except FileNotFoundError as fe:
            # print(f"DataReader FileNotFoundError: {fe}")
            return None
        except json.JSONDecodeError as je:
            print(f"DataReader JSONDecodeError: {je}")
            return None
        except csv.Error as ce:
            print(f"DataReader CSVError: {ce}")
            return None
        except ValueError as ve:
            print(f"DataReader ValueError: {ve}")
            return None
