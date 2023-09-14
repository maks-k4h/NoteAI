import uuid

from .. import schemas
from ..models import Role, User
from ..db import database, crud


def bind_role(role: schemas.role.RoleBase) -> schemas.role.IdentifiedRole:
    """
    Bind the role to a role in DB. If no such role exists, create new.
    :param role:
    :return:
    """
    with database.SessionLocal() as session:
        db_role = crud.role.get_by_name(session, role.name)

        if not db_role:
            db_role = Role()
            db_role.uuid = uuid.uuid4()
            db_role.name = role.name
            db_role.description = role.description

            if not crud.role.put(
                session,
                db_role
            ):
                raise Exception(f'Cannot put role \'{role.name}\' into the db')
        else:
            db_role.description = role.description
            session.commit()

        role = schemas.role.IdentifiedRole(
            uuid=str(db_role.uuid),
            name=role.name,
            description=role.description
        )

    return role


def authorize_uuid(user_uuid: str, *roles: schemas.role.IdentifiedRole) -> bool:
    """
    Check if this user has any of the passed roles. Performs DB request.
    :param user_uuid: user's uuid
    :param roles: roles to check
    :return: true if user has one of the passed roles, false otherwise
    """
    with database.SessionLocal() as session:
        user = crud.user.get_by_uuid(session, uuid.UUID(user_uuid))
        return authorize_user(user, *roles)


def authorize_user(user: User, *roles: schemas.role.IdentifiedRole) -> bool:
    """
    Check if this user has any of the passed roles.
    :param user:
    :param roles: roles to check
    :return: true if user has one of the passed roles, false otherwise
    """
    if not user:
        return False

    for role in roles:
        if role.uuid == user.role_uuid.__str__():
            return True
    return False


USER: schemas.role.IdentifiedRole = bind_role(schemas.role.RoleBase(
    name='User',
    description='Basic user'
))

NPDAEMON: schemas.role.IdentifiedRole = bind_role(schemas.role.RoleBase(
    name='NPDaemon',
    description='Note Processing Daemon'
))
