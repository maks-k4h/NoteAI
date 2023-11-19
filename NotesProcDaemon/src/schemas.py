from pydantic import BaseModel


class Note(BaseModel):
    uuid: str
    title: str | None
    content: str

    def __repr__(self):
        return (f'Note(uuid={self.uuid}, '
                f'title="{self.title}", '
                f'content="{self.content if len(self.content) < 50 else self.content[:50] + "..."}")')

    def __str__(self):
        return self.__repr__()


class NoteCategory(BaseModel):
    uuid: str
    name: str



