from .redis import r


def log_content_change(note_uuid: str, user_uuid: str):
    r.xadd('npd', {
        'uuid': note_uuid,
        'user_uuid': user_uuid,
        'channel': 'note',
    })

