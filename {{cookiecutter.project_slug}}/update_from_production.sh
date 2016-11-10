#!/bin/bash
set -e
echo "Dump production DB" && \
eval $(docker-machine env node1) && \
    docker-compose exec postgres pg_dump -U {{ cookiecutter.project_slug }} -d {{ cookiecutter.project_slug }} -w > {{ cookiecutter.project_slug }}/dumps/production.dump && \
        echo "Done" && \

echo "Commit" && \
    git commit {{ cookiecutter.project_slug }}/dumps/production.dump -m "Update production DB dump" && \
        echo "Done" #&& \

echo "Push" && \
    git push && \
        echo "Done"

echo "Load production data to local instance" && \
read -r -p "Are you sure? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
    eval $(docker-machine env default) && \
        docker-compose -f dev.yml stop && \
        docker-compose -f dev.yml run --rm django ./manage.py reset_db --noinput && \
        docker exec -i {{ cookiecutter.project_slug }}_postgres_1 psql -U {{ cookiecutter.project_slug }} -d {{ cookiecutter.project_slug }} -w < {{ cookiecutter.project_slug }}/dumps/production.dump && \
        docker-compose -f dev.yml run --rm django ./manage.py loaddata {{ cookiecutter.project_slug }}/fixtures/wagtail_sites.json && \
        docker-compose -f dev.yml up -d && \
            echo "Done"
fi

echo "Sync amazon S3 with local media files" && \
read -r -p "Are you sure? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
    aws s3 sync --region us-east-1 s3://{{ cookiecutter.project_slug }} {{ cookiecutter.project_slug }}/media
fi
