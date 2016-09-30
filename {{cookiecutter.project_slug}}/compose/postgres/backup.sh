#!/bin/bash
# stop on errors
set -e

# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "${{ cookiecutter.project_slug|upper }}_POSTGRES_1_ENV_POSTGRES_USER" == "postgres" ]
then
    echo "creating a backup as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=${{ cookiecutter.project_slug|upper }}_POSTGRES_1_ENV_POSTGRES_PASSWORD

echo "creating backup"
echo "---------------"

FILENAME=backup_$(date +'%Y_%m_%d_W-%V_T%H_%M_%S').sql.gz
pg_dump -h {{ cookiecutter.project_slug }}_postgres_1 -U ${{ cookiecutter.project_slug|upper }}_POSTGRES_1_ENV_POSTGRES_USER | gzip > /backups/$FILENAME

echo "successfully created backup $FILENAME"
