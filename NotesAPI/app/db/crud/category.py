
import sqlalchemy as sa
from sqlalchemy import orm

from ... import models


# CREATE

def put_category(session: orm.Session, category: models.Category) -> bool:
    try:
        session.add(category)
        session.commit()
        return True
    except:
        return False


# READ
def get_by_uuid(session: orm.Session, uuid: sa.UUID) -> models.Category | None:
    return session.get(models.Category, uuid)


def get_by_name(session: orm.Session, name: str) -> models.Category | None:
    """

    :param session: orm session
    :param name: case-sensitive category's name
    :return: Category or None
    """

    stmt = sa.select(models.Category).filter(models.Category.name == name)
    result = session.execute(stmt).scalars()
    category = result.first()

    return category


# UPDATE


# DELETE

def disconnect_user(session: orm.Session, category_uuid, user: models.User) -> bool:

    category = get_by_uuid(session, category_uuid)
    if not category:
        return False

    user.categories.remove(category)
    try:
        session.commit()
        return True
    except:
        return False


