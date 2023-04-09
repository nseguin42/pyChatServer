import asyncio
import logging

import server
from config import Config
from generator import Generator

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    config = Config.load("../config.json")
    generator = Generator(config)
    server = server.Server(config, generator)
    asyncio.get_event_loop().run_until_complete(server.run())
