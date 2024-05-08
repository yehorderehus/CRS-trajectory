from scripts.data_extractor import DataExtractor

from typing import Union
import pandas as pd
import json
import aiohttp
import time
import os


class DataFetcher:
    def __init__(self) -> None:
        self.extractor = DataExtractor()
        self.fetched_data = None
        self.write_path = "data/current_fetched.json"

    def update_source(self, url: Union[str, None], columns: Union[dict, None]) -> None:
        if not isinstance(url, (str, type(None))) or not isinstance(columns, dict):
            raise TypeError("DataFetcher TypeError: url must be a str or None and columns must be a dict or None.")
        self.url = url
        self.columns = columns

    async def fetch_data(self) -> Union[pd.DataFrame, None]:
        if self.url is None or self.columns is None:
            return None
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        print(f"DataFetcher warning - response other than 200: {response.status}")
                        return None
                    fetched_data = await response.text()
                    fetched_data = json.loads(fetched_data)
        except aiohttp.ContentTypeError as cte:
            print(f"DataFetcher ContentTypeError: {cte}")
            return None
        except aiohttp.ClientError as ce:
            print(f"DataFetcher ClientError: {ce}")
            return None
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"DataFetcher info: Retrieval took {elapsed_time:.2f} seconds.")
        if fetched_data:
            self.fetched_data = self.extractor.extract_data(data=fetched_data, columns=self.columns)
            await self.write_data()  # If needed
            return self.fetched_data
        print("DataFetcher warning: No data fetched from server.")
        return None

    # Without [], add manually
    async def write_data(self) -> None:
        if self.fetched_data is None:
            return

        if not os.path.exists(os.path.dirname(self.write_path)):
            os.makedirs(os.path.dirname(self.write_path))

        with open(self.write_path, 'a') as json_file:
            json_data = self.fetched_data.to_dict()
            json.dump(json_data, json_file)
            json_file.write(',')
            json_file.write('\n')
