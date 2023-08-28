# NoteAI

## Environment setup

### Security

Set up your secret signature using:

    openssl rand -hex 32

And add generated sequence to NotesAPI/secrets.env:
    
    SIGNATURE="put_your_secret_here"


### Docker compose

If you are willing to run the whole project at once, 
first set DATABASE_URL in NotesAPI/.env:

    DATABASE_URL=postgresql://user:password@pg-server/test


Then run docker compose project in the project's root directory:

    docker compose up


Now, we'll need to preform migrations. Assuming that NotesAPI runs in "notes-api" container,
this can be done using the following command:

    docker exec -it notes-api alembic upgrade head


### Running separately

You can, of course, run modules separately. 
Remember to set up .env and secrets.env in NotesAPI directory properly,
and run migrations within NotesAPI directory:
    
    alembic upgrade head


You can also use compose.yaml in Database directory to quickly run postgres server and pgadmin.