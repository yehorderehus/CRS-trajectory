from scripts.data_extractor import DataExtractor
from scripts.logging_config import logger

from typing import Union
import pandas as pd
import json
import aiohttp
import time


class DataFetcher:
    def __init__(self) -> None:
        self.extractor = DataExtractor()

    def update_source(self, url: Union[str, None], columns: Union[dict, None]) -> None:
        if not isinstance(url, (str, type(None))) or not isinstance(columns, dict):
            logger.error('DataFetcher: "url" must be a str or None and "columns" must be a dict.')
            return None

        self.url = url
        self.columns = columns

    async def fetch_data(self) -> Union[pd.DataFrame, None]:
        if self.url is None or self.columns is None:
            return None

        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        logger.error(f'DataFetcher: Response status {response.status}.')
                        return None

                    fetched_data = json.loads(await response.text())

        except aiohttp.ContentTypeError as cte:
            logger.error(f'DataFetcher ContentTypeError: {cte}')
            return None
        except aiohttp.ClientError as ce:
            logger.error(f'DataFetcher ClientError: {ce}')
            return None

        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Server retrieval took {elapsed_time:.2f} seconds.')

        if not fetched_data:
            logger.error('DataFetcher: No data fetched from server.')
            return None

        return self.extractor.extract_data(data=fetched_data, columns=self.columns)
