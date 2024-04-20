from scripts.dash_callbacks import DashCallbacks

import asyncio
from threading import Thread


class MainWrapper(DashCallbacks):
    def __init__(self) -> None:
        super().__init__()

        self.async_th = Thread(target=self.async_wrapper)
        self.async_th.start()
        self.run()
        self.async_th.join()

    def async_wrapper(self):
        asyncio.run(self.async_main())

    async def async_main(self):
        await asyncio.gather(self.get_data_asynchronously())
