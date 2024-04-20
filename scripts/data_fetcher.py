from scripts.data_extractor import DataExtractor

from typing import Union
import pandas as pd
import json
import aiohttp
import time


class DataFetcher:
    def __init__(self) -> None:
        self.extractor = DataExtractor()
        self.fetched_data = None

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
            print(self.fetched_data)
            return self.fetched_data
        print("DataFetcher warning: No data fetched from server.")
        return None

    async def write_data(self) -> None:
        # Write if needed, consider adding control parameters to update_source and default.json
        pass
