import asyncio
from contextlib import suppress

from internal.app.run import run

if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(run())
