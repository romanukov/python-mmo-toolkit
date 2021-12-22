import asyncio

import inject

from backend.common.network.server import Server
from backend.ioc.container import container


if __name__ == "__main__":
    inject.configure(container)
    server_coroutine = Server().run('localhost', 3000)
    asyncio.run(server_coroutine)
