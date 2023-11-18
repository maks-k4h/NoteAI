from .redis import r


def log_change(note_category_uuid: str):
    r.xadd('npd', {
        'uuid': note_category_uuid,
        'channel': 'note_category',
    })

