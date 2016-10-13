#!/bin/bash
set -e
echo "Dump data" && \
eval $(docker-machine env default) && \
    docker-compose -f dev.yml run --rm django python -Wi manage.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions -o {{ cookiecutter.project_slug }}/dumps/data.json && \
        echo "Done" && \

echo "Commit" && \
    git add {{ cookiecutter.project_slug }}/dumps/data.json && \
    git commit {{ cookiecutter.project_slug }}/dumps/data.json -m "Update fixtures" && \
        echo "Done"

{% if use_translations %}
echo "Compile translations" && \
eval $(docker-machine env default) && \
    docker-compose -f dev.yml run --rm django python -Wi manage.py compilemessages && \
        echo "Done" && \

echo "Commit" && \
    git add {{ cookiecutter.project_slug }}/locale && \
    git commit {{ cookiecutter.project_slug }}/locale -m "Update translations" && \
        echo "Done"
{% endif %}

echo "Push" && \
    git push && \
        echo "Done"

echo "Sync S3" && \
eval $(docker-machine env default) && \
    docker-compose -f dev.yml run --rm django ./manage.py sync_s3 --media-only && \
        echo "Done"

echo "Build docker image" && \
eval $(docker-machine env node1) && \
    docker-compose build && \
        echo "Done" && \
echo "Create docker containers"
eval $(docker-machine env node1) && \
    docker-compose up -d && \
        echo "Done" && \
echo "Migrate DB" && \
eval $(docker-machine env node1) && \
    docker-compose run --rm django ./manage.py migrate && \
        echo "Done" && \
echo "Load DB data" && \
eval $(docker-machine env node1) && \
    docker-compose run --rm django ./manage.py loaddata {{ cookiecutter.project_slug }}/dumps/data.json && \
        echo "Done"
