from .redis import r


def log_content_change(note_uuid: str):
    r.xadd('npd', {
        'uuid': note_uuid,
        'channel': 'note',
    })

