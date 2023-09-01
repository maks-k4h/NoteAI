from contextlib import asynccontextmanager

from fastapi import FastAPI

from .events.redis import r


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init redis
    if not r.exists('changes:notes'):
        r.xadd('changes:notes', {'uuid': ''})

    # ...
    yield

    # Do nothing after shutdown
    pass
