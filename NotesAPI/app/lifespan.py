from contextlib import asynccontextmanager

from fastapi import FastAPI

from .events.redis import r


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init redis
    if not r.exists('npd'):
        r.xadd('npd', {'uuid': '', 'channel': ''})

    # ...
    yield

    # Do nothing after shutdown
    pass
