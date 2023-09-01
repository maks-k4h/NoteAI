from typing import Awaitable

from .redis import r


def log_content_change(note_uuid: str):
    r.xadd('changes:notes', {
        'uuid': note_uuid
    })

